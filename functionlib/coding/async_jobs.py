"""
Async job management system.

Provides job queues, workers, schedulers, and task management for async operations.
Pure Python implementation using threading and queue modules.
"""

import queue
import threading
import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import defaultdict
from enum import Enum
import json


class JobStatus(Enum):
    """Job status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"


class Job:
    """Represents a job to be executed."""
    
    def __init__(self, func: Callable, args: Tuple = (), kwargs: Optional[Dict] = None,
                 job_id: Optional[str] = None, priority: int = 0, max_retries: int = 0):
        self.job_id = job_id or str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.priority = priority
        self.max_retries = max_retries
        self.retry_count = 0
        
        self.status = JobStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
    
    def __lt__(self, other):
        """Compare jobs by priority (for priority queue)."""
        return self.priority > other.priority  # Higher priority = lower value in queue
    
    def execute(self):
        """Execute the job."""
        self.status = JobStatus.RUNNING
        self.started_at = time.time()
        
        try:
            self.result = self.func(*self.args, **self.kwargs)
            self.status = JobStatus.COMPLETED
        except Exception as e:
            self.error = str(e)
            if self.retry_count < self.max_retries:
                self.status = JobStatus.RETRYING
                self.retry_count += 1
            else:
                self.status = JobStatus.FAILED
        finally:
            self.completed_at = time.time()
    
    def to_dict(self) -> Dict:
        """Convert job to dictionary."""
        return {
            'job_id': self.job_id,
            'status': self.status.value,
            'priority': self.priority,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'result': str(self.result) if self.result is not None else None,
            'error': self.error
        }


class JobQueue:
    """Thread-safe job queue with priority support."""
    
    def __init__(self, maxsize: int = 0):
        self.queue = queue.PriorityQueue(maxsize=maxsize)
        self.jobs = {}  # job_id -> Job mapping
        self.lock = threading.Lock()
    
    def enqueue(self, job: Job):
        """Add a job to the queue."""
        with self.lock:
            self.jobs[job.job_id] = job
        self.queue.put(job)
    
    def dequeue(self, timeout: Optional[float] = None) -> Optional[Job]:
        """Get a job from the queue."""
        try:
            job = self.queue.get(timeout=timeout)
            return job
        except queue.Empty:
            return None
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID."""
        with self.lock:
            return self.jobs.get(job_id)
    
    def list_jobs(self, status: Optional[JobStatus] = None) -> List[Job]:
        """List all jobs, optionally filtered by status."""
        with self.lock:
            if status:
                return [job for job in self.jobs.values() if job.status == status]
            return list(self.jobs.values())
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending job."""
        with self.lock:
            job = self.jobs.get(job_id)
            if job and job.status == JobStatus.PENDING:
                job.status = JobStatus.CANCELLED
                return True
        return False
    
    def clear_completed(self):
        """Remove completed jobs from tracking."""
        with self.lock:
            completed_ids = [
                job_id for job_id, job in self.jobs.items()
                if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]
            ]
            for job_id in completed_ids:
                del self.jobs[job_id]
    
    def size(self) -> int:
        """Return queue size."""
        return self.queue.qsize()


class Worker(threading.Thread):
    """Worker thread that processes jobs from a queue."""
    
    def __init__(self, worker_id: str, job_queue: JobQueue, stop_event: threading.Event):
        super().__init__(daemon=True)
        self.worker_id = worker_id
        self.job_queue = job_queue
        self.stop_event = stop_event
        self.jobs_processed = 0
    
    def run(self):
        """Main worker loop."""
        while not self.stop_event.is_set():
            job = self.job_queue.dequeue(timeout=1.0)
            
            if job is None:
                continue
            
            if job.status == JobStatus.CANCELLED:
                continue
            
            job.execute()
            self.jobs_processed += 1
            
            # Re-queue if retrying
            if job.status == JobStatus.RETRYING:
                time.sleep(1)  # Brief delay before retry
                job.status = JobStatus.PENDING
                self.job_queue.enqueue(job)


class WorkerPool:
    """Pool of workers to process jobs."""
    
    def __init__(self, num_workers: int = 4, job_queue: Optional[JobQueue] = None):
        self.num_workers = num_workers
        self.job_queue = job_queue or JobQueue()
        self.workers = []
        self.stop_event = threading.Event()
        self.running = False
    
    def start(self):
        """Start all workers."""
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        
        for i in range(self.num_workers):
            worker = Worker(f"worker-{i}", self.job_queue, self.stop_event)
            worker.start()
            self.workers.append(worker)
    
    def stop(self, wait: bool = True):
        """Stop all workers."""
        if not self.running:
            return
        
        self.stop_event.set()
        
        if wait:
            for worker in self.workers:
                worker.join(timeout=5.0)
        
        self.workers.clear()
        self.running = False
    
    def submit(self, func: Callable, *args, **kwargs) -> str:
        """Submit a job to the pool."""
        job = Job(func, args, kwargs)
        self.job_queue.enqueue(job)
        return job.job_id
    
    def submit_with_priority(self, func: Callable, priority: int, *args, **kwargs) -> str:
        """Submit a job with priority."""
        job = Job(func, args, kwargs, priority=priority)
        self.job_queue.enqueue(job)
        return job.job_id
    
    def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        """Get status of a job."""
        job = self.job_queue.get_job(job_id)
        return job.status if job else None
    
    def get_job_result(self, job_id: str) -> Optional[Any]:
        """Get result of a completed job."""
        job = self.job_queue.get_job(job_id)
        if job and job.status == JobStatus.COMPLETED:
            return job.result
        return None
    
    def wait_for_job(self, job_id: str, timeout: Optional[float] = None) -> bool:
        """Wait for a job to complete."""
        start_time = time.time()
        
        while True:
            job = self.job_queue.get_job(job_id)
            
            if not job:
                return False
            
            if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                return job.status == JobStatus.COMPLETED
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.1)
    
    def get_statistics(self) -> Dict:
        """Get worker pool statistics."""
        jobs = self.job_queue.list_jobs()
        
        status_counts = defaultdict(int)
        for job in jobs:
            status_counts[job.status.value] += 1
        
        total_processed = sum(w.jobs_processed for w in self.workers)
        
        return {
            'num_workers': self.num_workers,
            'running': self.running,
            'queue_size': self.job_queue.size(),
            'total_jobs': len(jobs),
            'total_processed': total_processed,
            'status_counts': dict(status_counts)
        }


class Scheduler:
    """Schedule jobs to run at specific times or intervals."""
    
    def __init__(self, worker_pool: Optional[WorkerPool] = None):
        self.worker_pool = worker_pool or WorkerPool()
        self.scheduled_jobs = []
        self.running = False
        self.stop_event = threading.Event()
        self.scheduler_thread = None
    
    def schedule_once(self, func: Callable, delay: float, *args, **kwargs) -> str:
        """Schedule a job to run once after a delay."""
        run_at = time.time() + delay
        job_id = str(uuid.uuid4())
        
        scheduled_job = {
            'job_id': job_id,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'run_at': run_at,
            'interval': None,
            'last_run': None
        }
        
        self.scheduled_jobs.append(scheduled_job)
        return job_id
    
    def schedule_interval(self, func: Callable, interval: float, *args, **kwargs) -> str:
        """Schedule a job to run repeatedly at an interval."""
        job_id = str(uuid.uuid4())
        
        scheduled_job = {
            'job_id': job_id,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'run_at': time.time() + interval,
            'interval': interval,
            'last_run': None
        }
        
        self.scheduled_jobs.append(scheduled_job)
        return job_id
    
    def cancel_scheduled(self, job_id: str) -> bool:
        """Cancel a scheduled job."""
        for i, sj in enumerate(self.scheduled_jobs):
            if sj['job_id'] == job_id:
                self.scheduled_jobs.pop(i)
                return True
        return False
    
    def start(self):
        """Start the scheduler."""
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        self.worker_pool.start()
        
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
    
    def stop(self):
        """Stop the scheduler."""
        if not self.running:
            return
        
        self.stop_event.set()
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)
        
        self.worker_pool.stop()
        self.running = False
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while not self.stop_event.is_set():
            current_time = time.time()
            
            for scheduled_job in self.scheduled_jobs[:]:  # Copy list to allow modification
                if current_time >= scheduled_job['run_at']:
                    # Submit job to worker pool
                    self.worker_pool.submit(
                        scheduled_job['func'],
                        *scheduled_job['args'],
                        **scheduled_job['kwargs']
                    )
                    
                    scheduled_job['last_run'] = current_time
                    
                    # Reschedule if interval-based
                    if scheduled_job['interval']:
                        scheduled_job['run_at'] = current_time + scheduled_job['interval']
                    else:
                        # Remove one-time jobs
                        self.scheduled_jobs.remove(scheduled_job)
            
            time.sleep(0.1)


class TaskBatch:
    """Execute multiple tasks in batch."""
    
    def __init__(self, worker_pool: Optional[WorkerPool] = None):
        self.worker_pool = worker_pool or WorkerPool()
        self.tasks = []
    
    def add_task(self, func: Callable, *args, **kwargs):
        """Add a task to the batch."""
        self.tasks.append((func, args, kwargs))
    
    def execute(self, wait: bool = True) -> List[str]:
        """Execute all tasks."""
        if not self.worker_pool.running:
            self.worker_pool.start()
        
        job_ids = []
        for func, args, kwargs in self.tasks:
            job_id = self.worker_pool.submit(func, *args, **kwargs)
            job_ids.append(job_id)
        
        if wait:
            for job_id in job_ids:
                self.worker_pool.wait_for_job(job_id)
        
        return job_ids
    
    def get_results(self, job_ids: List[str]) -> List[Any]:
        """Get results for all jobs."""
        return [self.worker_pool.get_job_result(job_id) for job_id in job_ids]


class RateLimiter:
    """Rate limiter for job submission."""
    
    def __init__(self, max_calls: int, time_window: float):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
        self.lock = threading.Lock()
    
    def acquire(self, timeout: Optional[float] = None) -> bool:
        """Acquire permission to make a call."""
        start_time = time.time()
        
        while True:
            with self.lock:
                current_time = time.time()
                
                # Remove old calls outside the window
                self.calls = [t for t in self.calls if current_time - t < self.time_window]
                
                if len(self.calls) < self.max_calls:
                    self.calls.append(current_time)
                    return True
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.01)


class JobProgressTracker:
    """Track progress of long-running jobs."""
    
    def __init__(self):
        self.progress = {}
        self.lock = threading.Lock()
    
    def update_progress(self, job_id: str, current: int, total: int, message: str = ""):
        """Update job progress."""
        with self.lock:
            self.progress[job_id] = {
                'current': current,
                'total': total,
                'percentage': (current / total * 100) if total > 0 else 0,
                'message': message,
                'updated_at': time.time()
            }
    
    def get_progress(self, job_id: str) -> Optional[Dict]:
        """Get job progress."""
        with self.lock:
            return self.progress.get(job_id)
    
    def clear_progress(self, job_id: str):
        """Clear progress for a job."""
        with self.lock:
            self.progress.pop(job_id, None)


def create_job_chain(jobs: List[Tuple[Callable, tuple, dict]], worker_pool: Optional[WorkerPool] = None) -> List[str]:
    """
    Execute jobs in sequence, passing output of each to the next.
    """
    if not worker_pool:
        worker_pool = WorkerPool()
        worker_pool.start()
    
    job_ids = []
    previous_result = None
    
    for func, args, kwargs in jobs:
        # Add previous result as first argument if it exists
        if previous_result is not None:
            args = (previous_result,) + args
        
        job_id = worker_pool.submit(func, *args, **kwargs)
        job_ids.append(job_id)
        
        # Wait for job to complete
        worker_pool.wait_for_job(job_id)
        previous_result = worker_pool.get_job_result(job_id)
    
    return job_ids


__all__ = [
    'JobStatus',
    'Job',
    'JobQueue',
    'Worker',
    'WorkerPool',
    'Scheduler',
    'TaskBatch',
    'RateLimiter',
    'JobProgressTracker',
    'create_job_chain'
]
