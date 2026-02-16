"""
LLM Recipe functions for LlamaIndex and LangChain patterns.

Pure Python implementations of common LLM patterns and utilities.
Can be extended with actual LlamaIndex/LangChain when libraries are installed.
"""

import json
from typing import List, Dict, Any, Optional, Callable, Union
from collections import deque


class PromptTemplate:
    """Simple prompt template with variable substitution."""
    
    def __init__(self, template: str, input_variables: Optional[List[str]] = None):
        self.template = template
        self.input_variables = input_variables or []
    
    def format(self, **kwargs) -> str:
        """Format template with variables."""
        return self.template.format(**kwargs)
    
    def partial(self, **kwargs) -> 'PromptTemplate':
        """Create a new template with some variables filled in."""
        new_template = self.template
        for key, value in kwargs.items():
            new_template = new_template.replace(f"{{{key}}}", str(value))
        
        remaining_vars = [v for v in self.input_variables if v not in kwargs]
        return PromptTemplate(new_template, remaining_vars)


class ConversationMemory:
    """Memory for conversation history."""
    
    def __init__(self, max_messages: int = 10):
        self.messages = deque(maxlen=max_messages)
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str):
        """Add a message to memory."""
        self.messages.append({'role': role, 'content': content})
    
    def add_user_message(self, content: str):
        """Add a user message."""
        self.add_message('user', content)
    
    def add_assistant_message(self, content: str):
        """Add an assistant message."""
        self.add_message('assistant', content)
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages."""
        return list(self.messages)
    
    def get_context(self) -> str:
        """Get conversation as formatted string."""
        return "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in self.messages
        ])
    
    def clear(self):
        """Clear all messages."""
        self.messages.clear()
    
    def save(self, filepath: str):
        """Save conversation to file."""
        with open(filepath, 'w') as f:
            json.dump(list(self.messages), f, indent=2)
    
    def load(self, filepath: str):
        """Load conversation from file."""
        with open(filepath, 'r') as f:
            messages = json.load(f)
        self.messages = deque(messages, maxlen=self.max_messages)


class BufferMemory(ConversationMemory):
    """Simple buffer memory that keeps last N messages."""
    pass


class SummaryMemory:
    """Memory that summarizes old conversations."""
    
    def __init__(self, max_messages: int = 10, summarize_fn: Optional[Callable] = None):
        self.recent_messages = deque(maxlen=max_messages)
        self.summary = ""
        self.summarize_fn = summarize_fn or self._default_summarize
    
    def add_message(self, role: str, content: str):
        """Add a message, summarizing old ones if needed."""
        self.recent_messages.append({'role': role, 'content': content})
        
        # If buffer is full, summarize oldest messages
        if len(self.recent_messages) == self.recent_messages.maxlen:
            old_messages = list(self.recent_messages)[:5]
            self.summary = self.summarize_fn(old_messages, self.summary)
    
    def _default_summarize(self, messages: List[Dict], current_summary: str) -> str:
        """Default summarization (simple concatenation)."""
        new_content = " ".join([msg['content'][:100] for msg in messages])
        if current_summary:
            return f"{current_summary} | {new_content[:200]}"
        return new_content[:200]
    
    def get_context(self) -> str:
        """Get summary + recent messages."""
        context = []
        if self.summary:
            context.append(f"SUMMARY: {self.summary}")
        
        context.extend([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in self.recent_messages
        ])
        
        return "\n".join(context)


class LLMChain:
    """Chain that combines a prompt template with an LLM."""
    
    def __init__(self, prompt: PromptTemplate, llm_fn: Optional[Callable] = None):
        self.prompt = prompt
        self.llm_fn = llm_fn or self._mock_llm
    
    def _mock_llm(self, prompt: str) -> str:
        """Mock LLM for testing."""
        return f"Mock response to: {prompt[:100]}"
    
    def run(self, **kwargs) -> str:
        """Run the chain."""
        formatted_prompt = self.prompt.format(**kwargs)
        return self.llm_fn(formatted_prompt)
    
    def __call__(self, **kwargs) -> str:
        """Make chain callable."""
        return self.run(**kwargs)


class SequentialChain:
    """Chain multiple LLM chains together."""
    
    def __init__(self, chains: List[LLMChain]):
        self.chains = chains
    
    def run(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Run all chains in sequence."""
        current_input = initial_input.copy()
        
        for chain in self.chains:
            output = chain.run(**current_input)
            current_input['previous_output'] = output
        
        return {'output': output, 'intermediate_steps': current_input}


class RouterChain:
    """Route inputs to different chains based on conditions."""
    
    def __init__(self, routes: Dict[str, LLMChain], default_chain: Optional[LLMChain] = None):
        self.routes = routes
        self.default_chain = default_chain
    
    def route(self, input_data: Dict[str, Any]) -> str:
        """Determine which route to take."""
        # Simple keyword-based routing
        input_text = str(input_data.get('input', '')).lower()
        
        for route_key in self.routes.keys():
            if route_key.lower() in input_text:
                return route_key
        
        return 'default'
    
    def run(self, **kwargs) -> str:
        """Route and run appropriate chain."""
        route_key = self.route(kwargs)
        
        if route_key in self.routes:
            return self.routes[route_key].run(**kwargs)
        elif self.default_chain:
            return self.default_chain.run(**kwargs)
        else:
            return f"No route found for input"


class Agent:
    """Simple agent that can use tools."""
    
    def __init__(self, tools: List[Dict[str, Any]], llm_fn: Optional[Callable] = None):
        self.tools = {tool['name']: tool for tool in tools}
        self.llm_fn = llm_fn or self._mock_llm
        self.max_iterations = 5
    
    def _mock_llm(self, prompt: str) -> str:
        """Mock LLM response."""
        return "Use: calculator(5 + 3)"
    
    def _parse_action(self, llm_output: str) -> Optional[Dict[str, Any]]:
        """Parse LLM output to extract tool and input."""
        # Simple parsing: "Use: tool_name(input)"
        if "Use:" in llm_output:
            parts = llm_output.split("Use:")[1].strip()
            if "(" in parts and ")" in parts:
                tool_name = parts.split("(")[0].strip()
                tool_input = parts.split("(")[1].split(")")[0].strip()
                return {'tool': tool_name, 'input': tool_input}
        return None
    
    def run(self, task: str) -> str:
        """Run the agent on a task."""
        context = f"Task: {task}\nAvailable tools: {', '.join(self.tools.keys())}\n"
        
        for i in range(self.max_iterations):
            # Get LLM decision
            llm_output = self.llm_fn(context)
            
            # Parse action
            action = self._parse_action(llm_output)
            
            if not action:
                return llm_output
            
            # Execute tool
            tool_name = action['tool']
            if tool_name in self.tools:
                tool_fn = self.tools[tool_name]['function']
                result = tool_fn(action['input'])
                context += f"\nAction: {tool_name}({action['input']})\nResult: {result}\n"
            else:
                return f"Tool {tool_name} not found"
        
        return "Max iterations reached"


def create_rag_prompt(query: str, context: str, instruction: str = "") -> str:
    """Create a RAG prompt combining query and retrieved context."""
    template = """Use the following context to answer the question.

Context:
{context}

Question: {query}

{instruction}

Answer:"""
    
    return template.format(query=query, context=context, instruction=instruction)


def create_few_shot_prompt(examples: List[Dict[str, str]], query: str) -> str:
    """Create a few-shot learning prompt."""
    prompt_parts = ["Here are some examples:\n"]
    
    for i, example in enumerate(examples):
        prompt_parts.append(f"Example {i+1}:")
        prompt_parts.append(f"Input: {example['input']}")
        prompt_parts.append(f"Output: {example['output']}\n")
    
    prompt_parts.append(f"Now, for this input:\nInput: {query}")
    prompt_parts.append("Output:")
    
    return "\n".join(prompt_parts)


def create_cot_prompt(query: str) -> str:
    """Create a Chain-of-Thought prompt."""
    return f"""{query}

Let's think step by step:
1."""


def create_react_prompt(query: str, tools: List[str]) -> str:
    """Create a ReAct (Reasoning + Acting) prompt."""
    tools_str = "\n".join([f"- {tool}" for tool in tools])
    
    return f"""You can use these tools:
{tools_str}

Question: {query}

Thought: Let me think about what I need to do.
Action:"""


def parse_json_response(text: str) -> Optional[Dict]:
    """Extract and parse JSON from LLM response."""
    # Find JSON in response
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1:
        json_str = text[start:end+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None
    
    return None


def extract_code_blocks(text: str, language: str = "") -> List[str]:
    """Extract code blocks from markdown-formatted text."""
    import re
    
    if language:
        pattern = f"```{language}\\n(.*?)```"
    else:
        pattern = r"```(?:\w+)?\n(.*?)```"
    
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


def token_count_estimate(text: str) -> int:
    """Estimate token count (rough approximation)."""
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4


def truncate_to_tokens(text: str, max_tokens: int) -> str:
    """Truncate text to approximate token limit."""
    max_chars = max_tokens * 4
    if len(text) <= max_chars:
        return text
    
    return text[:max_chars] + "..."


class OutputParser:
    """Parse and validate LLM outputs."""
    
    def __init__(self, expected_format: str = "text"):
        self.expected_format = expected_format
    
    def parse(self, text: str) -> Any:
        """Parse output based on expected format."""
        if self.expected_format == "json":
            return parse_json_response(text)
        elif self.expected_format == "list":
            return self._parse_list(text)
        elif self.expected_format == "bool":
            return self._parse_bool(text)
        else:
            return text.strip()
    
    def _parse_list(self, text: str) -> List[str]:
        """Parse text as a list."""
        lines = text.strip().split('\n')
        items = []
        for line in lines:
            line = line.strip()
            # Remove bullet points and numbers
            line = line.lstrip('- * •').lstrip('0123456789.').strip()
            if line:
                items.append(line)
        return items
    
    def _parse_bool(self, text: str) -> bool:
        """Parse text as boolean."""
        text = text.lower().strip()
        return text in ['yes', 'true', '1', 'correct', 'right']


class RetryWithFeedback:
    """Retry LLM calls with feedback on failures."""
    
    def __init__(self, llm_fn: Callable, max_retries: int = 3):
        self.llm_fn = llm_fn
        self.max_retries = max_retries
    
    def run(self, prompt: str, validator: Optional[Callable] = None) -> str:
        """Run with retries and validation."""
        validator = validator or (lambda x: True)
        
        for attempt in range(self.max_retries):
            response = self.llm_fn(prompt)
            
            if validator(response):
                return response
            
            # Add feedback for retry
            feedback = f"\n\nThe previous response was invalid. Please try again."
            prompt = prompt + feedback
        
        return response  # Return last attempt even if invalid


class LLMCache:
    """Cache LLM responses to avoid redundant calls."""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, prompt: str) -> Optional[str]:
        """Get cached response."""
        return self.cache.get(prompt)
    
    def set(self, prompt: str, response: str):
        """Cache a response."""
        self.cache[prompt] = response
    
    def clear(self):
        """Clear cache."""
        self.cache.clear()
    
    def wrap(self, llm_fn: Callable) -> Callable:
        """Wrap an LLM function with caching."""
        def cached_llm_fn(prompt: str) -> str:
            cached = self.get(prompt)
            if cached is not None:
                return cached
            
            response = llm_fn(prompt)
            self.set(prompt, response)
            return response
        
        return cached_llm_fn


def batch_prompts(prompts: List[str], batch_size: int = 5) -> List[List[str]]:
    """Batch prompts for efficient processing."""
    batches = []
    for i in range(0, len(prompts), batch_size):
        batches.append(prompts[i:i+batch_size])
    return batches


def create_system_message(role: str, constraints: Optional[List[str]] = None) -> str:
    """Create a system message for chat models."""
    message = f"You are a helpful {role}."
    
    if constraints:
        message += "\n\nConstraints:"
        for constraint in constraints:
            message += f"\n- {constraint}"
    
    return message


def format_chat_messages(messages: List[Dict[str, str]], format_type: str = "openai") -> Any:
    """Format messages for different chat APIs."""
    if format_type == "openai":
        return messages
    elif format_type == "anthropic":
        # Convert to Anthropic format
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    elif format_type == "text":
        # Convert to plain text
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    
    return messages


__all__ = [
    'PromptTemplate',
    'ConversationMemory',
    'BufferMemory',
    'SummaryMemory',
    'LLMChain',
    'SequentialChain',
    'RouterChain',
    'Agent',
    'create_rag_prompt',
    'create_few_shot_prompt',
    'create_cot_prompt',
    'create_react_prompt',
    'parse_json_response',
    'extract_code_blocks',
    'token_count_estimate',
    'truncate_to_tokens',
    'OutputParser',
    'RetryWithFeedback',
    'LLMCache',
    'batch_prompts',
    'create_system_message',
    'format_chat_messages'
]
