"""
Main workflow for the Ascend system using LangGraph.

This module implements the core workflow that orchestrates the multi-agent system,
managing state transitions and coordinating agent activities.
"""

import asyncio
from typing import Any, Dict, List, Optional, TypedDict, Annotated
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langgraph.checkpoint.memory import MemorySaver

from agents.coordinator import CoordinatorAgent
from agents.planner import PlannerAgent
from agents.notewriter import NotewriterAgent
from agents.advisor import AdvisorAgent
from workflows.state_manager import AscendState
from config.logging_config import LoggerMixin


class AscendWorkflow(LoggerMixin):
    """
    Main workflow orchestrator for the Ascend system.
    
    This class manages the LangGraph workflow that coordinates all agents
    and handles the complete student support lifecycle.
    """
    
    def __init__(self, services: Optional[Dict[str, Any]] = None):
        """
        Initialize the Ascend workflow.
        
        Args:
            services: Dictionary of service instances
        """
        self.services = services or {}
        self.agents = {}
        self.workflow_graph = None
        self.tool_executor = None
        self.checkpointer = None
        
        self.logger.info("Initializing Ascend workflow")
    
    async def initialize(self):
        """Initialize the workflow and all agents."""
        try:
            # Initialize agents
            await self._initialize_agents()
            
            # Create workflow graph
            self._create_workflow_graph()
            
            # Initialize tool executor
            self._initialize_tool_executor()
            
            # Initialize checkpointer
            self._initialize_checkpointer()
            
            self.logger.info("Ascend workflow initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize workflow: {e}")
            raise
    
    async def _initialize_agents(self):
        """Initialize all agents in the system."""
        # Initialize Coordinator Agent
        self.agents['coordinator'] = CoordinatorAgent()
        
        # Initialize Planner Agent
        self.agents['planner'] = PlannerAgent()
        
        # Initialize Notewriter Agent
        self.agents['notewriter'] = NotewriterAgent()
        
        # Initialize Advisor Agent
        self.agents['advisor'] = AdvisorAgent()
        
        # Register agents with coordinator
        for name, agent in self.agents.items():
            await self.agents['coordinator'].process_task({
                "type": "agent_coordination",
                "coordination_type": "register_agent",
                "agent_name": name,
                "agent_instance": agent
            })
        
        self.logger.info(f"Initialized {len(self.agents)} agents")
    
    def _create_workflow_graph(self):
        """Create the LangGraph workflow graph."""
        # Create state graph
        workflow = StateGraph(AscendState)
        
        # Add nodes for each agent
        workflow.add_node("coordinator", self._coordinator_node)
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("notewriter", self._notewriter_node)
        workflow.add_node("advisor", self._advisor_node)
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "coordinator",
            self._route_from_coordinator,
            {
                "planner": "planner",
                "notewriter": "notewriter",
                "advisor": "advisor",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "planner",
            self._route_from_planner,
            {
                "coordinator": "coordinator",
                "notewriter": "notewriter",
                "advisor": "advisor",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "notewriter",
            self._route_from_notewriter,
            {
                "coordinator": "coordinator",
                "planner": "planner",
                "advisor": "advisor",
                "end": END
            }
        )
        
        workflow.add_conditional_edges(
            "advisor",
            self._route_from_advisor,
            {
                "coordinator": "coordinator",
                "planner": "planner",
                "notewriter": "notewriter",
                "end": END
            }
        )
        
        # Set entry point
        workflow.set_entry_point("coordinator")
        
        # Compile the graph
        self.workflow_graph = workflow.compile()
        
        self.logger.info("Workflow graph created successfully")
    
    def _initialize_tool_executor(self):
        """Initialize the tool executor for agent interactions."""
        # Create tools for each agent
        tools = {}
        
        for agent_name, agent in self.agents.items():
            tools[f"{agent_name}_process_task"] = {
                "name": f"{agent_name}_process_task",
                "description": f"Process a task using the {agent_name} agent",
                "fn": agent.process_task
            }
        
        self.tool_executor = ToolExecutor(tools)
        self.logger.info("Tool executor initialized")
    
    def _initialize_checkpointer(self):
        """Initialize the checkpointer for state persistence."""
        self.checkpointer = MemorySaver()
        self.logger.info("Checkpointer initialized")
    
    async def conduct_assessment(
        self,
        student_id: str,
        learning_preferences: Dict[str, float],
        academic_commitments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Conduct initial student assessment.
        
        Args:
            student_id: Unique identifier for the student
            learning_preferences: Learning style preferences
            academic_commitments: Current academic commitments
            
        Returns:
            Assessment results
        """
        try:
            # Create initial state
            initial_state = AscendState(
                student_id=student_id,
                current_task="initial_assessment",
                task_data={
                    "learning_preferences": learning_preferences,
                    "academic_commitments": academic_commitments
                },
                workflow_step="coordinator",
                agent_results={},
                workflow_history=[],
                created_at=datetime.now()
            )
            
            # Execute workflow
            config = {"configurable": {"thread_id": student_id}}
            result = await self.workflow_graph.ainvoke(initial_state, config)
            
            return {
                "student_id": student_id,
                "assessment_complete": True,
                "results": result.agent_results,
                "workflow_history": result.workflow_history
            }
            
        except Exception as e:
            self.logger.error(f"Assessment failed for student {student_id}: {e}")
            raise
    
    async def optimize_schedule(
        self,
        student_id: str,
        available_time_slots: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Optimize student schedule.
        
        Args:
            student_id: Student identifier
            available_time_slots: Available time slots for scheduling
            
        Returns:
            Optimized schedule
        """
        try:
            # Create state for schedule optimization
            state = AscendState(
                student_id=student_id,
                current_task="schedule_optimization",
                task_data={
                    "available_time_slots": available_time_slots
                },
                workflow_step="planner",
                agent_results={},
                workflow_history=[],
                created_at=datetime.now()
            )
            
            # Execute workflow starting from planner
            config = {"configurable": {"thread_id": f"{student_id}_schedule"}}
            result = await self.workflow_graph.ainvoke(state, config)
            
            return {
                "student_id": student_id,
                "schedule_optimized": True,
                "schedule": result.agent_results.get("planner", {}),
                "workflow_history": result.workflow_history
            }
            
        except Exception as e:
            self.logger.error(f"Schedule optimization failed for student {student_id}: {e}")
            raise
    
    async def generate_materials(
        self,
        student_id: str,
        topic: str,
        learning_style: str
    ) -> Dict[str, Any]:
        """
        Generate customized learning materials.
        
        Args:
            student_id: Student identifier
            topic: Topic for material generation
            learning_style: Preferred learning style
            
        Returns:
            Generated materials
        """
        try:
            # Create state for material generation
            state = AscendState(
                student_id=student_id,
                current_task="material_generation",
                task_data={
                    "topic": topic,
                    "learning_style": learning_style
                },
                workflow_step="notewriter",
                agent_results={},
                workflow_history=[],
                created_at=datetime.now()
            )
            
            # Execute workflow starting from notewriter
            config = {"configurable": {"thread_id": f"{student_id}_materials"}}
            result = await self.workflow_graph.ainvoke(state, config)
            
            return {
                "student_id": student_id,
                "materials_generated": True,
                "materials": result.agent_results.get("notewriter", {}),
                "workflow_history": result.workflow_history
            }
            
        except Exception as e:
            self.logger.error(f"Material generation failed for student {student_id}: {e}")
            raise
    
    async def provide_guidance(
        self,
        student_id: str,
        context: str,
        challenge: str
    ) -> Dict[str, Any]:
        """
        Provide personalized guidance.
        
        Args:
            student_id: Student identifier
            context: Context for guidance
            challenge: Specific challenge to address
            
        Returns:
            Guidance and recommendations
        """
        try:
            # Create state for guidance
            state = AscendState(
                student_id=student_id,
                current_task="guidance_provision",
                task_data={
                    "context": context,
                    "challenge": challenge
                },
                workflow_step="advisor",
                agent_results={},
                workflow_history=[],
                created_at=datetime.now()
            )
            
            # Execute workflow starting from advisor
            config = {"configurable": {"thread_id": f"{student_id}_guidance"}}
            result = await self.workflow_graph.ainvoke(state, config)
            
            return {
                "student_id": student_id,
                "guidance_provided": True,
                "guidance": result.agent_results.get("advisor", {}),
                "workflow_history": result.workflow_history
            }
            
        except Exception as e:
            self.logger.error(f"Guidance provision failed for student {student_id}: {e}")
            raise
    
    # Node functions for the workflow graph
    async def _coordinator_node(self, state: AscendState) -> AscendState:
        """Coordinator agent node."""
        try:
            task = {
                "type": state.current_task,
                "data": state.task_data,
                "student_id": state.student_id
            }
            
            result = await self.agents['coordinator'].process_task(task, state.agent_results)
            
            # Update state
            state.agent_results["coordinator"] = {
                "content": result.content,
                "metadata": result.metadata,
                "success": result.success
            }
            
            state.workflow_history.append({
                "step": "coordinator",
                "timestamp": datetime.now().isoformat(),
                "task": state.current_task,
                "success": result.success
            })
            
            state.workflow_step = "coordinator"
            
            return state
            
        except Exception as e:
            self.logger.error(f"Coordinator node failed: {e}")
            state.agent_results["coordinator"] = {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
            return state
    
    async def _planner_node(self, state: AscendState) -> AscendState:
        """Planner agent node."""
        try:
            task = {
                "type": state.current_task,
                "data": state.task_data,
                "student_id": state.student_id
            }
            
            result = await self.agents['planner'].process_task(task, state.agent_results)
            
            # Update state
            state.agent_results["planner"] = {
                "content": result.content,
                "metadata": result.metadata,
                "success": result.success
            }
            
            state.workflow_history.append({
                "step": "planner",
                "timestamp": datetime.now().isoformat(),
                "task": state.current_task,
                "success": result.success
            })
            
            state.workflow_step = "planner"
            
            return state
            
        except Exception as e:
            self.logger.error(f"Planner node failed: {e}")
            state.agent_results["planner"] = {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
            return state
    
    async def _notewriter_node(self, state: AscendState) -> AscendState:
        """Notewriter agent node."""
        try:
            task = {
                "type": state.current_task,
                "data": state.task_data,
                "student_id": state.student_id
            }
            
            result = await self.agents['notewriter'].process_task(task, state.agent_results)
            
            # Update state
            state.agent_results["notewriter"] = {
                "content": result.content,
                "metadata": result.metadata,
                "success": result.success
            }
            
            state.workflow_history.append({
                "step": "notewriter",
                "timestamp": datetime.now().isoformat(),
                "task": state.current_task,
                "success": result.success
            })
            
            state.workflow_step = "notewriter"
            
            return state
            
        except Exception as e:
            self.logger.error(f"Notewriter node failed: {e}")
            state.agent_results["notewriter"] = {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
            return state
    
    async def _advisor_node(self, state: AscendState) -> AscendState:
        """Advisor agent node."""
        try:
            task = {
                "type": state.current_task,
                "data": state.task_data,
                "student_id": state.student_id
            }
            
            result = await self.agents['advisor'].process_task(task, state.agent_results)
            
            # Update state
            state.agent_results["advisor"] = {
                "content": result.content,
                "metadata": result.metadata,
                "success": result.success
            }
            
            state.workflow_history.append({
                "step": "advisor",
                "timestamp": datetime.now().isoformat(),
                "task": state.current_task,
                "success": result.success
            })
            
            state.workflow_step = "advisor"
            
            return state
            
        except Exception as e:
            self.logger.error(f"Advisor node failed: {e}")
            state.agent_results["advisor"] = {
                "content": "",
                "metadata": {},
                "success": False,
                "error": str(e)
            }
            return state
    
    # Routing functions for conditional edges
    def _route_from_coordinator(self, state: AscendState) -> str:
        """Route from coordinator to next agent."""
        task = state.current_task
        
        if task == "initial_assessment":
            return "planner"
        elif task == "schedule_optimization":
            return "planner"
        elif task == "material_generation":
            return "notewriter"
        elif task == "guidance_provision":
            return "advisor"
        else:
            return "end"
    
    def _route_from_planner(self, state: AscendState) -> str:
        """Route from planner to next agent."""
        # Planner typically completes its task and returns to coordinator
        return "coordinator"
    
    def _route_from_notewriter(self, state: AscendState) -> str:
        """Route from notewriter to next agent."""
        # Notewriter typically completes its task and returns to coordinator
        return "coordinator"
    
    def _route_from_advisor(self, state: AscendState) -> str:
        """Route from advisor to next agent."""
        # Advisor typically completes its task and returns to coordinator
        return "coordinator"
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status."""
        return {
            "agents_initialized": len(self.agents),
            "workflow_graph_created": self.workflow_graph is not None,
            "tool_executor_ready": self.tool_executor is not None,
            "checkpointer_ready": self.checkpointer is not None,
            "agent_names": list(self.agents.keys())
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on all components."""
        health_status = {
            "workflow": True,
            "agents": {},
            "overall": True
        }
        
        # Check each agent
        for name, agent in self.agents.items():
            try:
                agent_health = await agent.health_check()
                health_status["agents"][name] = agent_health
                if not agent_health:
                    health_status["overall"] = False
            except Exception as e:
                health_status["agents"][name] = False
                health_status["overall"] = False
                self.logger.error(f"Health check failed for agent {name}: {e}")
        
        return health_status
