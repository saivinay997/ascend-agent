"""
State management for the Ascend workflow system.

This module defines the state structure and management functions
for the LangGraph workflow system.
"""

from typing import Any, Dict, List, Optional, TypedDict
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class AscendState:
    """
    State class for the Ascend workflow system.
    
    This class represents the complete state of a workflow execution,
    including student information, current task, agent results, and history.
    """
    
    # Core identification
    student_id: str
    current_task: str
    task_data: Dict[str, Any] = field(default_factory=dict)
    
    # Workflow tracking
    workflow_step: str = "coordinator"
    agent_results: Dict[str, Any] = field(default_factory=dict)
    workflow_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Optional fields for extended functionality
    session_id: Optional[str] = None
    priority: str = "normal"  # low, normal, high, critical
    timeout_seconds: int = 300  # 5 minutes default
    
    def update(self, **kwargs):
        """Update state with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def add_agent_result(self, agent_name: str, result: Dict[str, Any]):
        """Add a result from an agent."""
        self.agent_results[agent_name] = result
        self.updated_at = datetime.now()
    
    def add_workflow_step(self, step: str, task: str, success: bool, metadata: Dict[str, Any] = None):
        """Add a workflow step to history."""
        step_record = {
            "step": step,
            "task": task,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.workflow_history.append(step_record)
        self.updated_at = datetime.now()
    
    def get_agent_result(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get result from a specific agent."""
        return self.agent_results.get(agent_name)
    
    def get_last_workflow_step(self) -> Optional[Dict[str, Any]]:
        """Get the last workflow step from history."""
        if self.workflow_history:
            return self.workflow_history[-1]
        return None
    
    def is_complete(self) -> bool:
        """Check if the workflow is complete."""
        # This is a simplified check - in a real implementation,
        # you might have more sophisticated completion logic
        return len(self.workflow_history) > 0 and self.workflow_step == "coordinator"
    
    def has_error(self) -> bool:
        """Check if there are any errors in the workflow."""
        for result in self.agent_results.values():
            if isinstance(result, dict) and not result.get("success", True):
                return True
        return False
    
    def get_error_summary(self) -> List[str]:
        """Get a summary of errors in the workflow."""
        errors = []
        for agent_name, result in self.agent_results.items():
            if isinstance(result, dict) and not result.get("success", True):
                error_msg = result.get("error", "Unknown error")
                errors.append(f"{agent_name}: {error_msg}")
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "student_id": self.student_id,
            "current_task": self.current_task,
            "task_data": self.task_data,
            "workflow_step": self.workflow_step,
            "agent_results": self.agent_results,
            "workflow_history": self.workflow_history,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "session_id": self.session_id,
            "priority": self.priority,
            "timeout_seconds": self.timeout_seconds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AscendState':
        """Create state from dictionary."""
        # Convert datetime strings back to datetime objects
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        
        return cls(**data)


class StateManager:
    """
    Manager class for handling state operations in the Ascend system.
    
    This class provides utilities for state creation, validation, and management.
    """
    
    @staticmethod
    def create_initial_state(
        student_id: str,
        task: str,
        task_data: Dict[str, Any],
        priority: str = "normal"
    ) -> AscendState:
        """
        Create an initial state for a new workflow.
        
        Args:
            student_id: Student identifier
            task: Task to perform
            task_data: Data for the task
            priority: Priority level
            
        Returns:
            Initial AscendState
        """
        return AscendState(
            student_id=student_id,
            current_task=task,
            task_data=task_data,
            priority=priority,
            workflow_step="coordinator"
        )
    
    @staticmethod
    def validate_state(state: AscendState) -> List[str]:
        """
        Validate a state object.
        
        Args:
            state: State to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not state.student_id:
            errors.append("student_id is required")
        
        if not state.current_task:
            errors.append("current_task is required")
        
        if state.priority not in ["low", "normal", "high", "critical"]:
            errors.append("priority must be one of: low, normal, high, critical")
        
        if state.timeout_seconds <= 0:
            errors.append("timeout_seconds must be positive")
        
        return errors
    
    @staticmethod
    def is_state_expired(state: AscendState) -> bool:
        """
        Check if a state has expired based on timeout.
        
        Args:
            state: State to check
            
        Returns:
            True if expired, False otherwise
        """
        elapsed = datetime.now() - state.created_at
        return elapsed.total_seconds() > state.timeout_seconds
    
    @staticmethod
    def get_state_summary(state: AscendState) -> Dict[str, Any]:
        """
        Get a summary of the current state.
        
        Args:
            state: State to summarize
            
        Returns:
            Summary dictionary
        """
        return {
            "student_id": state.student_id,
            "current_task": state.current_task,
            "workflow_step": state.workflow_step,
            "agents_completed": len(state.agent_results),
            "steps_completed": len(state.workflow_history),
            "has_errors": state.has_error(),
            "is_complete": state.is_complete(),
            "is_expired": StateManager.is_state_expired(state),
            "created_at": state.created_at.isoformat(),
            "updated_at": state.updated_at.isoformat()
        }
    
    @staticmethod
    def merge_states(base_state: AscendState, update_state: AscendState) -> AscendState:
        """
        Merge two states, with update_state taking precedence.
        
        Args:
            base_state: Base state
            update_state: State with updates
            
        Returns:
            Merged state
        """
        # Create a copy of the base state
        merged = AscendState(
            student_id=update_state.student_id or base_state.student_id,
            current_task=update_state.current_task or base_state.current_task,
            task_data={**base_state.task_data, **update_state.task_data},
            workflow_step=update_state.workflow_step or base_state.workflow_step,
            agent_results={**base_state.agent_results, **update_state.agent_results},
            workflow_history=base_state.workflow_history + update_state.workflow_history,
            created_at=base_state.created_at,
            updated_at=datetime.now(),
            session_id=update_state.session_id or base_state.session_id,
            priority=update_state.priority or base_state.priority,
            timeout_seconds=update_state.timeout_seconds or base_state.timeout_seconds
        )
        
        return merged


# Type definitions for type hints
class AgentResult(TypedDict):
    """Type definition for agent results."""
    content: str
    metadata: Dict[str, Any]
    success: bool
    error: Optional[str]
    execution_time: Optional[float]


class WorkflowStep(TypedDict):
    """Type definition for workflow steps."""
    step: str
    task: str
    success: bool
    timestamp: str
    metadata: Dict[str, Any]


class StateSummary(TypedDict):
    """Type definition for state summaries."""
    student_id: str
    current_task: str
    workflow_step: str
    agents_completed: int
    steps_completed: int
    has_errors: bool
    is_complete: bool
    is_expired: bool
    created_at: str
    updated_at: str
