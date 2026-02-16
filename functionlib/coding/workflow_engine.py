"""
Workflow Engine for DAG-based task orchestration.

Provides workflow definition, task dependencies, execution, and monitoring.
Pure Python implementation supporting complex workflow patterns.
"""

import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from collections import defaultdict, deque
from enum import Enum
import json
import threading


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    CANCELLED = "cancelled"


class Task:
    """Represents a task in a workflow."""
    
    def __init__(self, task_id: str, func: Callable, args: Tuple = (), kwargs: Optional[Dict] = None,
                 retry_count: int = 0, timeout: Optional[float] = None):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs or {}
        self.retry_count = retry_count
        self.timeout = timeout
        
        self.dependencies = []  # Tasks that must complete before this
        self.dependents = []  # Tasks that depend on this
        
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.retries_left = retry_count
        
        self.started_at = None
        self.completed_at = None
    
    def add_dependency(self, task: 'Task'):
        """Add a task dependency."""
        if task not in self.dependencies:
            self.dependencies.append(task)
            task.dependents.append(self)
    
    def can_run(self) -> bool:
        """Check if task is ready to run."""
        if self.status != TaskStatus.PENDING:
            return False
        
        # All dependencies must be completed
        return all(dep.status == TaskStatus.COMPLETED for dep in self.dependencies)
    
    def execute(self) -> bool:
        """Execute the task. Returns True if successful."""
        self.status = TaskStatus.RUNNING
        self.started_at = time.time()
        
        try:
            # Get results from dependencies
            dep_results = {dep.task_id: dep.result for dep in self.dependencies}
            
            # Add dependency results to kwargs
            kwargs = self.kwargs.copy()
            if dep_results:
                kwargs['_dependencies'] = dep_results
            
            self.result = self.func(*self.args, **kwargs)
            self.status = TaskStatus.COMPLETED
            self.completed_at = time.time()
            return True
            
        except Exception as e:
            self.error = str(e)
            
            if self.retries_left > 0:
                self.retries_left -= 1
                self.status = TaskStatus.PENDING
                return False
            else:
                self.status = TaskStatus.FAILED
                self.completed_at = time.time()
                return False
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary."""
        return {
            'task_id': self.task_id,
            'status': self.status.value,
            'dependencies': [dep.task_id for dep in self.dependencies],
            'result': str(self.result) if self.result is not None else None,
            'error': self.error,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'retries_left': self.retries_left
        }


class Workflow:
    """Workflow containing tasks and their dependencies (DAG)."""
    
    def __init__(self, workflow_id: Optional[str] = None):
        self.workflow_id = workflow_id or str(uuid.uuid4())
        self.tasks = {}  # task_id -> Task
        self.execution_order = []
        self.status = "pending"
        self.created_at = time.time()
        self.started_at = None
        self.completed_at = None
    
    def add_task(self, task: Task):
        """Add a task to the workflow."""
        self.tasks[task.task_id] = task
    
    def add_task_from_func(self, task_id: str, func: Callable, dependencies: Optional[List[str]] = None,
                          args: Tuple = (), kwargs: Optional[Dict] = None, **task_kwargs) -> Task:
        """Create and add a task from a function."""
        task = Task(task_id, func, args, kwargs, **task_kwargs)
        self.add_task(task)
        
        if dependencies:
            for dep_id in dependencies:
                if dep_id in self.tasks:
                    task.add_dependency(self.tasks[dep_id])
        
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate workflow (check for cycles, orphans)."""
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            
            task = self.tasks[task_id]
            for dep in task.dependencies:
                if dep.task_id not in visited:
                    if has_cycle(dep.task_id):
                        return True
                elif dep.task_id in rec_stack:
                    return True
            
            rec_stack.remove(task_id)
            return False
        
        for task_id in self.tasks:
            if task_id not in visited:
                if has_cycle(task_id):
                    return False, f"Cycle detected in workflow"
        
        return True, None
    
    def topological_sort(self) -> List[str]:
        """Get tasks in topological order."""
        in_degree = {task_id: 0 for task_id in self.tasks}
        
        # Calculate in-degrees
        for task in self.tasks.values():
            for dep in task.dependencies:
                in_degree[task.task_id] += 1
        
        # Queue of tasks with no dependencies
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        sorted_tasks = []
        
        while queue:
            task_id = queue.popleft()
            sorted_tasks.append(task_id)
            
            task = self.tasks[task_id]
            for dependent in task.dependents:
                in_degree[dependent.task_id] -= 1
                if in_degree[dependent.task_id] == 0:
                    queue.append(dependent.task_id)
        
        return sorted_tasks
    
    def get_ready_tasks(self) -> List[Task]:
        """Get all tasks that are ready to run."""
        return [task for task in self.tasks.values() if task.can_run()]
    
    def is_complete(self) -> bool:
        """Check if workflow is complete."""
        return all(
            task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED, TaskStatus.CANCELLED]
            for task in self.tasks.values()
        )
    
    def get_statistics(self) -> Dict:
        """Get workflow statistics."""
        status_counts = defaultdict(int)
        for task in self.tasks.values():
            status_counts[task.status.value] += 1
        
        duration = None
        if self.started_at:
            end_time = self.completed_at or time.time()
            duration = end_time - self.started_at
        
        return {
            'workflow_id': self.workflow_id,
            'status': self.status,
            'total_tasks': len(self.tasks),
            'status_counts': dict(status_counts),
            'duration': duration,
            'created_at': self.created_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at
        }
    
    def to_dict(self) -> Dict:
        """Convert workflow to dictionary."""
        return {
            'workflow_id': self.workflow_id,
            'status': self.status,
            'tasks': {task_id: task.to_dict() for task_id, task in self.tasks.items()},
            'statistics': self.get_statistics()
        }
    
    def save(self, filepath: str):
        """Save workflow state to file."""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class WorkflowExecutor:
    """Execute workflows with various strategies."""
    
    def __init__(self, max_parallel: int = 4):
        self.max_parallel = max_parallel
        self.running_tasks = {}
        self.lock = threading.Lock()
    
    def execute_sequential(self, workflow: Workflow) -> bool:
        """Execute workflow tasks sequentially."""
        valid, error = workflow.validate()
        if not valid:
            workflow.status = "invalid"
            return False
        
        workflow.status = "running"
        workflow.started_at = time.time()
        
        sorted_tasks = workflow.topological_sort()
        
        for task_id in sorted_tasks:
            task = workflow.get_task(task_id)
            if not task.execute():
                workflow.status = "failed"
                workflow.completed_at = time.time()
                return False
        
        workflow.status = "completed"
        workflow.completed_at = time.time()
        return True
    
    def execute_parallel(self, workflow: Workflow) -> bool:
        """Execute workflow tasks in parallel where possible."""
        valid, error = workflow.validate()
        if not valid:
            workflow.status = "invalid"
            return False
        
        workflow.status = "running"
        workflow.started_at = time.time()
        
        threads = []
        
        while not workflow.is_complete():
            ready_tasks = workflow.get_ready_tasks()
            
            if not ready_tasks:
                # Wait for running tasks
                time.sleep(0.1)
                continue
            
            # Mark tasks as ready
            for task in ready_tasks:
                task.status = TaskStatus.READY
            
            # Execute up to max_parallel tasks
            for task in ready_tasks[:self.max_parallel]:
                thread = threading.Thread(target=task.execute)
                thread.start()
                threads.append(thread)
            
            # Wait for batch to complete
            for thread in threads:
                thread.join()
            threads.clear()
        
        # Check if any tasks failed
        failed_tasks = [t for t in workflow.tasks.values() if t.status == TaskStatus.FAILED]
        
        if failed_tasks:
            workflow.status = "failed"
        else:
            workflow.status = "completed"
        
        workflow.completed_at = time.time()
        return workflow.status == "completed"
    
    def execute_with_callback(self, workflow: Workflow, 
                            on_task_complete: Optional[Callable] = None,
                            on_task_fail: Optional[Callable] = None) -> bool:
        """Execute workflow with callbacks on task completion/failure."""
        valid, error = workflow.validate()
        if not valid:
            workflow.status = "invalid"
            return False
        
        workflow.status = "running"
        workflow.started_at = time.time()
        
        sorted_tasks = workflow.topological_sort()
        
        for task_id in sorted_tasks:
            task = workflow.get_task(task_id)
            success = task.execute()
            
            if success and on_task_complete:
                on_task_complete(task)
            elif not success and on_task_fail:
                on_task_fail(task)
            
            if not success:
                workflow.status = "failed"
                workflow.completed_at = time.time()
                return False
        
        workflow.status = "completed"
        workflow.completed_at = time.time()
        return True


class ConditionalTask(Task):
    """Task that runs conditionally based on a predicate."""
    
    def __init__(self, task_id: str, func: Callable, condition: Callable,
                 args: Tuple = (), kwargs: Optional[Dict] = None, **task_kwargs):
        super().__init__(task_id, func, args, kwargs, **task_kwargs)
        self.condition = condition
    
    def execute(self) -> bool:
        """Execute task only if condition is met."""
        # Evaluate condition
        dep_results = {dep.task_id: dep.result for dep in self.dependencies}
        
        try:
            should_run = self.condition(dep_results)
        except Exception as e:
            self.error = f"Condition evaluation failed: {e}"
            self.status = TaskStatus.FAILED
            return False
        
        if not should_run:
            self.status = TaskStatus.SKIPPED
            self.completed_at = time.time()
            return True
        
        return super().execute()


class ParallelTaskGroup:
    """Group of tasks that run in parallel."""
    
    def __init__(self, group_id: str):
        self.group_id = group_id
        self.tasks = []
    
    def add_task(self, task: Task):
        """Add a task to the group."""
        self.tasks.append(task)
    
    def execute(self) -> bool:
        """Execute all tasks in parallel."""
        threads = []
        
        for task in self.tasks:
            thread = threading.Thread(target=task.execute)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        # Return True if all succeeded
        return all(task.status == TaskStatus.COMPLETED for task in self.tasks)


class WorkflowTemplate:
    """Template for creating workflows with common patterns."""
    
    @staticmethod
    def create_map_reduce(map_func: Callable, reduce_func: Callable, 
                         inputs: List[Any]) -> Workflow:
        """Create a map-reduce workflow."""
        workflow = Workflow()
        
        # Create map tasks
        map_tasks = []
        for i, inp in enumerate(inputs):
            task = workflow.add_task_from_func(
                f"map_{i}",
                map_func,
                args=(inp,)
            )
            map_tasks.append(task.task_id)
        
        # Create reduce task
        workflow.add_task_from_func(
            "reduce",
            reduce_func,
            dependencies=map_tasks
        )
        
        return workflow
    
    @staticmethod
    def create_pipeline(stages: List[Tuple[str, Callable]]) -> Workflow:
        """Create a linear pipeline workflow."""
        workflow = Workflow()
        
        previous_task_id = None
        for stage_name, func in stages:
            dependencies = [previous_task_id] if previous_task_id else None
            task = workflow.add_task_from_func(stage_name, func, dependencies=dependencies)
            previous_task_id = task.task_id
        
        return workflow
    
    @staticmethod
    def create_fan_out_fan_in(prepare_func: Callable, parallel_funcs: List[Tuple[str, Callable]],
                             aggregate_func: Callable) -> Workflow:
        """Create a fan-out/fan-in workflow."""
        workflow = Workflow()
        
        # Prepare task
        prepare_task = workflow.add_task_from_func("prepare", prepare_func)
        
        # Parallel tasks
        parallel_task_ids = []
        for name, func in parallel_funcs:
            task = workflow.add_task_from_func(
                name,
                func,
                dependencies=["prepare"]
            )
            parallel_task_ids.append(task.task_id)
        
        # Aggregate task
        workflow.add_task_from_func(
            "aggregate",
            aggregate_func,
            dependencies=parallel_task_ids
        )
        
        return workflow


class WorkflowMonitor:
    """Monitor workflow execution."""
    
    def __init__(self):
        self.workflows = {}
        self.lock = threading.Lock()
    
    def register_workflow(self, workflow: Workflow):
        """Register a workflow for monitoring."""
        with self.lock:
            self.workflows[workflow.workflow_id] = workflow
    
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict]:
        """Get current status of a workflow."""
        with self.lock:
            workflow = self.workflows.get(workflow_id)
            if workflow:
                return workflow.get_statistics()
        return None
    
    def get_all_workflows(self) -> Dict[str, Dict]:
        """Get status of all workflows."""
        with self.lock:
            return {
                wf_id: wf.get_statistics()
                for wf_id, wf in self.workflows.items()
            }
    
    def cleanup_completed(self):
        """Remove completed workflows from monitoring."""
        with self.lock:
            completed = [
                wf_id for wf_id, wf in self.workflows.items()
                if wf.is_complete()
            ]
            for wf_id in completed:
                del self.workflows[wf_id]


def visualize_workflow(workflow: Workflow) -> str:
    """Create a text visualization of the workflow DAG."""
    lines = [f"Workflow: {workflow.workflow_id}"]
    lines.append("=" * 50)
    
    # Topological sort for display order
    sorted_tasks = workflow.topological_sort()
    
    for task_id in sorted_tasks:
        task = workflow.get_task(task_id)
        status_symbol = {
            TaskStatus.PENDING: "⏸",
            TaskStatus.READY: "▶",
            TaskStatus.RUNNING: "⚙",
            TaskStatus.COMPLETED: "✓",
            TaskStatus.FAILED: "✗",
            TaskStatus.SKIPPED: "⊘",
            TaskStatus.CANCELLED: "⊗"
        }.get(task.status, "?")
        
        indent = len(task.dependencies) * 2
        deps_str = f" <- [{', '.join(d.task_id for d in task.dependencies)}]" if task.dependencies else ""
        
        lines.append(f"{' ' * indent}{status_symbol} {task_id}{deps_str}")
    
    return "\n".join(lines)


__all__ = [
    'TaskStatus',
    'Task',
    'Workflow',
    'WorkflowExecutor',
    'ConditionalTask',
    'ParallelTaskGroup',
    'WorkflowTemplate',
    'WorkflowMonitor',
    'visualize_workflow'
]
