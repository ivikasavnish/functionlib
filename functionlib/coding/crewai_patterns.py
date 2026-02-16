"""
CrewAI-style multi-agent patterns.

Provides agent roles, task delegation, crew management, and collaborative workflows.
Pure Python implementation of multi-agent orchestration patterns.
"""

import time
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import defaultdict
from enum import Enum
import json


class AgentRole(Enum):
    """Predefined agent roles."""
    RESEARCHER = "researcher"
    WRITER = "writer"
    REVIEWER = "reviewer"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    MANAGER = "manager"
    DESIGNER = "designer"
    TESTER = "tester"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Agent:
    """An agent with a role, goal, and backstory."""
    
    def __init__(self, role: str, goal: str, backstory: str,
                 llm_fn: Optional[Callable] = None, tools: Optional[List[Dict]] = None):
        self.agent_id = str(uuid.uuid4())[:8]
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.llm_fn = llm_fn or self._mock_llm
        self.tools = {tool['name']: tool for tool in (tools or [])}
        
        self.tasks_completed = 0
        self.context = {}
    
    def _mock_llm(self, prompt: str) -> str:
        """Mock LLM for testing."""
        return f"[{self.role}]: Response to task"
    
    def execute_task(self, task: 'CrewTask', context: Optional[Dict] = None) -> str:
        """Execute a task with given context."""
        # Build prompt with role context
        prompt = f"""You are a {self.role}.
Goal: {self.goal}
Background: {self.backstory}

Task: {task.description}
Expected Output: {task.expected_output}

{f"Context: {json.dumps(context)}" if context else ""}

Please complete this task:"""
        
        # Call LLM
        result = self.llm_fn(prompt)
        
        self.tasks_completed += 1
        self.context.update(context or {})
        
        return result
    
    def use_tool(self, tool_name: str, tool_input: Any) -> Any:
        """Use a tool available to the agent."""
        if tool_name in self.tools:
            tool_fn = self.tools[tool_name]['function']
            return tool_fn(tool_input)
        raise ValueError(f"Tool {tool_name} not available to agent")
    
    def to_dict(self) -> Dict:
        """Convert agent to dictionary."""
        return {
            'agent_id': self.agent_id,
            'role': self.role,
            'goal': self.goal,
            'backstory': self.backstory,
            'tasks_completed': self.tasks_completed,
            'available_tools': list(self.tools.keys())
        }


class CrewTask:
    """A task to be executed by an agent."""
    
    def __init__(self, description: str, expected_output: str,
                 agent: Optional[Agent] = None, priority: TaskPriority = TaskPriority.MEDIUM,
                 async_execution: bool = False):
        self.task_id = str(uuid.uuid4())[:8]
        self.description = description
        self.expected_output = expected_output
        self.agent = agent
        self.priority = priority
        self.async_execution = async_execution
        
        self.status = "pending"
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None
        self.dependencies = []
    
    def add_dependency(self, task: 'CrewTask'):
        """Add a task dependency."""
        self.dependencies.append(task)
    
    def can_execute(self) -> bool:
        """Check if task can be executed."""
        return all(dep.status == "completed" for dep in self.dependencies)
    
    def execute(self, agent: Optional[Agent] = None, context: Optional[Dict] = None) -> str:
        """Execute the task."""
        executing_agent = agent or self.agent
        if not executing_agent:
            raise ValueError("No agent assigned to task")
        
        self.status = "running"
        self.started_at = time.time()
        
        try:
            # Get context from dependencies
            dep_context = {}
            for dep in self.dependencies:
                if dep.result:
                    dep_context[dep.task_id] = dep.result
            
            # Merge with provided context
            full_context = {**(context or {}), **dep_context}
            
            self.result = executing_agent.execute_task(self, full_context)
            self.status = "completed"
            
        except Exception as e:
            self.error = str(e)
            self.status = "failed"
        
        finally:
            self.completed_at = time.time()
        
        return self.result
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary."""
        return {
            'task_id': self.task_id,
            'description': self.description[:100],
            'agent': self.agent.role if self.agent else None,
            'priority': self.priority.value,
            'status': self.status,
            'result': str(self.result)[:200] if self.result else None,
            'error': self.error
        }


class Crew:
    """A crew of agents working together on tasks."""
    
    def __init__(self, agents: List[Agent], tasks: List[CrewTask],
                 process: str = "sequential"):
        self.crew_id = str(uuid.uuid4())[:8]
        self.agents = agents
        self.tasks = tasks
        self.process = process  # "sequential" or "hierarchical"
        
        self.status = "initialized"
        self.results = []
    
    def kickoff(self) -> List[str]:
        """Start the crew working on tasks."""
        self.status = "running"
        self.results = []
        
        if self.process == "sequential":
            return self._execute_sequential()
        elif self.process == "hierarchical":
            return self._execute_hierarchical()
        else:
            raise ValueError(f"Unknown process: {self.process}")
    
    def _execute_sequential(self) -> List[str]:
        """Execute tasks sequentially."""
        context = {}
        
        for task in self.tasks:
            if not task.can_execute():
                raise RuntimeError(f"Task {task.task_id} dependencies not met")
            
            result = task.execute(context=context)
            self.results.append(result)
            
            # Add result to context for next tasks
            context[task.task_id] = result
        
        self.status = "completed"
        return self.results
    
    def _execute_hierarchical(self) -> List[str]:
        """Execute tasks with manager delegation."""
        # Find manager agent
        manager = next((a for a in self.agents if 'manager' in a.role.lower()), self.agents[0])
        
        context = {}
        
        for task in self.tasks:
            # Manager assigns task to best agent
            assigned_agent = self._assign_task(task, manager)
            
            result = task.execute(agent=assigned_agent, context=context)
            self.results.append(result)
            context[task.task_id] = result
        
        self.status = "completed"
        return self.results
    
    def _assign_task(self, task: CrewTask, manager: Agent) -> Agent:
        """Manager assigns task to most suitable agent."""
        # Simple assignment based on role keywords
        task_desc = task.description.lower()
        
        for agent in self.agents:
            if agent == manager:
                continue
            
            role_keywords = agent.role.lower().split()
            if any(keyword in task_desc for keyword in role_keywords):
                return agent
        
        # Default to first non-manager agent
        return next((a for a in self.agents if a != manager), self.agents[0])
    
    def get_status(self) -> Dict:
        """Get crew execution status."""
        completed_tasks = sum(1 for t in self.tasks if t.status == "completed")
        failed_tasks = sum(1 for t in self.tasks if t.status == "failed")
        
        return {
            'crew_id': self.crew_id,
            'status': self.status,
            'total_agents': len(self.agents),
            'total_tasks': len(self.tasks),
            'completed_tasks': completed_tasks,
            'failed_tasks': failed_tasks,
            'agents': [a.to_dict() for a in self.agents],
            'tasks': [t.to_dict() for t in self.tasks]
        }


class MultiAgentCollaboration:
    """Collaboration patterns for multiple agents."""
    
    @staticmethod
    def debate(topic: str, agents: List[Agent], rounds: int = 3) -> List[Dict]:
        """Agents debate a topic for multiple rounds."""
        debate_history = []
        
        for round_num in range(rounds):
            for agent in agents:
                # Each agent responds to the topic and previous arguments
                context = {
                    'topic': topic,
                    'round': round_num + 1,
                    'previous_arguments': debate_history[-len(agents):] if debate_history else []
                }
                
                task = CrewTask(
                    description=f"Provide your perspective on: {topic}",
                    expected_output="A reasoned argument",
                    agent=agent
                )
                
                response = agent.execute_task(task, context)
                
                debate_history.append({
                    'round': round_num + 1,
                    'agent': agent.role,
                    'response': response
                })
        
        return debate_history
    
    @staticmethod
    def consensus(question: str, agents: List[Agent]) -> Dict:
        """Agents work towards consensus on a question."""
        responses = []
        
        # Each agent gives initial response
        for agent in agents:
            task = CrewTask(
                description=f"Answer: {question}",
                expected_output="Your answer with reasoning",
                agent=agent
            )
            response = agent.execute_task(task)
            responses.append({'agent': agent.role, 'response': response})
        
        # Synthesize consensus (simple majority or aggregation)
        return {
            'question': question,
            'responses': responses,
            'consensus': responses[0]['response']  # Simplified
        }
    
    @staticmethod
    def peer_review(content: str, author: Agent, reviewers: List[Agent]) -> Dict:
        """Peer review pattern where reviewers provide feedback."""
        # Author creates content
        creation_task = CrewTask(
            description=f"Create: {content}",
            expected_output="The created content",
            agent=author
        )
        created_content = author.execute_task(creation_task)
        
        # Reviewers provide feedback
        reviews = []
        for reviewer in reviewers:
            review_task = CrewTask(
                description=f"Review and provide feedback on: {created_content[:200]}",
                expected_output="Constructive feedback",
                agent=reviewer
            )
            feedback = reviewer.execute_task(review_task)
            reviews.append({'reviewer': reviewer.role, 'feedback': feedback})
        
        return {
            'content': created_content,
            'reviews': reviews
        }


def create_research_crew(topic: str, llm_fn: Optional[Callable] = None) -> Crew:
    """Create a research crew for investigating a topic."""
    # Define agents
    researcher = Agent(
        role="Senior Researcher",
        goal=f"Research and gather information about {topic}",
        backstory="Expert at finding and analyzing information",
        llm_fn=llm_fn
    )
    
    analyst = Agent(
        role="Data Analyst",
        goal=f"Analyze research findings about {topic}",
        backstory="Skilled at identifying patterns and insights",
        llm_fn=llm_fn
    )
    
    writer = Agent(
        role="Technical Writer",
        goal=f"Create a comprehensive report about {topic}",
        backstory="Excellent at synthesizing information into clear reports",
        llm_fn=llm_fn
    )
    
    # Define tasks
    research_task = CrewTask(
        description=f"Research {topic} and gather key information",
        expected_output="Comprehensive research findings",
        agent=researcher,
        priority=TaskPriority.HIGH
    )
    
    analysis_task = CrewTask(
        description="Analyze the research findings and identify key insights",
        expected_output="Analysis report with insights",
        agent=analyst,
        priority=TaskPriority.MEDIUM
    )
    analysis_task.add_dependency(research_task)
    
    writing_task = CrewTask(
        description="Write a comprehensive report based on research and analysis",
        expected_output="Final report",
        agent=writer,
        priority=TaskPriority.MEDIUM
    )
    writing_task.add_dependency(analysis_task)
    
    return Crew(
        agents=[researcher, analyst, writer],
        tasks=[research_task, analysis_task, writing_task],
        process="sequential"
    )


def create_development_crew(project: str, llm_fn: Optional[Callable] = None) -> Crew:
    """Create a software development crew."""
    manager = Agent(
        role="Project Manager",
        goal=f"Manage development of {project}",
        backstory="Experienced in coordinating development teams",
        llm_fn=llm_fn
    )
    
    developer = Agent(
        role="Senior Developer",
        goal=f"Implement {project}",
        backstory="Expert programmer with 10+ years experience",
        llm_fn=llm_fn
    )
    
    tester = Agent(
        role="QA Engineer",
        goal=f"Test {project}",
        backstory="Thorough tester who finds edge cases",
        llm_fn=llm_fn
    )
    
    # Tasks
    design_task = CrewTask(
        description=f"Design the architecture for {project}",
        expected_output="System design document",
        priority=TaskPriority.CRITICAL
    )
    
    implement_task = CrewTask(
        description="Implement the system based on design",
        expected_output="Working implementation",
        agent=developer,
        priority=TaskPriority.HIGH
    )
    implement_task.add_dependency(design_task)
    
    test_task = CrewTask(
        description="Test the implementation thoroughly",
        expected_output="Test report",
        agent=tester,
        priority=TaskPriority.HIGH
    )
    test_task.add_dependency(implement_task)
    
    return Crew(
        agents=[manager, developer, tester],
        tasks=[design_task, implement_task, test_task],
        process="hierarchical"
    )


__all__ = [
    'AgentRole',
    'TaskPriority',
    'Agent',
    'CrewTask',
    'Crew',
    'MultiAgentCollaboration',
    'create_research_crew',
    'create_development_crew'
]
