#!/usr/bin/env python3
"""
Streamlit UI for Ascend - Adaptive Student Companion for Educational Navigation & Development
"""

import streamlit as st
import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from agents.base_agent import SimpleAgent, AgentResponse
from services.assessment_service import AssessmentService
from services.schedule_service import ScheduleService
from services.content_service import ContentService
from services.integration_service import IntegrationService
from services.database_service import database_service


# Page configuration
st.set_page_config(
    page_title="Ascend - Adaptive Student Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)


class StreamlitUI:
    """Main Streamlit UI class for Ascend."""
    
    def __init__(self):
        """Initialize the Streamlit UI."""
        self.initialize_session_state()
        self.services = self.initialize_services()
    
    def initialize_session_state(self):
        """Initialize session state variables."""
        if 'student_data' not in st.session_state:
            st.session_state.student_data = {}
        if 'assessment_results' not in st.session_state:
            st.session_state.assessment_results = {}
        if 'schedule_data' not in st.session_state:
            st.session_state.schedule_data = {}
        if 'materials_data' not in st.session_state:
            st.session_state.materials_data = {}
        if 'current_student_id' not in st.session_state:
            st.session_state.current_student_id = None
    
    def initialize_services(self) -> Dict[str, Any]:
        """Initialize all services."""
        try:
            return {
                'assessment': AssessmentService(),
                'schedule': ScheduleService(),
                'content': ContentService(),
                'integration': IntegrationService()
            }
        except Exception as e:
            st.error(f"Failed to initialize services: {e}")
            return {}
    
    def run(self):
        """Run the main Streamlit application."""
        # Header
        st.markdown('<h1 class="main-header">🎓 Ascend</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Adaptive Student Companion for Educational Navigation & Development</p>', unsafe_allow_html=True)
        
        # Sidebar navigation
        self.render_sidebar()
        
        # Main content area
        page = st.session_state.get('current_page', 'dashboard')
        
        if page == 'dashboard':
            self.render_dashboard()
        elif page == 'assessment':
            self.render_assessment_page()
        elif page == 'schedule':
            self.render_schedule_page()
        elif page == 'materials':
            self.render_materials_page()
        elif page == 'guidance':
            self.render_guidance_page()
        elif page == 'analytics':
            self.render_analytics_page()
        elif page == 'history':
            self.render_history_page()
        elif page == 'settings':
            self.render_settings_page()
    
    def render_sidebar(self):
        """Render the sidebar navigation."""
        with st.sidebar:
            st.markdown("## Navigation")
            
            # Student selection
            st.markdown("### Student")
            student_id = st.text_input("Student ID", value=st.session_state.current_student_id or "")
            if student_id != st.session_state.current_student_id:
                st.session_state.current_student_id = student_id
            
            # Navigation menu
            st.markdown("### Menu")
            pages = {
                "📊 Dashboard": "dashboard",
                "📋 Assessment": "assessment", 
                "📅 Schedule": "schedule",
                "📚 Materials": "materials",
                "💡 Guidance": "guidance",
                "📈 Analytics": "analytics",
                "📜 History": "history",
                "⚙️ Settings": "settings"
            }
            
            for label, page_name in pages.items():
                if st.button(label, key=f"nav_{page_name}"):
                    st.session_state.current_page = page_name
                    st.rerun()
            
            # System status
            st.markdown("---")
            st.markdown("### System Status")
            
            # Check Gemini connection
            if settings.has_gemini_config:
                st.success("✅ Gemini Connected")
            else:
                st.error("❌ Gemini Not Configured")
            
            # Display current model
            st.info(f"Model: {settings.GEMINI_MODEL}")
    
    def render_dashboard(self):
        """Render the main dashboard."""
        st.markdown('<h2 class="sub-header">Dashboard</h2>', unsafe_allow_html=True)
        
        # Welcome message
        if st.session_state.current_student_id:
            st.markdown(f"### Welcome, Student {st.session_state.current_student_id}!")
        else:
            st.markdown("### Welcome to Ascend!")
            st.info("Please enter a Student ID in the sidebar to get started.")
            return
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Assessments", len(st.session_state.assessment_results))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Schedules", len(st.session_state.schedule_data))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Materials", len(st.session_state.materials_data))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Active Sessions", 1)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent activity
        st.markdown("### Recent Activity")
        
        # Quick actions
        st.markdown("### Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 New Assessment", use_container_width=True):
                st.session_state.current_page = "assessment"
                st.rerun()
        
        with col2:
            if st.button("📅 Optimize Schedule", use_container_width=True):
                st.session_state.current_page = "schedule"
                st.rerun()
        
        with col3:
            if st.button("📚 Generate Materials", use_container_width=True):
                st.session_state.current_page = "materials"
                st.rerun()
    
    def render_assessment_page(self):
        """Render the assessment page."""
        st.markdown('<h2 class="sub-header">Student Assessment</h2>', unsafe_allow_html=True)
        
        if not st.session_state.current_student_id:
            st.error("Please enter a Student ID in the sidebar first.")
            return
        
        # Course management (outside form)
        st.markdown("### Academic Commitments")
        courses = st.session_state.get('courses', [])
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Add Course"):
                courses.append({"course": "", "credits": 3})
                st.session_state.courses = courses
                st.rerun()
        
        for i, course in enumerate(courses):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                course["course"] = st.text_input(f"Course {i+1}", course["course"], key=f"course_{i}")
            with col2:
                course["credits"] = st.number_input("Credits", min_value=1, max_value=6, value=course["credits"], key=f"credits_{i}")
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    courses.pop(i)
                    st.session_state.courses = courses
                    st.rerun()
        
        # Assessment form
        with st.form("assessment_form"):
            st.markdown("### Learning Preferences")
            
            col1, col2 = st.columns(2)
            
            with col1:
                visual_pref = st.slider("Visual Learning", 0.0, 1.0, 0.5, 0.1)
                auditory_pref = st.slider("Auditory Learning", 0.0, 1.0, 0.5, 0.1)
            
            with col2:
                kinesthetic_pref = st.slider("Kinesthetic Learning", 0.0, 1.0, 0.5, 0.1)
                reading_pref = st.slider("Reading/Writing", 0.0, 1.0, 0.5, 0.1)
            
            # Additional context
            st.markdown("### Additional Context")
            additional_context = st.text_area("Any additional information about the student's learning needs, challenges, or goals:")
            
            submitted = st.form_submit_button("Conduct Assessment")
            
            if submitted:
                self.run_assessment(visual_pref, auditory_pref, kinesthetic_pref, reading_pref, courses, additional_context)
    
    def run_assessment(self, visual_pref, auditory_pref, kinesthetic_pref, reading_pref, courses, additional_context):
        """Run the assessment process."""
        start_time = datetime.now()
        
        with st.spinner("Conducting assessment..."):
            try:
                # Prepare assessment data
                learning_preferences = {
                    "visual": visual_pref,
                    "auditory": auditory_pref,
                    "kinesthetic": kinesthetic_pref,
                    "reading": reading_pref
                }
                
                academic_commitments = courses
                
                # Create assessment service call
                assessment_data = {
                    "student_id": st.session_state.current_student_id,
                    "learning_preferences": learning_preferences,
                    "academic_commitments": academic_commitments,
                    "additional_context": additional_context
                }
                
                # Store in session state
                assessment_id = f"assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.assessment_results[assessment_id] = assessment_data
                
                # Simulate assessment processing
                import time
                time.sleep(2)  # Simulate processing time
                
                # Generate assessment results
                results = self.generate_assessment_results(learning_preferences, academic_commitments, additional_context)
                
                st.session_state.assessment_results[assessment_id]["results"] = results
                
                # Calculate processing time
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store in database
                try:
                    database_service.store_assessment(
                        user_id=st.session_state.current_student_id,
                        learning_preferences=learning_preferences,
                        academic_commitments=academic_commitments,
                        additional_context=additional_context,
                        primary_learning_style=results.get('learning_style'),
                        analysis_results=results.get('analysis'),
                        recommendations=results.get('recommendations'),
                        processing_time=processing_time,
                        success=True
                    )
                except Exception as db_error:
                    st.warning(f"Assessment completed but failed to save to history: {db_error}")
                
                st.success("Assessment completed successfully!")
                
                # Display results
                self.display_assessment_results(results)
                
            except Exception as e:
                # Calculate processing time for failed assessment
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store failed assessment in database
                try:
                    database_service.store_assessment(
                        user_id=st.session_state.current_student_id,
                        learning_preferences=learning_preferences,
                        academic_commitments=academic_commitments,
                        additional_context=additional_context,
                        processing_time=processing_time,
                        success=False,
                        error_message=str(e)
                    )
                except Exception as db_error:
                    pass  # Don't show error for database storage failure
                
                st.error(f"Assessment failed: {e}")
    
    def generate_assessment_results(self, learning_preferences, academic_commitments, additional_context):
        """Generate assessment results using Gemini."""
        try:
            # Create a simple agent for assessment
            assessment_agent = SimpleAgent(
                name="AssessmentAgent",
                description="Specialized agent for student assessment and analysis"
            )
            
            # Prepare the assessment prompt
            prompt = f"""
            Please analyze the following student data and provide a comprehensive assessment:
            
            Learning Preferences:
            - Visual: {learning_preferences['visual']}
            - Auditory: {learning_preferences['auditory']}
            - Kinesthetic: {learning_preferences['kinesthetic']}
            - Reading/Writing: {learning_preferences['reading']}
            
            Academic Commitments:
            {json.dumps(academic_commitments, indent=2)}
            
            Additional Context:
            {additional_context}
            
            Please provide:
            1. Learning style analysis
            2. Recommended study strategies
            3. Potential challenges and solutions
            4. Personalized recommendations
            """
            
            # Store query in database
            try:
                database_service.store_query(
                    user_id=st.session_state.current_student_id,
                    query_type="assessment",
                    query_text=prompt,
                    query_data={
                        "learning_preferences": learning_preferences,
                        "academic_commitments": academic_commitments,
                        "additional_context": additional_context
                    }
                )
            except Exception as db_error:
                pass  # Don't fail the assessment if query storage fails
            
            # Run the assessment
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(assessment_agent.process_message(prompt))
            loop.close()
            
            if response.success:
                # Store response in database
                try:
                    database_service.store_query(
                        user_id=st.session_state.current_student_id,
                        query_type="assessment_response",
                        query_text=prompt,
                        response_text=response.content,
                        response_data={
                            "learning_style": self.determine_primary_learning_style(learning_preferences),
                            "recommendations": self.extract_recommendations(response.content)
                        },
                        success=True
                    )
                except Exception as db_error:
                    pass  # Don't fail the assessment if response storage fails
                
                return {
                    "analysis": response.content,
                    "learning_style": self.determine_primary_learning_style(learning_preferences),
                    "recommendations": self.extract_recommendations(response.content),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Store failed response in database
                try:
                    database_service.store_query(
                        user_id=st.session_state.current_student_id,
                        query_type="assessment_response",
                        query_text=prompt,
                        response_text="Assessment analysis could not be completed.",
                        success=False,
                        error_message="AI response was not successful"
                    )
                except Exception as db_error:
                    pass
                
                return {
                    "analysis": "Assessment analysis could not be completed.",
                    "learning_style": "Unknown",
                    "recommendations": [],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            # Store error in database
            try:
                database_service.store_query(
                    user_id=st.session_state.current_student_id,
                    query_type="assessment_error",
                    query_text=prompt,
                    success=False,
                    error_message=str(e)
                )
            except Exception as db_error:
                pass
            
            return {
                "analysis": f"Error during assessment: {e}",
                "learning_style": "Unknown",
                "recommendations": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def determine_primary_learning_style(self, preferences):
        """Determine the primary learning style from preferences."""
        max_pref = max(preferences.items(), key=lambda x: x[1])
        return max_pref[0].title()
    
    def extract_recommendations(self, analysis_text):
        """Extract recommendations from analysis text."""
        # Simple extraction - in a real implementation, this would be more sophisticated
        recommendations = []
        lines = analysis_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'try', 'use']):
                recommendations.append(line.strip())
        return recommendations[:5]  # Limit to 5 recommendations
    
    def display_assessment_results(self, results):
        """Display assessment results."""
        st.markdown("### Assessment Results")
        
        # Learning style
        st.markdown(f"**Primary Learning Style:** {results['learning_style']}")
        
        # Analysis
        st.markdown("**Analysis:**")
        st.markdown(results['analysis'])
        
        # Recommendations
        if results['recommendations']:
            st.markdown("**Key Recommendations:**")
            for i, rec in enumerate(results['recommendations'], 1):
                st.markdown(f"{i}. {rec}")
    
    def render_schedule_page(self):
        """Render the schedule optimization page."""
        st.markdown('<h2 class="sub-header">Schedule Optimization</h2>', unsafe_allow_html=True)
        
        if not st.session_state.current_student_id:
            st.error("Please enter a Student ID in the sidebar first.")
            return
        
        # Time slot management (outside form)
        st.markdown("### Available Time Slots")
        time_slots = st.session_state.get('time_slots', [])
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Add Time Slot"):
                time_slots.append({"day": "Monday", "start": "09:00", "end": "17:00"})
                st.session_state.time_slots = time_slots
                st.rerun()
        
        for i, slot in enumerate(time_slots):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
            with col1:
                slot["day"] = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], key=f"day_{i}")
            with col2:
                slot["start"] = st.time_input("Start", value=datetime.strptime(slot["start"], "%H:%M").time(), key=f"start_{i}")
            with col3:
                slot["end"] = st.time_input("End", value=datetime.strptime(slot["end"], "%H:%M").time(), key=f"end_{i}")
            with col4:
                if st.button("Remove", key=f"remove_slot_{i}"):
                    time_slots.pop(i)
                    st.session_state.time_slots = time_slots
                    st.rerun()
        
        # Schedule form
        with st.form("schedule_form"):
            # Study preferences
            st.markdown("### Study Preferences")
            col1, col2 = st.columns(2)
            
            with col1:
                preferred_study_duration = st.slider("Preferred Study Duration (hours)", 1, 4, 2)
                break_duration = st.slider("Break Duration (minutes)", 10, 60, 15)
            
            with col2:
                max_study_sessions = st.slider("Max Study Sessions per Day", 1, 6, 3)
                energy_level = st.selectbox("Energy Level", ["Low", "Medium", "High"])
            
            # Optimization options
            st.markdown("### Optimization Options")
            include_breaks = st.checkbox("Include breaks between sessions", value=True)
            prioritize_difficult_subjects = st.checkbox("Prioritize difficult subjects", value=True)
            
            submitted = st.form_submit_button("Optimize Schedule")
            
            if submitted:
                self.run_schedule_optimization(time_slots, preferred_study_duration, break_duration, max_study_sessions, energy_level, include_breaks, prioritize_difficult_subjects)
    
    def run_schedule_optimization(self, time_slots, study_duration, break_duration, max_sessions, energy_level, include_breaks, prioritize_difficult):
        """Run schedule optimization."""
        start_time = datetime.now()
        
        with st.spinner("Optimizing schedule..."):
            try:
                # Prepare schedule data
                schedule_data = {
                    "student_id": st.session_state.current_student_id,
                    "available_time_slots": time_slots,
                    "preferences": {
                        "study_duration": study_duration,
                        "break_duration": break_duration,
                        "max_sessions": max_sessions,
                        "energy_level": energy_level,
                        "include_breaks": include_breaks,
                        "prioritize_difficult": prioritize_difficult
                    }
                }
                
                # Store in session state
                schedule_id = f"schedule_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.schedule_data[schedule_id] = schedule_data
                
                # Generate optimized schedule
                optimized_schedule = self.generate_optimized_schedule(schedule_data)
                
                st.session_state.schedule_data[schedule_id]["optimized_schedule"] = optimized_schedule
                
                # Calculate processing time
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store in database
                try:
                    database_service.store_schedule(
                        user_id=st.session_state.current_student_id,
                        available_time_slots=time_slots,
                        study_preferences=schedule_data["preferences"],
                        optimization_options={
                            "include_breaks": include_breaks,
                            "prioritize_difficult": prioritize_difficult
                        },
                        optimized_schedule=optimized_schedule.get('schedule'),
                        schedule_recommendations=optimized_schedule.get('recommendations'),
                        processing_time=processing_time,
                        success=True
                    )
                except Exception as db_error:
                    st.warning(f"Schedule optimized but failed to save to history: {db_error}")
                
                st.success("Schedule optimized successfully!")
                
                # Display results
                self.display_schedule_results(optimized_schedule)
                
            except Exception as e:
                # Calculate processing time for failed optimization
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store failed schedule in database
                try:
                    database_service.store_schedule(
                        user_id=st.session_state.current_student_id,
                        available_time_slots=time_slots,
                        study_preferences=schedule_data["preferences"],
                        processing_time=processing_time,
                        success=False,
                        error_message=str(e)
                    )
                except Exception as db_error:
                    pass  # Don't show error for database storage failure
                
                st.error(f"Schedule optimization failed: {e}")
    
    def generate_optimized_schedule(self, schedule_data):
        """Generate optimized schedule using Gemini."""
        try:
            # Create schedule optimization agent
            schedule_agent = SimpleAgent(
                name="ScheduleAgent",
                description="Specialized agent for schedule optimization and time management"
            )
            
            # Prepare the schedule prompt
            prompt = f"""
            Please create an optimized study schedule based on the following information:
            
            Student ID: {schedule_data['student_id']}
            
            Available Time Slots:
            {json.dumps(schedule_data['available_time_slots'], indent=2)}
            
            Preferences:
            - Study Duration: {schedule_data['preferences']['study_duration']} hours
            - Break Duration: {schedule_data['preferences']['break_duration']} minutes
            - Max Sessions per Day: {schedule_data['preferences']['max_sessions']}
            - Energy Level: {schedule_data['preferences']['energy_level']}
            - Include Breaks: {schedule_data['preferences']['include_breaks']}
            - Prioritize Difficult Subjects: {schedule_data['preferences']['prioritize_difficult']}
            
            Please provide:
            1. A detailed weekly schedule
            2. Study session recommendations
            3. Break timing suggestions
            4. Energy management tips
            """
            
            # Run the optimization
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(schedule_agent.process_message(prompt))
            loop.close()
            
            if response.success:
                return {
                    "schedule": response.content,
                    "recommendations": self.extract_schedule_recommendations(response.content),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "schedule": "Schedule optimization could not be completed.",
                    "recommendations": [],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "schedule": f"Error during schedule optimization: {e}",
                "recommendations": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def extract_schedule_recommendations(self, schedule_text):
        """Extract schedule recommendations from text."""
        recommendations = []
        lines = schedule_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['recommend', 'suggest', 'tip', 'advice']):
                recommendations.append(line.strip())
        return recommendations[:3]  # Limit to 3 recommendations
    
    def display_schedule_results(self, results):
        """Display schedule optimization results."""
        st.markdown("### Optimized Schedule")
        
        # Schedule
        st.markdown("**Weekly Schedule:**")
        st.markdown(results['schedule'])
        
        # Recommendations
        if results['recommendations']:
            st.markdown("**Schedule Recommendations:**")
            for i, rec in enumerate(results['recommendations'], 1):
                st.markdown(f"{i}. {rec}")
    
    def render_materials_page(self):
        """Render the learning materials page."""
        st.markdown('<h2 class="sub-header">Learning Materials Generation</h2>', unsafe_allow_html=True)
        
        if not st.session_state.current_student_id:
            st.error("Please enter a Student ID in the sidebar first.")
            return
        
        # Materials form
        with st.form("materials_form"):
            st.markdown("### Material Generation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input("Topic/Subject", placeholder="e.g., Calculus Derivatives, Python Programming")
                learning_style = st.selectbox("Learning Style", ["Visual", "Auditory", "Kinesthetic", "Reading/Writing", "Mixed"])
            
            with col2:
                difficulty_level = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
                material_type = st.selectbox("Material Type", ["Study Guide", "Practice Problems", "Summary Notes", "Concept Map", "Video Script"])
            
            # Additional requirements
            st.markdown("### Additional Requirements")
            additional_requirements = st.text_area("Any specific requirements or focus areas:")
            
            # Generation options
            st.markdown("### Generation Options")
            col1, col2 = st.columns(2)
            
            with col1:
                include_examples = st.checkbox("Include examples", value=True)
                include_practice = st.checkbox("Include practice exercises", value=True)
            
            with col2:
                include_visuals = st.checkbox("Include visual elements", value=True)
                adaptive_content = st.checkbox("Adapt to learning style", value=True)
            
            submitted = st.form_submit_button("Generate Materials")
            
            if submitted:
                self.run_material_generation(topic, learning_style, difficulty_level, material_type, additional_requirements, include_examples, include_practice, include_visuals, adaptive_content)
    
    def run_material_generation(self, topic, learning_style, difficulty_level, material_type, additional_requirements, include_examples, include_practice, include_visuals, adaptive_content):
        """Run material generation."""
        start_time = datetime.now()
        
        with st.spinner("Generating learning materials..."):
            try:
                # Prepare material data
                material_data = {
                    "student_id": st.session_state.current_student_id,
                    "topic": topic,
                    "learning_style": learning_style,
                    "difficulty_level": difficulty_level,
                    "material_type": material_type,
                    "additional_requirements": additional_requirements,
                    "options": {
                        "include_examples": include_examples,
                        "include_practice": include_practice,
                        "include_visuals": include_visuals,
                        "adaptive_content": adaptive_content
                    }
                }
                
                # Store in session state
                material_id = f"material_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                st.session_state.materials_data[material_id] = material_data
                
                # Generate materials
                generated_materials = self.generate_learning_materials(material_data)
                
                st.session_state.materials_data[material_id]["generated_content"] = generated_materials
                
                # Calculate processing time
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store in database
                try:
                    database_service.store_material(
                        user_id=st.session_state.current_student_id,
                        topic=topic,
                        learning_style=learning_style,
                        difficulty_level=difficulty_level,
                        material_type=material_type,
                        additional_requirements=additional_requirements,
                        generation_options=material_data["options"],
                        generated_content=generated_materials.get('content'),
                        content_sections=generated_materials.get('sections'),
                        processing_time=processing_time,
                        success=True
                    )
                except Exception as db_error:
                    st.warning(f"Materials generated but failed to save to history: {db_error}")
                
                st.success("Learning materials generated successfully!")
                
                # Display results
                self.display_material_results(generated_materials)
                
            except Exception as e:
                # Calculate processing time for failed generation
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store failed material in database
                try:
                    database_service.store_material(
                        user_id=st.session_state.current_student_id,
                        topic=topic,
                        learning_style=learning_style,
                        difficulty_level=difficulty_level,
                        material_type=material_type,
                        additional_requirements=additional_requirements,
                        generation_options=material_data["options"],
                        processing_time=processing_time,
                        success=False,
                        error_message=str(e)
                    )
                except Exception as db_error:
                    pass  # Don't show error for database storage failure
                
                st.error(f"Material generation failed: {e}")
    
    def generate_learning_materials(self, material_data):
        """Generate learning materials using Gemini."""
        try:
            # Create content generation agent
            content_agent = SimpleAgent(
                name="ContentAgent",
                description="Specialized agent for generating educational content and learning materials"
            )
            
            # Prepare the content prompt
            prompt = f"""
            Please generate comprehensive learning materials for the following request:
            
            Topic: {material_data['topic']}
            Learning Style: {material_data['learning_style']}
            Difficulty Level: {material_data['difficulty_level']}
            Material Type: {material_data['material_type']}
            Additional Requirements: {material_data['additional_requirements']}
            
            Options:
            - Include Examples: {material_data['options']['include_examples']}
            - Include Practice: {material_data['options']['include_practice']}
            - Include Visuals: {material_data['options']['include_visuals']}
            - Adaptive Content: {material_data['options']['adaptive_content']}
            
            Please provide:
            1. Comprehensive content tailored to the learning style
            2. Examples and explanations
            3. Practice exercises (if requested)
            4. Visual descriptions or diagrams (if requested)
            5. Study tips and strategies
            """
            
            # Run the generation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(content_agent.process_message(prompt))
            loop.close()
            
            if response.success:
                return {
                    "content": response.content,
                    "sections": self.extract_content_sections(response.content),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "content": "Material generation could not be completed.",
                    "sections": [],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "content": f"Error during material generation: {e}",
                "sections": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def extract_content_sections(self, content_text):
        """Extract content sections from generated text."""
        sections = []
        lines = content_text.split('\n')
        current_section = ""
        
        for line in lines:
            if line.strip().startswith(('#', '##', '###', '1.', '2.', '3.')):
                if current_section:
                    sections.append(current_section.strip())
                current_section = line
            else:
                current_section += line + "\n"
        
        if current_section:
            sections.append(current_section.strip())
        
        return sections[:5]  # Limit to 5 sections
    
    def display_material_results(self, results):
        """Display material generation results."""
        st.markdown("### Generated Learning Materials")
        
        # Content
        st.markdown("**Content:**")
        st.markdown(results['content'])
        
        # Sections
        if results['sections']:
            st.markdown("**Content Sections:**")
            for i, section in enumerate(results['sections'], 1):
                with st.expander(f"Section {i}"):
                    st.markdown(section)
    
    def render_guidance_page(self):
        """Render the guidance page."""
        st.markdown('<h2 class="sub-header">Personalized Guidance</h2>', unsafe_allow_html=True)
        
        if not st.session_state.current_student_id:
            st.error("Please enter a Student ID in the sidebar first.")
            return
        
        # Guidance form
        with st.form("guidance_form"):
            st.markdown("### Guidance Request")
            
            context = st.text_area("What's your current situation or challenge?", placeholder="Describe your academic situation, challenges, or questions...")
            
            guidance_type = st.selectbox("Type of Guidance", [
                "Study Strategy",
                "Time Management",
                "Subject-Specific Help",
                "Motivation & Mindset",
                "Exam Preparation",
                "General Academic Advice"
            ])
            
            urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High"])
            
            include_resources = st.checkbox("Include additional resources and references", value=True)
            
            submitted = st.form_submit_button("Get Guidance")
            
            if submitted:
                self.run_guidance_generation(context, guidance_type, urgency, include_resources)
    
    def run_guidance_generation(self, context, guidance_type, urgency, include_resources):
        """Run guidance generation."""
        start_time = datetime.now()
        
        with st.spinner("Generating personalized guidance..."):
            try:
                # Prepare guidance data
                guidance_data = {
                    "student_id": st.session_state.current_student_id,
                    "context": context,
                    "guidance_type": guidance_type,
                    "urgency": urgency,
                    "include_resources": include_resources
                }
                
                # Generate guidance
                guidance = self.generate_personalized_guidance(guidance_data)
                
                # Calculate processing time
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store in database
                try:
                    database_service.store_guidance(
                        user_id=st.session_state.current_student_id,
                        context=context,
                        guidance_type=guidance_type,
                        urgency_level=urgency,
                        include_resources=include_resources,
                        guidance_content=guidance.get('guidance'),
                        action_items=guidance.get('action_items'),
                        processing_time=processing_time,
                        success=True
                    )
                except Exception as db_error:
                    st.warning(f"Guidance generated but failed to save to history: {db_error}")
                
                st.success("Guidance generated successfully!")
                
                # Display results
                self.display_guidance_results(guidance)
                
            except Exception as e:
                # Calculate processing time for failed generation
                processing_time = (datetime.now() - start_time).total_seconds()
                
                # Store failed guidance in database
                try:
                    database_service.store_guidance(
                        user_id=st.session_state.current_student_id,
                        context=context,
                        guidance_type=guidance_type,
                        urgency_level=urgency,
                        include_resources=include_resources,
                        processing_time=processing_time,
                        success=False,
                        error_message=str(e)
                    )
                except Exception as db_error:
                    pass  # Don't show error for database storage failure
                
                st.error(f"Guidance generation failed: {e}")
    
    def generate_personalized_guidance(self, guidance_data):
        """Generate personalized guidance using Gemini."""
        try:
            # Create guidance agent
            guidance_agent = SimpleAgent(
                name="GuidanceAgent",
                description="Specialized agent for providing personalized academic guidance and support"
            )
            
            # Prepare the guidance prompt
            prompt = f"""
            Please provide personalized guidance for the following student request:
            
            Student Context: {guidance_data['context']}
            Guidance Type: {guidance_data['guidance_type']}
            Urgency Level: {guidance_data['urgency']}
            Include Resources: {guidance_data['include_resources']}
            
            Please provide:
            1. Personalized advice and strategies
            2. Actionable steps and recommendations
            3. Motivational support and encouragement
            4. Additional resources (if requested)
            5. Follow-up suggestions
            """
            
            # Run the guidance generation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(guidance_agent.process_message(prompt))
            loop.close()
            
            if response.success:
                return {
                    "guidance": response.content,
                    "action_items": self.extract_action_items(response.content),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "guidance": "Guidance could not be generated.",
                    "action_items": [],
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "guidance": f"Error during guidance generation: {e}",
                "action_items": [],
                "timestamp": datetime.now().isoformat()
            }
    
    def extract_action_items(self, guidance_text):
        """Extract action items from guidance text."""
        action_items = []
        lines = guidance_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['do', 'try', 'practice', 'implement', 'start', 'focus']):
                action_items.append(line.strip())
        return action_items[:5]  # Limit to 5 action items
    
    def display_guidance_results(self, results):
        """Display guidance results."""
        st.markdown("### Personalized Guidance")
        
        # Guidance
        st.markdown("**Guidance:**")
        st.markdown(results['guidance'])
        
        # Action items
        if results['action_items']:
            st.markdown("**Action Items:**")
            for i, item in enumerate(results['action_items'], 1):
                st.markdown(f"{i}. {item}")
    
    def render_analytics_page(self):
        """Render the analytics page."""
        st.markdown('<h2 class="sub-header">Analytics & Insights</h2>', unsafe_allow_html=True)
        
        if not st.session_state.current_student_id:
            st.error("Please enter a Student ID in the sidebar first.")
            return
        
        # Analytics overview
        st.markdown("### Learning Analytics")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assessments", len(st.session_state.assessment_results))
        
        with col2:
            st.metric("Schedules Created", len(st.session_state.schedule_data))
        
        with col3:
            st.metric("Materials Generated", len(st.session_state.materials_data))
        
        # Learning progress chart
        st.markdown("### Learning Progress")
        
        # Sample data - in a real implementation, this would come from a database
        progress_data = {
            "Week 1": 75,
            "Week 2": 82,
            "Week 3": 78,
            "Week 4": 85,
            "Week 5": 88
        }
        
        st.line_chart(progress_data)
        
        # Recent activity
        st.markdown("### Recent Activity")
        
        activities = []
        
        # Add assessment activities
        for assessment_id, assessment in st.session_state.assessment_results.items():
            activities.append({
                "date": assessment.get("timestamp", "Unknown"),
                "type": "Assessment",
                "description": f"Learning style: {assessment.get('results', {}).get('learning_style', 'Unknown')}"
            })
        
        # Add schedule activities
        for schedule_id, schedule in st.session_state.schedule_data.items():
            activities.append({
                "date": schedule.get("timestamp", "Unknown"),
                "type": "Schedule",
                "description": f"Optimized schedule created"
            })
        
        # Add material activities
        for material_id, material in st.session_state.materials_data.items():
            activities.append({
                "date": material.get("timestamp", "Unknown"),
                "type": "Materials",
                "description": f"Generated {material.get('material_type', 'Unknown')} for {material.get('topic', 'Unknown')}"
            })
        
        # Sort by date
        activities.sort(key=lambda x: x["date"], reverse=True)
        
        # Display activities
        for activity in activities[:10]:  # Show last 10 activities
            st.markdown(f"**{activity['date']}** - {activity['type']}: {activity['description']}")
    
    def render_history_page(self):
        """Render the user history page."""
        st.markdown('<h2 class="sub-header">User History & Statistics</h2>', unsafe_allow_html=True)
        
        if not st.session_state.current_student_id:
            st.error("Please enter a Student ID in the sidebar first.")
            return
        
        user_id = st.session_state.current_student_id
        
        # Get user statistics
        try:
            stats = database_service.get_user_statistics(user_id)
            
            # Display statistics
            st.markdown("### User Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Interactions", stats["total_interactions"])
            
            with col2:
                st.metric("Assessments", stats["assessments"]["total"])
            
            with col3:
                st.metric("Schedules", stats["schedules"]["total"])
            
            with col4:
                st.metric("Materials", stats["materials"]["total"])
            
            # Success rates
            st.markdown("### Success Rates")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Assessment Success", f"{stats['assessments']['success_rate']:.1f}%")
            
            with col2:
                st.metric("Schedule Success", f"{stats['schedules']['success_rate']:.1f}%")
            
            with col3:
                st.metric("Material Success", f"{stats['materials']['success_rate']:.1f}%")
            
            with col4:
                st.metric("Guidance Success", f"{stats['guidance']['success_rate']:.1f}%")
            
            # Average processing times
            st.markdown("### Average Processing Times (seconds)")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Assessment Time", stats["assessments"]["avg_processing_time"])
            
            with col2:
                st.metric("Schedule Time", stats["schedules"]["avg_processing_time"])
            
            with col3:
                st.metric("Material Time", stats["materials"]["avg_processing_time"])
            
            with col4:
                st.metric("Guidance Time", stats["guidance"]["avg_processing_time"])
            
        except Exception as e:
            st.error(f"Failed to load user statistics: {e}")
            return
        
        # History filters
        st.markdown("### History Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            history_type = st.selectbox(
                "History Type",
                ["All", "Assessment", "Schedule", "Material", "Guidance", "Query"]
            )
        
        with col2:
            limit = st.slider("Number of Records", 5, 50, 20)
        
        with col3:
            if st.button("Load History"):
                st.session_state.history_data = None  # Clear cache
        
        # Load and display history
        if "history_data" not in st.session_state or st.button("Refresh History"):
            try:
                query_type = history_type.lower() if history_type != "All" else None
                history = database_service.get_user_history(user_id, query_type, limit)
                st.session_state.history_data = history
            except Exception as e:
                st.error(f"Failed to load history: {e}")
                return
        
        if "history_data" in st.session_state:
            history = st.session_state.history_data
            
            # Display assessments
            if history["assessments"]:
                st.markdown("### Assessment History")
                for assessment in history["assessments"]:
                    with st.expander(f"Assessment {assessment['_id']} - {assessment['created_at']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Learning Preferences:**")
                            st.json(assessment["learning_preferences"])
                            if assessment["academic_commitments"]:
                                st.write("**Academic Commitments:**")
                                st.json(assessment["academic_commitments"])
                        with col2:
                            st.write(f"**Primary Learning Style:** {assessment['primary_learning_style']}")
                            st.write(f"**Success:** {'✅' if assessment['success'] else '❌'}")
                            if assessment["recommendations"]:
                                st.write("**Recommendations:**")
                                for i, rec in enumerate(assessment["recommendations"], 1):
                                    st.write(f"{i}. {rec}")
            
            # Display schedules
            if history["schedules"]:
                st.markdown("### Schedule History")
                for schedule in history["schedules"]:
                    with st.expander(f"Schedule {schedule['_id']} - {schedule['created_at']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Study Preferences:**")
                            st.json(schedule["study_preferences"])
                        with col2:
                            st.write(f"**Success:** {'✅' if schedule['success'] else '❌'}")
                            if schedule["schedule_recommendations"]:
                                st.write("**Recommendations:**")
                                for i, rec in enumerate(schedule["schedule_recommendations"], 1):
                                    st.write(f"{i}. {rec}")
                        if schedule["optimized_schedule"]:
                            st.write("**Optimized Schedule:**")
                            st.text(schedule["optimized_schedule"])
            
            # Display materials
            if history["materials"]:
                st.markdown("### Material History")
                for material in history["materials"]:
                    with st.expander(f"Material {material['_id']} - {material['topic']} - {material['created_at']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Topic:** {material['topic']}")
                            st.write(f"**Learning Style:** {material['learning_style']}")
                            st.write(f"**Difficulty:** {material['difficulty_level']}")
                            st.write(f"**Type:** {material['material_type']}")
                        with col2:
                            st.write(f"**Success:** {'✅' if material['success'] else '❌'}")
                            if material["content_sections"]:
                                st.write("**Content Sections:**")
                                for i, section in enumerate(material["content_sections"], 1):
                                    st.write(f"{i}. {section[:100]}...")
            
            # Display guidance
            if history["guidance"]:
                st.markdown("### Guidance History")
                for guidance in history["guidance"]:
                    with st.expander(f"Guidance {guidance['_id']} - {guidance['guidance_type']} - {guidance['created_at']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Type:** {guidance['guidance_type']}")
                            st.write(f"**Urgency:** {guidance['urgency_level']}")
                            st.write("**Context:**")
                            st.text(guidance["context"])
                        with col2:
                            st.write(f"**Success:** {'✅' if guidance['success'] else '❌'}")
                            if guidance["action_items"]:
                                st.write("**Action Items:**")
                                for i, item in enumerate(guidance["action_items"], 1):
                                    st.write(f"{i}. {item}")
            
            # Display queries
            if history["queries"]:
                st.markdown("### Query History")
                for query in history["queries"]:
                    with st.expander(f"Query {query['_id']} - {query['query_type']} - {query['created_at']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Query:**")
                            st.text(query["query_text"])
                        with col2:
                            st.write(f"**Type:** {query['query_type']}")
                            st.write(f"**Success:** {'✅' if query['success'] else '❌'}")
                            if query["processing_time"]:
                                st.write(f"**Processing Time:** {query['processing_time']:.2f}s")
        
        # Data management
        st.markdown("### Data Management")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Clear Session Data"):
                st.session_state.assessment_results = {}
                st.session_state.schedule_data = {}
                st.session_state.materials_data = {}
                st.success("Session data cleared!")
        
        with col2:
            if st.button("Export History"):
                try:
                    # Export all history to JSON
                    all_history = database_service.get_user_history(user_id, limit=1000)
                    import json
                    history_json = json.dumps(all_history, indent=2, default=str)
                    st.download_button(
                        label="Download History JSON",
                        data=history_json,
                        file_name=f"user_history_{user_id}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"Failed to export history: {e}")
        
        with col3:
            if st.button("Delete All History"):
                if st.checkbox("I understand this will permanently delete all my history"):
                    try:
                        database_service.delete_user_history(user_id)
                        st.success("All history deleted successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to delete history: {e}")
    
    def render_settings_page(self):
        """Render the settings page."""
        st.markdown('<h2 class="sub-header">Settings & Configuration</h2>', unsafe_allow_html=True)
        
        # System settings
        st.markdown("### System Configuration")
        
        # Gemini settings
        st.markdown("#### LLM Configuration")
        
        if settings.has_gemini_config:
            st.success("✅ Gemini API Key: Configured")
        else:
            st.error("❌ Gemini API Key: Not configured")
        
        st.info(f"Model: {settings.GEMINI_MODEL}")
        st.info(f"Temperature: {settings.GEMINI_TEMPERATURE}")
        st.info(f"Max Tokens: {settings.GEMINI_MAX_TOKENS}")
        
        # System information
        st.markdown("#### System Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"Environment: {settings.ENVIRONMENT}")
            st.info(f"Debug Mode: {settings.DEBUG}")
            st.info(f"Log Level: {settings.LOG_LEVEL}")
        
        with col2:
            st.info(f"Max Sessions: {settings.MAX_CONCURRENT_SESSIONS}")
            st.info(f"Session Timeout: {settings.SESSION_TIMEOUT}s")
            st.info(f"Agent Timeout: {settings.AGENT_TIMEOUT}s")
        
        # Data management
        st.markdown("### Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Session Data"):
                st.session_state.assessment_results = {}
                st.session_state.schedule_data = {}
                st.session_state.materials_data = {}
                st.success("Session data cleared!")
        
        with col2:
            if st.button("Export Data"):
                # In a real implementation, this would export to a file
                st.info("Data export functionality would be implemented here")
        
        # System health
        st.markdown("### System Health")
        
        # Health check
        if st.button("Run Health Check"):
            with st.spinner("Running health check..."):
                try:
                    # Test Gemini connection
                    test_agent = SimpleAgent(
                        name="HealthCheckAgent",
                        description="Agent for system health checks"
                    )
                    
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    health_response = loop.run_until_complete(test_agent.health_check())
                    loop.close()
                    
                    if health_response:
                        st.success("✅ System health check passed!")
                    else:
                        st.error("❌ System health check failed!")
                        
                except Exception as e:
                    st.error(f"❌ Health check error: {e}")


def main():
    """Main function to run the Streamlit app."""
    # Initialize the UI
    ui = StreamlitUI()
    
    # Run the application
    ui.run()


if __name__ == "__main__":
    main()
