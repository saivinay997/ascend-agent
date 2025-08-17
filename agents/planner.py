"""
Planner Agent for the Ascend system.

The Planner Agent focuses on schedule optimization and time management,
creating personalized study schedules that adapt to student preferences
and energy patterns.
"""

import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from .base_agent import BaseAgent, AgentResponse
from config.logging_config import LoggerMixin


@dataclass
class TimeSlot:
    """Represents a time slot in a schedule."""
    day: str
    start_time: str
    end_time: str
    activity: str
    priority: int = 1
    energy_level: str = "medium"  # low, medium, high
    flexibility: float = 0.5  # 0.0 = fixed, 1.0 = flexible


@dataclass
class StudySession:
    """Represents a study session."""
    subject: str
    duration: int  # minutes
    learning_style: str
    difficulty: str  # easy, medium, hard
    energy_requirement: str  # low, medium, high
    deadline: Optional[datetime] = None


class PlannerAgent(BaseAgent):
    """
    Planner Agent - Schedule optimization and time management specialist.
    
    Responsibilities:
    - Create personalized study schedules
    - Optimize time allocation based on energy patterns
    - Manage deadlines and priorities
    - Adapt schedules to changing circumstances
    - Implement spaced repetition scheduling
    """
    
    def __init__(self, **kwargs):
        """Initialize the Planner Agent."""
        super().__init__(
            name="Planner",
            description="Schedule optimization and time management specialist",
            **kwargs
        )
        self.student_schedules = {}
        self.energy_patterns = {}
        self.deadline_tracker = {}
        
    async def process_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Process a planning task.
        
        Args:
            task: Task to process
            context: Additional context
            
        Returns:
            AgentResponse with the result
        """
        task_type = task.get("type", "unknown")
        
        if task_type == "create_schedule":
            return await self._create_schedule(task, context)
        elif task_type == "optimize_schedule":
            return await self._optimize_schedule(task, context)
        elif task_type == "add_study_session":
            return await self._add_study_session(task, context)
        elif task_type == "manage_deadlines":
            return await self._manage_deadlines(task, context)
        elif task_type == "adapt_schedule":
            return await self._adapt_schedule(task, context)
        elif task_type == "spaced_repetition":
            return await self._schedule_spaced_repetition(task, context)
        else:
            return await self._handle_unknown_task(task, context)
    
    async def _create_schedule(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Create a new personalized study schedule."""
        student_id = task.get("student_id")
        available_time = task.get("available_time", [])
        subjects = task.get("subjects", [])
        learning_preferences = task.get("learning_preferences", {})
        energy_pattern = task.get("energy_pattern", {})
        
        if not student_id:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error="Student ID is required"
            )
        
        try:
            # Analyze energy patterns
            energy_analysis = self._analyze_energy_patterns(energy_pattern)
            
            # Create study sessions based on subjects
            study_sessions = self._create_study_sessions(subjects, learning_preferences)
            
            # Optimize time allocation
            optimized_schedule = self._optimize_time_allocation(
                available_time, study_sessions, energy_analysis
            )
            
            # Store the schedule
            self.student_schedules[student_id] = {
                "schedule": optimized_schedule,
                "energy_pattern": energy_analysis,
                "learning_preferences": learning_preferences,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
            
            schedule_summary = self._generate_schedule_summary(optimized_schedule)
            
            return AgentResponse(
                content=schedule_summary,
                metadata={
                    "student_id": student_id,
                    "schedule": optimized_schedule,
                    "energy_analysis": energy_analysis,
                    "sessions_count": len(study_sessions)
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Schedule creation failed",
                student_id=student_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id},
                success=False,
                error=str(e)
            )
    
    async def _optimize_schedule(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Optimize an existing schedule."""
        student_id = task.get("student_id")
        optimization_criteria = task.get("criteria", {})
        
        if student_id not in self.student_schedules:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"No schedule found for student {student_id}"
            )
        
        try:
            current_schedule = self.student_schedules[student_id]["schedule"]
            
            # Apply optimization strategies
            optimized_schedule = self._apply_optimization_strategies(
                current_schedule, optimization_criteria
            )
            
            # Update the stored schedule
            self.student_schedules[student_id]["schedule"] = optimized_schedule
            self.student_schedules[student_id]["last_updated"] = datetime.now().isoformat()
            
            optimization_summary = self._generate_optimization_summary(
                current_schedule, optimized_schedule
            )
            
            return AgentResponse(
                content=optimization_summary,
                metadata={
                    "student_id": student_id,
                    "optimized_schedule": optimized_schedule,
                    "criteria": optimization_criteria
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Schedule optimization failed",
                student_id=student_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id},
                success=False,
                error=str(e)
            )
    
    async def _add_study_session(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Add a new study session to an existing schedule."""
        student_id = task.get("student_id")
        session_data = task.get("session", {})
        
        if student_id not in self.student_schedules:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"No schedule found for student {student_id}"
            )
        
        try:
            # Create study session object
            study_session = StudySession(
                subject=session_data.get("subject"),
                duration=session_data.get("duration", 60),
                learning_style=session_data.get("learning_style", "visual"),
                difficulty=session_data.get("difficulty", "medium"),
                energy_requirement=session_data.get("energy_requirement", "medium"),
                deadline=session_data.get("deadline")
            )
            
            # Find optimal time slot
            current_schedule = self.student_schedules[student_id]["schedule"]
            optimal_slot = self._find_optimal_time_slot(current_schedule, study_session)
            
            if optimal_slot:
                # Add session to schedule
                new_time_slot = TimeSlot(
                    day=optimal_slot["day"],
                    start_time=optimal_slot["start_time"],
                    end_time=optimal_slot["end_time"],
                    activity=f"Study: {study_session.subject}",
                    priority=session_data.get("priority", 1),
                    energy_level=study_session.energy_requirement
                )
                
                current_schedule.append(new_time_slot)
                
                # Re-optimize schedule
                optimized_schedule = self._optimize_time_allocation(
                    self._extract_available_time(current_schedule),
                    [study_session],
                    self.student_schedules[student_id]["energy_pattern"]
                )
                
                self.student_schedules[student_id]["schedule"] = optimized_schedule
                self.student_schedules[student_id]["last_updated"] = datetime.now().isoformat()
                
                return AgentResponse(
                    content=f"Study session for {study_session.subject} added successfully",
                    metadata={
                        "student_id": student_id,
                        "session": session_data,
                        "optimal_slot": optimal_slot
                    },
                    success=True
                )
            else:
                return AgentResponse(
                    content="",
                    metadata={"student_id": student_id},
                    success=False,
                    error="No suitable time slot found for the study session"
                )
                
        except Exception as e:
            self.logger.error(
                "Adding study session failed",
                student_id=student_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id},
                success=False,
                error=str(e)
            )
    
    async def _manage_deadlines(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Manage deadlines and create urgency-based scheduling."""
        student_id = task.get("student_id")
        deadline_data = task.get("deadline", {})
        
        if student_id not in self.student_schedules:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"No schedule found for student {student_id}"
            )
        
        try:
            # Add deadline to tracker
            if student_id not in self.deadline_tracker:
                self.deadline_tracker[student_id] = []
            
            deadline_info = {
                "subject": deadline_data.get("subject"),
                "deadline": deadline_data.get("deadline"),
                "priority": deadline_data.get("priority", 1),
                "description": deadline_data.get("description", "")
            }
            
            self.deadline_tracker[student_id].append(deadline_info)
            
            # Re-prioritize schedule based on deadlines
            updated_schedule = self._prioritize_by_deadlines(
                self.student_schedules[student_id]["schedule"],
                self.deadline_tracker[student_id]
            )
            
            self.student_schedules[student_id]["schedule"] = updated_schedule
            self.student_schedules[student_id]["last_updated"] = datetime.now().isoformat()
            
            deadline_summary = self._generate_deadline_summary(
                self.deadline_tracker[student_id]
            )
            
            return AgentResponse(
                content=deadline_summary,
                metadata={
                    "student_id": student_id,
                    "deadline": deadline_info,
                    "updated_schedule": updated_schedule
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Deadline management failed",
                student_id=student_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id},
                success=False,
                error=str(e)
            )
    
    async def _adapt_schedule(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Adapt schedule to changing circumstances."""
        student_id = task.get("student_id")
        changes = task.get("changes", {})
        
        if student_id not in self.student_schedules:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"No schedule found for student {student_id}"
            )
        
        try:
            current_schedule = self.student_schedules[student_id]["schedule"]
            
            # Apply changes
            adapted_schedule = self._apply_schedule_changes(current_schedule, changes)
            
            # Re-optimize if needed
            if changes.get("reoptimize", False):
                adapted_schedule = self._optimize_time_allocation(
                    self._extract_available_time(adapted_schedule),
                    self._extract_study_sessions(adapted_schedule),
                    self.student_schedules[student_id]["energy_pattern"]
                )
            
            self.student_schedules[student_id]["schedule"] = adapted_schedule
            self.student_schedules[student_id]["last_updated"] = datetime.now().isoformat()
            
            adaptation_summary = self._generate_adaptation_summary(changes)
            
            return AgentResponse(
                content=adaptation_summary,
                metadata={
                    "student_id": student_id,
                    "changes": changes,
                    "adapted_schedule": adapted_schedule
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Schedule adaptation failed",
                student_id=student_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id},
                success=False,
                error=str(e)
            )
    
    async def _schedule_spaced_repetition(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Schedule spaced repetition sessions."""
        student_id = task.get("student_id")
        subject = task.get("subject")
        initial_date = task.get("initial_date")
        
        if student_id not in self.student_schedules:
            return AgentResponse(
                content="",
                metadata={"task": task},
                success=False,
                error=f"No schedule found for student {student_id}"
            )
        
        try:
            # Calculate spaced repetition intervals
            intervals = self._calculate_spaced_repetition_intervals(initial_date)
            
            # Create review sessions
            review_sessions = []
            for i, interval in enumerate(intervals):
                review_date = initial_date + timedelta(days=interval)
                review_session = StudySession(
                    subject=f"{subject} Review {i+1}",
                    duration=30,  # Shorter review sessions
                    learning_style="mixed",
                    difficulty="easy",
                    energy_requirement="low",
                    deadline=review_date
                )
                review_sessions.append(review_session)
            
            # Add review sessions to schedule
            current_schedule = self.student_schedules[student_id]["schedule"]
            for session in review_sessions:
                optimal_slot = self._find_optimal_time_slot(current_schedule, session)
                if optimal_slot:
                    new_time_slot = TimeSlot(
                        day=optimal_slot["day"],
                        start_time=optimal_slot["start_time"],
                        end_time=optimal_slot["end_time"],
                        activity=f"Review: {session.subject}",
                        priority=2,
                        energy_level="low"
                    )
                    current_schedule.append(new_time_slot)
            
            self.student_schedules[student_id]["schedule"] = current_schedule
            self.student_schedules[student_id]["last_updated"] = datetime.now().isoformat()
            
            return AgentResponse(
                content=f"Spaced repetition scheduled for {subject}",
                metadata={
                    "student_id": student_id,
                    "subject": subject,
                    "intervals": intervals,
                    "review_sessions": len(review_sessions)
                },
                success=True
            )
            
        except Exception as e:
            self.logger.error(
                "Spaced repetition scheduling failed",
                student_id=student_id,
                error=str(e)
            )
            return AgentResponse(
                content="",
                metadata={"student_id": student_id},
                success=False,
                error=str(e)
            )
    
    def _analyze_energy_patterns(self, energy_pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze student energy patterns throughout the day."""
        # This is a simplified analysis - in a real implementation,
        # you might use more sophisticated algorithms
        analysis = {
            "peak_hours": [],
            "low_energy_hours": [],
            "recommended_break_times": []
        }
        
        # Analyze hourly energy levels
        for hour, energy in energy_pattern.get("hourly_energy", {}).items():
            if energy >= 8:  # High energy
                analysis["peak_hours"].append(hour)
            elif energy <= 4:  # Low energy
                analysis["low_energy_hours"].append(hour)
        
        return analysis
    
    def _create_study_sessions(
        self, 
        subjects: List[Dict[str, Any]], 
        learning_preferences: Dict[str, Any]
    ) -> List[StudySession]:
        """Create study sessions based on subjects and learning preferences."""
        sessions = []
        
        for subject in subjects:
            session = StudySession(
                subject=subject.get("name"),
                duration=subject.get("recommended_duration", 60),
                learning_style=learning_preferences.get("preferred_style", "visual"),
                difficulty=subject.get("difficulty", "medium"),
                energy_requirement=subject.get("energy_requirement", "medium")
            )
            sessions.append(session)
        
        return sessions
    
    def _optimize_time_allocation(
        self, 
        available_time: List[Dict[str, Any]], 
        study_sessions: List[StudySession],
        energy_analysis: Dict[str, Any]
    ) -> List[TimeSlot]:
        """Optimize time allocation for study sessions."""
        schedule = []
        
        # Sort sessions by priority and energy requirements
        high_energy_sessions = [s for s in study_sessions if s.energy_requirement == "high"]
        medium_energy_sessions = [s for s in study_sessions if s.energy_requirement == "medium"]
        low_energy_sessions = [s for s in study_sessions if s.energy_requirement == "low"]
        
        # Allocate high-energy sessions to peak hours
        for session in high_energy_sessions:
            slot = self._find_optimal_slot_for_energy_level(
                available_time, session, "high", energy_analysis["peak_hours"]
            )
            if slot:
                schedule.append(slot)
        
        # Allocate remaining sessions
        remaining_sessions = medium_energy_sessions + low_energy_sessions
        for session in remaining_sessions:
            slot = self._find_optimal_slot_for_energy_level(
                available_time, session, session.energy_requirement
            )
            if slot:
                schedule.append(slot)
        
        return schedule
    
    def _find_optimal_slot_for_energy_level(
        self, 
        available_time: List[Dict[str, Any]], 
        session: StudySession,
        energy_level: str,
        preferred_hours: List[str] = None
    ) -> Optional[TimeSlot]:
        """Find optimal time slot for a session based on energy level."""
        # Simplified implementation - in reality, this would be more sophisticated
        for time_slot in available_time:
            if preferred_hours and time_slot.get("hour") in preferred_hours:
                return TimeSlot(
                    day=time_slot["day"],
                    start_time=time_slot["start_time"],
                    end_time=time_slot["end_time"],
                    activity=f"Study: {session.subject}",
                    energy_level=energy_level
                )
        
        # Fallback to any available slot
        if available_time:
            slot = available_time[0]
            return TimeSlot(
                day=slot["day"],
                start_time=slot["start_time"],
                end_time=slot["end_time"],
                activity=f"Study: {session.subject}",
                energy_level=energy_level
            )
        
        return None
    
    def _find_optimal_time_slot(
        self, 
        schedule: List[TimeSlot], 
        session: StudySession
    ) -> Optional[Dict[str, Any]]:
        """Find optimal time slot for a new study session."""
        # Simplified implementation
        # In reality, this would analyze gaps in the schedule
        return {
            "day": "Monday",
            "start_time": "10:00",
            "end_time": "11:00"
        }
    
    def _extract_available_time(self, schedule: List[TimeSlot]) -> List[Dict[str, Any]]:
        """Extract available time slots from schedule."""
        # Simplified implementation
        return [
            {"day": "Monday", "start_time": "09:00", "end_time": "17:00"},
            {"day": "Tuesday", "start_time": "09:00", "end_time": "17:00"},
            {"day": "Wednesday", "start_time": "09:00", "end_time": "17:00"},
            {"day": "Thursday", "start_time": "09:00", "end_time": "17:00"},
            {"day": "Friday", "start_time": "09:00", "end_time": "17:00"}
        ]
    
    def _extract_study_sessions(self, schedule: List[TimeSlot]) -> List[StudySession]:
        """Extract study sessions from schedule."""
        sessions = []
        for slot in schedule:
            if "Study:" in slot.activity:
                subject = slot.activity.replace("Study: ", "")
                sessions.append(StudySession(
                    subject=subject,
                    duration=60,  # Default duration
                    learning_style="mixed",
                    difficulty="medium",
                    energy_requirement=slot.energy_level
                ))
        return sessions
    
    def _apply_optimization_strategies(
        self, 
        schedule: List[TimeSlot], 
        criteria: Dict[str, Any]
    ) -> List[TimeSlot]:
        """Apply optimization strategies to schedule."""
        # Simplified implementation
        return schedule
    
    def _prioritize_by_deadlines(
        self, 
        schedule: List[TimeSlot], 
        deadlines: List[Dict[str, Any]]
    ) -> List[TimeSlot]:
        """Prioritize schedule based on deadlines."""
        # Simplified implementation
        return schedule
    
    def _apply_schedule_changes(
        self, 
        schedule: List[TimeSlot], 
        changes: Dict[str, Any]
    ) -> List[TimeSlot]:
        """Apply changes to schedule."""
        # Simplified implementation
        return schedule
    
    def _calculate_spaced_repetition_intervals(self, initial_date: datetime) -> List[int]:
        """Calculate spaced repetition intervals."""
        # Standard spaced repetition intervals (in days)
        return [1, 3, 7, 14, 30, 90]
    
    def _generate_schedule_summary(self, schedule: List[TimeSlot]) -> str:
        """Generate a summary of the schedule."""
        summary = "📅 Personalized Study Schedule Created\n\n"
        
        for slot in schedule:
            summary += f"📚 {slot.day} {slot.start_time}-{slot.end_time}: {slot.activity}\n"
        
        return summary
    
    def _generate_optimization_summary(
        self, 
        original: List[TimeSlot], 
        optimized: List[TimeSlot]
    ) -> str:
        """Generate optimization summary."""
        return f"✅ Schedule optimized successfully!\n\nOriginal sessions: {len(original)}\nOptimized sessions: {len(optimized)}"
    
    def _generate_deadline_summary(self, deadlines: List[Dict[str, Any]]) -> str:
        """Generate deadline summary."""
        summary = "⏰ Deadline Management Summary\n\n"
        
        for deadline in deadlines:
            summary += f"📝 {deadline['subject']}: {deadline['deadline']}\n"
        
        return summary
    
    def _generate_adaptation_summary(self, changes: Dict[str, Any]) -> str:
        """Generate adaptation summary."""
        return f"🔄 Schedule adapted successfully!\n\nChanges applied: {len(changes)} modifications"
    
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
    
    def get_capabilities(self) -> List[str]:
        """Get the capabilities of the Planner Agent."""
        return [
            "Personalized study schedule creation",
            "Time optimization based on energy patterns",
            "Deadline management and prioritization",
            "Schedule adaptation to changing circumstances",
            "Spaced repetition scheduling",
            "Learning style optimization"
        ]
    
    def get_student_schedule(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Get schedule for a specific student."""
        return self.student_schedules.get(student_id)
    
    def get_deadlines(self, student_id: str) -> List[Dict[str, Any]]:
        """Get deadlines for a specific student."""
        return self.deadline_tracker.get(student_id, [])
