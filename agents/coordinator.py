"""
Coordinator Agent for the Ascend system.

The Coordinator Agent serves as the central orchestrator, managing workflow
and ensuring seamless communication between all other agents.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse
from config.logging_config import LoggerMixin


class CoordinatorAgent(BaseAgent):
    """
    Coordinator Agent - Central orchestrator for the Ascend system.
    
    Responsibilities:
    - Manage workflow execution
    - Coordinate communication between agents
    - Handle task delegation and routing
    - Monitor system performance
    - Manage state transitions
    """
    
    def __init__(self, **kwargs):
        """Initialize the Coordinator Agent."""
        super().__init__(
            name="Coordinator",
            description="Central orchestrator managing workflow and agent communication",
            **kwargs
        )
        self.active_workflows = {}
        self.agent_registry = {}
        self.workflow_history = []
        
    async def process_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a coordination task.
        
        Args:
            task: Task to process
            context: Additional context
            
        Returns:
            AgentResponse with the result
        """
        task_type = task.get("type", "unknown")
        
        if task_type == "workflow_execution":
            return await self._execute_workflow(task, context)
        elif task_type == "agent_coordination":
            return await self._coordinate_agents(task, context)
        elif task_type == "state_management":
            return await self._manage_state(task, context)
        elif task_type == "performance_monitoring":
            return await self._monitor_performance(task, context)
        else:
            return await self._handle_unknown_task(task, context)
    
    async def _execute_workflow(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Execute a workflow with multiple agents."""
        workflow_id = task.get("workflow_id")
        workflow_steps = task.get("steps", [])
        
        self.logger.info(
            "Executing workflow",
            workflow_id=workflow_id,
            steps_count=len(workflow_steps)
        )
        
        try:
            results = []
            current_state = context or {}
            
            for step in workflow_steps:
                step_result = await self._execute_workflow_step(step, current_state)
                results.append(step_result)
                
                # Update state with step result
                if step_result.success:
                    current_state.update(step_result.metadata.get("state_updates", {}))
                
                # Check for workflow termination conditions
                if step.get("terminate_on_failure") and not step_result.success:
                    break
            
            # Compile final result
            success = all(result.success for result in results)
            final_result = self._compile_workflow_results(results, current_state)
            
            # Record workflow execution
            self._record_workflow_execution(workflow_id, success, results)
            
            return AgentResponse(
                content=final_result,
                metadata={
                    "workflow_id": workflow_id,
                    "steps_executed": len(results),
                    "success": success,
                    "final_state": current_state
                },
                success=success
            )
            
        except Exception as e:
            self.logger.error(
                "Workflow execution failed",
                workflow_id=workflow_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"workflow_id": workflow_id},
                success=False,
                error=str(e)
            )
    
    async def _execute_workflow_step(
        self, 
        step: Dict[str, Any], 
        current_state: Dict[str, Any]
    ) -> AgentResponse:
        """Execute a single workflow step."""
        agent_name = step.get("agent")
        step_type = step.get("type")
        step_data = step.get("data", {})
        
        if agent_name not in self.agent_registry:
            return AgentResponse(
                content="",
                metadata={"step": step},
                success=False,
                error=f"Agent {agent_name} not found in registry"
            )
        
        agent = self.agent_registry[agent_name]
        
        # Prepare task for the agent
        task = {
            "type": step_type,
            "data": step_data,
            "workflow_context": current_state
        }
        
        # Execute the agent task
        return await agent.process_task(task, current_state)
    
    async def _coordinate_agents(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Coordinate communication between multiple agents."""
        coordination_type = task.get("coordination_type")
        
        if coordination_type == "register_agent":
            return await self._register_agent(task, context)
        elif coordination_type == "agent_communication":
            return await self._facilitate_agent_communication(task, context)
        elif coordination_type == "load_balancing":
            return await self._balance_agent_load(task, context)
        else:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"Unknown coordination type: {coordination_type}"
            )
    
    async def _register_agent(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Register an agent in the coordinator's registry."""
        agent_name = task.get("agent_name")
        agent_instance = task.get("agent_instance")
        
        if not agent_name or not agent_instance:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Agent name and instance are required"
            )
        
        self.agent_registry[agent_name] = agent_instance
        
        self.logger.info(
            "Agent registered",
            agent_name=agent_name,
            registry_size=len(self.agent_registry)
        )
        
        return AgentResponse(
            content=f"Agent {agent_name} registered successfully",
            metadata={
                "agent_name": agent_name,
                "registry_size": len(self.agent_registry)
            },
            success=True
        )
    
    async def _facilitate_agent_communication(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Facilitate communication between agents."""
        source_agent = task.get("source_agent")
        target_agent = task.get("target_agent")
        message = task.get("message")
        
        if not all([source_agent, target_agent, message]):
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Source agent, target agent, and message are required"
            )
        
        if target_agent not in self.agent_registry:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"Target agent {target_agent} not found"
            )
        
        # Forward message to target agent
        target_agent_instance = self.agent_registry[target_agent]
        response = await target_agent_instance.process_message(message, context)
        
        return AgentResponse(
            content=f"Message forwarded from {source_agent} to {target_agent}",
            metadata={
                "source_agent": source_agent,
                "target_agent": target_agent,
                "response": response.content if response.success else response.error
            },
            success=response.success,
            error=response.error
        )
    
    async def _balance_agent_load(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Balance load across available agents."""
        agent_type = task.get("agent_type")
        task_data = task.get("task_data")
        
        # Find available agents of the specified type
        available_agents = [
            (name, agent) for name, agent in self.agent_registry.items()
            if agent_type in agent.get_capabilities()
        ]
        
        if not available_agents:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"No agents available for type: {agent_type}"
            )
        
        # Simple round-robin load balancing
        # In a real implementation, you might consider agent load, performance, etc.
        selected_agent_name, selected_agent = available_agents[0]
        
        # Execute task on selected agent
        result = await selected_agent.process_task(task_data, context)
        
        return AgentResponse(
            content=f"Task assigned to {selected_agent_name}",
            metadata={
                "assigned_agent": selected_agent_name,
                "agent_type": agent_type,
                "result": result.content if result.success else result.error
            },
            success=result.success,
            error=result.error
        )
    
    async def _manage_state(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Manage system state and transitions."""
        state_action = task.get("action")
        
        if state_action == "save_state":
            return await self._save_state(task, context)
        elif state_action == "load_state":
            return await self._load_state(task, context)
        elif state_action == "update_state":
            return await self._update_state(task, context)
        else:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"Unknown state action: {state_action}"
            )
    
    async def _save_state(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Save current system state."""
        state_key = task.get("state_key")
        state_data = task.get("state_data", context or {})
        
        # In a real implementation, this would save to a persistent store
        self.active_workflows[state_key] = {
            "data": state_data,
            "timestamp": datetime.now().isoformat()
        }
        
        return AgentResponse(
            content=f"State saved with key: {state_key}",
            metadata={"state_key": state_key, "timestamp": datetime.now().isoformat()},
            success=True
        )
    
    async def _load_state(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Load system state."""
        state_key = task.get("state_key")
        
        if state_key not in self.active_workflows:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"State not found for key: {state_key}"
            )
        
        state_data = self.active_workflows[state_key]
        
        return AgentResponse(
            content=f"State loaded for key: {state_key}",
            metadata={"state_key": state_key, "state_data": state_data},
            success=True
        )
    
    async def _update_state(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Update system state."""
        state_key = task.get("state_key")
        updates = task.get("updates", {})
        
        if state_key not in self.active_workflows:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"State not found for key: {state_key}"
            )
        
        # Update the state
        self.active_workflows[state_key]["data"].update(updates)
        self.active_workflows[state_key]["timestamp"] = datetime.now().isoformat()
        
        return AgentResponse(
            content=f"State updated for key: {state_key}",
            metadata={"state_key": state_key, "updates": updates},
            success=True
        )
    
    async def _monitor_performance(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Monitor system performance and health."""
        monitoring_type = task.get("monitoring_type", "health_check")
        
        if monitoring_type == "health_check":
            return await self._perform_health_check()
        elif monitoring_type == "performance_metrics":
            return await self._collect_performance_metrics()
        else:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"Unknown monitoring type: {monitoring_type}"
            )
    
    async def _perform_health_check(self) -> AgentResponse:
        """Perform health check on all registered agents."""
        health_results = {}
        
        for agent_name, agent in self.agent_registry.items():
            try:
                health_status = await agent.health_check()
                health_results[agent_name] = health_status
            except Exception as e:
                health_results[agent_name] = False
                self.logger.error(
                    "Health check failed for agent",
                    agent_name=agent_name,
                    error=str(e)
                )
        
        overall_health = all(health_results.values())
        
        return AgentResponse(
            content="Health check completed",
            metadata={
                "overall_health": overall_health,
                "agent_health": health_results
            },
            success=overall_health
        )
    
    async def _collect_performance_metrics(self) -> AgentResponse:
        """Collect performance metrics from all agents."""
        metrics = {
            "total_agents": len(self.agent_registry),
            "active_workflows": len(self.active_workflows),
            "workflow_history_size": len(self.workflow_history),
            "agent_status": {}
        }
        
        for agent_name, agent in self.agent_registry.items():
            metrics["agent_status"][agent_name] = agent.get_status()
        
        return AgentResponse(
            content="Performance metrics collected",
            metadata={"metrics": metrics},
            success=True
        )
    
    async def _handle_unknown_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Handle unknown task types."""
        task_type = task.get("type", "unknown")
        
        self.logger.warning(
            "Unknown task type received",
            task_type=task_type,
            task=task
        )
        
        return AgentResponse(
            content=f"Unknown task type: {task_type}",
            metadata={"task": task},
            success=False,
            error=f"Unsupported task type: {task_type}"
        )
    
    def _compile_workflow_results(
        self, 
        results: List[AgentResponse], 
        final_state: Dict[str, Any]
    ) -> str:
        """Compile workflow results into a summary."""
        successful_steps = sum(1 for result in results if result.success)
        total_steps = len(results)
        
        summary = f"Workflow completed: {successful_steps}/{total_steps} steps successful"
        
        if successful_steps == total_steps:
            summary += "\nAll steps completed successfully."
        else:
            failed_steps = [i for i, result in enumerate(results) if not result.success]
            summary += f"\nFailed steps: {failed_steps}"
        
        return summary
    
    def _record_workflow_execution(
        self, 
        workflow_id: str, 
        success: bool, 
        results: List[AgentResponse]
    ):
        """Record workflow execution in history."""
        execution_record = {
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "steps_count": len(results),
            "successful_steps": sum(1 for result in results if result.success)
        }
        
        self.workflow_history.append(execution_record)
        
        # Keep only recent history (last 100 executions)
        if len(self.workflow_history) > 100:
            self.workflow_history = self.workflow_history[-100:]
    
    def get_capabilities(self) -> List[str]:
        """Get the capabilities of the Coordinator Agent."""
        return [
            "Workflow orchestration and execution",
            "Agent coordination and communication",
            "State management and persistence",
            "Performance monitoring and health checks",
            "Load balancing across agents",
            "Task delegation and routing"
        ]
    
    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self.agent_registry.keys())
    
    def get_workflow_history(self) -> List[Dict[str, Any]]:
        """Get workflow execution history."""
        return self.workflow_history.copy()
