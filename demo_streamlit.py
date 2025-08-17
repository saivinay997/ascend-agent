#!/usr/bin/env python3
"""
Demo script for the Ascend Streamlit UI.
This script demonstrates the UI features with sample data.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_dashboard():
    """Demo dashboard with sample data."""
    st.markdown("## 📊 Dashboard Demo")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Assessments", 3, "+1")
    
    with col2:
        st.metric("Schedules", 2, "+1")
    
    with col3:
        st.metric("Materials", 5, "+2")
    
    with col4:
        st.metric("Active Sessions", 1, "0")
    
    # Sample recent activity
    st.markdown("### Recent Activity")
    activities = [
        {"time": "2 hours ago", "action": "Generated study materials for Calculus", "type": "Materials"},
        {"time": "4 hours ago", "action": "Optimized study schedule", "type": "Schedule"},
        {"time": "1 day ago", "action": "Completed learning assessment", "type": "Assessment"},
        {"time": "2 days ago", "action": "Received guidance on time management", "type": "Guidance"}
    ]
    
    for activity in activities:
        st.markdown(f"**{activity['time']}** - {activity['type']}: {activity['action']}")

def demo_assessment():
    """Demo assessment with sample results."""
    st.markdown("## 📋 Assessment Demo")
    
    # Sample assessment form
    with st.form("demo_assessment"):
        st.markdown("### Learning Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            visual = st.slider("Visual Learning", 0.0, 1.0, 0.8, 0.1)
            auditory = st.slider("Auditory Learning", 0.0, 1.0, 0.6, 0.1)
        
        with col2:
            kinesthetic = st.slider("Kinesthetic Learning", 0.0, 1.0, 0.4, 0.1)
            reading = st.slider("Reading/Writing", 0.0, 1.0, 0.7, 0.1)
        
        st.markdown("### Academic Commitments")
        st.markdown("- Mathematics 101 (3 credits)")
        st.markdown("- Physics 101 (4 credits)")
        st.markdown("- English Literature (3 credits)")
        
        submitted = st.form_submit_button("Run Demo Assessment")
        
        if submitted:
            st.success("Assessment completed successfully!")
            
            # Sample results
            st.markdown("### Assessment Results")
            st.markdown("**Primary Learning Style:** Visual")
            
            st.markdown("**Analysis:**")
            st.markdown("""
            Based on your learning preferences, you show a strong preference for visual learning (0.8) 
            combined with reading/writing (0.7). This suggests you learn best through:
            
            - **Visual aids**: Diagrams, charts, and visual representations
            - **Written materials**: Notes, textbooks, and written explanations
            - **Combined approach**: Visual + textual information
            
            Your moderate auditory preference (0.6) indicates you can also benefit from:
            - Lectures and discussions
            - Audio explanations
            - Group study sessions
            """)
            
            st.markdown("**Key Recommendations:**")
            st.markdown("1. Use mind maps and diagrams for complex topics")
            st.markdown("2. Take detailed notes during lectures")
            st.markdown("3. Create visual summaries of key concepts")
            st.markdown("4. Combine visual and textual study materials")
            st.markdown("5. Use color coding in your notes")

def demo_schedule():
    """Demo schedule optimization."""
    st.markdown("## 📅 Schedule Optimization Demo")
    
    with st.form("demo_schedule"):
        st.markdown("### Available Time Slots")
        st.markdown("- Monday: 9:00 AM - 5:00 PM")
        st.markdown("- Tuesday: 10:00 AM - 4:00 PM")
        st.markdown("- Wednesday: 9:00 AM - 6:00 PM")
        st.markdown("- Thursday: 11:00 AM - 7:00 PM")
        st.markdown("- Friday: 9:00 AM - 3:00 PM")
        
        st.markdown("### Study Preferences")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("- Study Duration: 2 hours")
            st.markdown("- Break Duration: 15 minutes")
        with col2:
            st.markdown("- Max Sessions: 3 per day")
            st.markdown("- Energy Level: High")
        
        submitted = st.form_submit_button("Generate Demo Schedule")
        
        if submitted:
            st.success("Schedule optimized successfully!")
            
            st.markdown("### Optimized Schedule")
            st.markdown("""
            **Monday:**
            - 9:00-11:00 AM: Mathematics 101 (High energy for complex topics)
            - 11:15-11:30 AM: Break
            - 11:30-1:30 PM: Physics 101 (Continued high energy)
            - 1:30-2:30 PM: Lunch break
            - 2:30-4:30 PM: English Literature (Moderate energy for reading)
            
            **Tuesday:**
            - 10:00-12:00 AM: Physics 101 (Problem solving)
            - 12:15-12:30 PM: Break
            - 12:30-2:30 PM: Mathematics 101 (Practice problems)
            - 2:45-4:00 PM: Review and planning
            
            **Wednesday:**
            - 9:00-11:00 AM: English Literature (Essay writing)
            - 11:15-11:30 AM: Break
            - 11:30-1:30 PM: Mathematics 101 (New concepts)
            - 1:30-2:30 PM: Lunch
            - 2:30-4:30 PM: Physics 101 (Lab preparation)
            - 4:45-6:00 PM: Group study session
            """)
            
            st.markdown("**Schedule Recommendations:**")
            st.markdown("1. Start with most challenging subjects during peak energy")
            st.markdown("2. Include regular breaks to maintain focus")
            st.markdown("3. Group similar subjects together for efficiency")

def demo_materials():
    """Demo learning materials generation."""
    st.markdown("## 📚 Learning Materials Demo")
    
    with st.form("demo_materials"):
        st.markdown("### Material Generation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("- Topic: Calculus Derivatives")
            st.markdown("- Learning Style: Visual")
        with col2:
            st.markdown("- Difficulty: Intermediate")
            st.markdown("- Material Type: Study Guide")
        
        st.markdown("### Generation Options")
        st.markdown("- Include examples: ✅")
        st.markdown("- Include practice: ✅")
        st.markdown("- Include visuals: ✅")
        st.markdown("- Adaptive content: ✅")
        
        submitted = st.form_submit_button("Generate Demo Materials")
        
        if submitted:
            st.success("Learning materials generated successfully!")
            
            st.markdown("### Generated Study Guide: Calculus Derivatives")
            
            with st.expander("Introduction to Derivatives", expanded=True):
                st.markdown("""
                **What is a Derivative?**
                
                A derivative represents the rate of change of a function at any given point. 
                It tells us how fast the function is changing and in what direction.
                
                **Visual Representation:**
                - Think of a derivative as the slope of a tangent line
                - Positive derivative = function is increasing
                - Negative derivative = function is decreasing
                - Zero derivative = function is constant
                """)
            
            with st.expander("Basic Derivative Rules"):
                st.markdown("""
                **Power Rule:**
                - If f(x) = x^n, then f'(x) = n·x^(n-1)
                - Example: f(x) = x³ → f'(x) = 3x²
                
                **Constant Rule:**
                - If f(x) = c, then f'(x) = 0
                - Example: f(x) = 5 → f'(x) = 0
                
                **Sum Rule:**
                - If f(x) = g(x) + h(x), then f'(x) = g'(x) + h'(x)
                """)
            
            with st.expander("Practice Problems"):
                st.markdown("""
                **Problem 1:** Find the derivative of f(x) = 2x³ + 5x² - 3x + 7
                
                **Solution:**
                - f'(x) = 6x² + 10x - 3
                
                **Problem 2:** Find the derivative of f(x) = x⁴ - 2x² + 1
                
                **Solution:**
                - f'(x) = 4x³ - 4x
                """)
            
            st.markdown("**Study Tips:**")
            st.markdown("1. Draw graphs to visualize the concepts")
            st.markdown("2. Practice with different types of functions")
            st.markdown("3. Use the power rule as your foundation")
            st.markdown("4. Check your work by taking the derivative of your answer")

def demo_guidance():
    """Demo personalized guidance."""
    st.markdown("## 💡 Personalized Guidance Demo")
    
    with st.form("demo_guidance"):
        st.markdown("### Guidance Request")
        st.markdown("**Context:** I'm struggling with time management between my three courses. I feel overwhelmed and don't know how to prioritize my studies.")
        
        st.markdown("**Guidance Type:** Time Management")
        st.markdown("**Urgency Level:** High")
        st.markdown("**Include Resources:** Yes")
        
        submitted = st.form_submit_button("Get Demo Guidance")
        
        if submitted:
            st.success("Guidance generated successfully!")
            
            st.markdown("### Personalized Guidance")
            
            st.markdown("""
            **Understanding Your Situation:**
            
            Feeling overwhelmed with multiple courses is very common, especially when each course 
            has different demands and deadlines. Let's break this down into manageable steps.
            
            **Immediate Action Plan:**
            
            1. **Audit Your Current Schedule** (Today)
               - List all upcoming deadlines and exams
               - Identify which courses need immediate attention
               - Calculate how much time each task realistically needs
            
            2. **Create a Priority Matrix** (This week)
               - High Priority/High Urgency: Do first
               - High Priority/Low Urgency: Schedule for later
               - Low Priority/High Urgency: Delegate if possible
               - Low Priority/Low Urgency: Eliminate or postpone
            
            3. **Implement the 2-Minute Rule** (Starting now)
               - If a task takes less than 2 minutes, do it immediately
               - This prevents small tasks from accumulating
            """)
            
            st.markdown("**Action Items:**")
            st.markdown("1. Create a master calendar with all deadlines")
            st.markdown("2. Use the Pomodoro Technique (25-min focused sessions)")
            st.markdown("3. Set specific study goals for each session")
            st.markdown("4. Review and adjust your schedule weekly")
            st.markdown("5. Don't forget to include breaks and self-care")
            
            st.markdown("**Additional Resources:**")
            st.markdown("- Time management apps: Forest, Focus@Will")
            st.markdown("- Study techniques: Pomodoro, spaced repetition")
            st.markdown("- Academic support: Check if your school offers tutoring")

def demo_analytics():
    """Demo analytics and insights."""
    st.markdown("## 📈 Analytics & Insights Demo")
    
    # Sample metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assessments", 3)
    
    with col2:
        st.metric("Schedules Created", 2)
    
    with col3:
        st.metric("Materials Generated", 5)
    
    # Sample progress chart
    st.markdown("### Learning Progress")
    import pandas as pd
    
    progress_data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
        'Progress': [75, 82, 78, 85, 88]
    })
    
    st.line_chart(progress_data.set_index('Week'))
    
    # Sample recent activity
    st.markdown("### Recent Activity")
    activities = [
        {"date": "2024-01-15 14:30", "type": "Assessment", "description": "Learning style: Visual"},
        {"date": "2024-01-14 16:45", "type": "Schedule", "description": "Optimized schedule created"},
        {"date": "2024-01-13 10:20", "type": "Materials", "description": "Generated Study Guide for Calculus"},
        {"date": "2024-01-12 09:15", "type": "Guidance", "description": "Time management advice provided"},
        {"date": "2024-01-11 15:30", "type": "Materials", "description": "Generated Practice Problems for Physics"}
    ]
    
    for activity in activities:
        st.markdown(f"**{activity['date']}** - {activity['type']}: {activity['description']}")

def main():
    """Main demo function."""
    st.set_page_config(
        page_title="Ascend Demo",
        page_icon="🎓",
        layout="wide"
    )
    
    st.markdown("""
    # 🎓 Ascend - Streamlit UI Demo
    
    This demo showcases the key features of the Ascend Adaptive Student Companion system.
    """)
    
    # Navigation
    st.sidebar.markdown("## Demo Navigation")
    
    demo_pages = {
        "📊 Dashboard": demo_dashboard,
        "📋 Assessment": demo_assessment,
        "📅 Schedule": demo_schedule,
        "📚 Materials": demo_materials,
        "💡 Guidance": demo_guidance,
        "📈 Analytics": demo_analytics
    }
    
    selected_page = st.sidebar.selectbox("Choose a demo page:", list(demo_pages.keys()))
    
    # Run selected demo
    demo_pages[selected_page]()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Note:** This is a demo with sample data. The actual application connects to Google's Gemini AI 
    to provide real-time, personalized responses based on your input.
    """)

if __name__ == "__main__":
    main()
