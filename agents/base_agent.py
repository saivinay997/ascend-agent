"""
Base agent class for the Ascend multi-agent system.
"""

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings
from config.logging_config import LoggerMixin, PerformanceLogger


@dataclass
class AgentResponse:
    """Response from an agent."""
    content: str
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str] = None
    execution_time: Optional[float] = None


class BaseAgent(ABC, LoggerMixin):
    """
    Base class for all agents in the Ascend system.
    
    Provides common functionality for:
    - LLM integration
    - Message handling
    - Performance monitoring
    - Error handling
    - Retry logic
    """
    
    def __init__(self, name: str, description: str, **kwargs):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            description: Agent description
            **kwargs: Additional configuration
        """
        self.name = name
        self.description = description
        self.llm = self._initialize_llm()
        self.performance_logger = PerformanceLogger(f"agent.{name}")
        self.max_retries = kwargs.get('max_retries', settings.AGENT_MAX_RETRIES)
        self.retry_delay = kwargs.get('retry_delay', settings.AGENT_RETRY_DELAY)
        self.timeout = kwargs.get('timeout', settings.AGENT_TIMEOUT)
        
        self.logger.info(
            "Agent initialized",
            agent_name=name,
            description=description,
            max_retries=self.max_retries,
            timeout=self.timeout
        )
    
    def _initialize_llm(self) -> ChatGoogleGenerativeAI:
        """Initialize the language model based on configuration."""
        if settings.has_gemini_config:
            return ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
                google_api_key=settings.GOOGLE_API_KEY
            )
        else:
            raise ValueError("No LLM configuration found. Please configure Google API key for Gemini.")
    
    async def process_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Process a message and return a response.
        
        Args:
            message: Input message
            context: Additional context
            **kwargs: Additional parameters
            
        Returns:
            AgentResponse with the result
        """
        start_time = time.time()
        
        try:
            # Prepare the message with context
            prepared_message = self._prepare_message(message, context, **kwargs)
            
            # Execute with retry logic
            for attempt in range(self.max_retries + 1):
                try:
                    result = await self._execute_with_timeout(prepared_message, **kwargs)
                    
                    execution_time = time.time() - start_time
                    self.performance_logger.log_timing(
                        "message_processing",
                        execution_time,
                        agent=self.name,
                        attempt=attempt + 1
                    )
                    
                    return AgentResponse(
                        content=result,
                        metadata={
                            "agent": self.name,
                            "attempt": attempt + 1,
                            "context": context
                        },
                        success=True,
                        execution_time=execution_time
                    )
                    
                except asyncio.TimeoutError:
                    if attempt == self.max_retries:
                        raise
                    self.logger.warning(
                        "Agent timeout, retrying",
                        agent=self.name,
                        attempt=attempt + 1,
                        timeout=self.timeout
                    )
                    await asyncio.sleep(self.retry_delay)
                    
                except Exception as e:
                    if attempt == self.max_retries:
                        raise
                    self.logger.warning(
                        "Agent error, retrying",
                        agent=self.name,
                        attempt=attempt + 1,
                        error=str(e)
                    )
                    await asyncio.sleep(self.retry_delay)
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.performance_logger.log_error(
                "message_processing",
                e,
                agent=self.name,
                execution_time=execution_time
            )
            
            return AgentResponse(
                content="",
                metadata={"agent": self.name, "context": context},
                success=False,
                error=str(e),
                execution_time=execution_time
            )
    
    def _prepare_message(
        self, 
        message: str, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> List[BaseMessage]:
        """
        Prepare the message for processing.
        
        Args:
            message: Input message
            context: Additional context
            **kwargs: Additional parameters
            
        Returns:
            List of messages for the LLM
        """
        messages = []
        
        # Add system message with agent description
        system_message = self._create_system_message(context, **kwargs)
        if system_message:
            messages.append(system_message)
        
        # Add context if provided
        if context:
            context_message = self._create_context_message(context)
            if context_message:
                messages.append(context_message)
        
        # Add the main message
        messages.append(HumanMessage(content=message))
        
        return messages
    
    def _create_system_message(
        self, 
        context: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Optional[BaseMessage]:
        """
        Create the system message for this agent.
        
        Args:
            context: Additional context
            **kwargs: Additional parameters
            
        Returns:
            System message or None
        """
        system_prompt = f"""You are {self.name}, {self.description}.

Your role is to assist students with their academic needs by providing personalized support and guidance.

Please be helpful, accurate, and supportive in your responses."""
        
        return AIMessage(content=system_prompt)
    
    def _create_context_message(self, context: Dict[str, Any]) -> Optional[BaseMessage]:
        """
        Create a context message from the provided context.
        
        Args:
            context: Context dictionary
            
        Returns:
            Context message or None
        """
        if not context:
            return None
        
        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        return HumanMessage(content=f"Context:\n{context_str}")
    
    async def _execute_with_timeout(
        self, 
        messages: List[BaseMessage], 
        **kwargs
    ) -> str:
        """
        Execute the LLM call with timeout.
        
        Args:
            messages: List of messages to send to LLM
            **kwargs: Additional parameters
            
        Returns:
            LLM response content
        """
        try:
            response = await asyncio.wait_for(
                self.llm.ainvoke(messages),
                timeout=self.timeout
            )
            return response.content
        except asyncio.TimeoutError:
            raise
        except Exception as e:
            self.logger.error(
                "LLM execution failed",
                agent=self.name,
                error=str(e),
                error_type=type(e).__name__
            )
            raise
    
    @abstractmethod
    async def process_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a specific task for this agent.
        
        Args:
            task: Task to process
            context: Additional context
            
        Returns:
            AgentResponse with the result
        """
        pass
    
    def get_capabilities(self) -> List[str]:
        """
        Get the capabilities of this agent.
        
        Returns:
            List of capability descriptions
        """
        return [self.description]
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of this agent.
        
        Returns:
            Status dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "status": "active",
            "llm_provider": "Gemini",
            "max_retries": self.max_retries,
            "timeout": self.timeout
        }
    
    async def health_check(self) -> bool:
        """
        Perform a health check on this agent.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            # Simple test message to verify LLM connectivity
            test_message = "Hello, this is a health check."
            response = await self.process_message(test_message)
            return response.success
        except Exception as e:
            self.logger.error(
                "Health check failed",
                agent=self.name,
                error=str(e)
            )
            return False


class SimpleAgent(BaseAgent):
    """Simple concrete implementation of BaseAgent for basic LLM interactions."""
    
    async def process_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a task by sending it as a message to the LLM.
        
        Args:
            task: Task to process
            context: Additional context
            
        Returns:
            AgentResponse with the result
        """
        try:
            # Convert task to a simple message
            if isinstance(task, dict):
                message = str(task)
            else:
                message = str(task)
            
            # Use the existing process_message method
            return await self.process_message(message, context)
            
        except Exception as e:
            return AgentResponse(
                content="",
                metadata={"agent": self.name, "task": task},
                success=False,
                error=str(e)
            )
