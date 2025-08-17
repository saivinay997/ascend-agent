#!/usr/bin/env python3
"""
Test script for database functionality and user history storage.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services.database_service import database_service


def test_database_functionality():
    """Test the database functionality."""
    print("Testing database functionality...")
    
    # Test user creation
    user_id = "test_user_123"
    print(f"Creating user: {user_id}")
    
    try:
        # Test assessment storage
        print("\n1. Testing assessment storage...")
        assessment_result = database_service.store_assessment(
            user_id=user_id,
            learning_preferences={
                "visual": 0.8,
                "auditory": 0.6,
                "kinesthetic": 0.4,
                "reading": 0.7
            },
            academic_commitments=[
                {"course": "Mathematics", "credits": 3},
                {"course": "Physics", "credits": 4}
            ],
            additional_context="Student prefers visual learning methods",
            primary_learning_style="Visual",
            analysis_results="This student shows a strong preference for visual learning...",
            recommendations=["Use diagrams and charts", "Create mind maps", "Watch educational videos"],
            processing_time=2.5,
            success=True
        )
        print(f"✅ Assessment stored with ID: {assessment_result.id}")
        
        # Test schedule storage
        print("\n2. Testing schedule storage...")
        schedule_result = database_service.store_schedule(
            user_id=user_id,
            available_time_slots=[
                {"day": "Monday", "start": "09:00", "end": "17:00"},
                {"day": "Tuesday", "start": "10:00", "end": "16:00"}
            ],
            study_preferences={
                "study_duration": 2,
                "break_duration": 15,
                "max_sessions": 3,
                "energy_level": "Medium"
            },
            optimization_options={
                "include_breaks": True,
                "prioritize_difficult": True
            },
            optimized_schedule="Monday: 9:00-11:00 Math, 11:15-13:15 Physics...",
            schedule_recommendations=["Take breaks every 2 hours", "Study difficult subjects first"],
            processing_time=3.2,
            success=True
        )
        print(f"✅ Schedule stored with ID: {schedule_result.id}")
        
        # Test material storage
        print("\n3. Testing material storage...")
        material_result = database_service.store_material(
            user_id=user_id,
            topic="Calculus Derivatives",
            learning_style="Visual",
            difficulty_level="Intermediate",
            material_type="Study Guide",
            additional_requirements="Include step-by-step examples",
            generation_options={
                "include_examples": True,
                "include_practice": True,
                "include_visuals": True,
                "adaptive_content": True
            },
            generated_content="# Calculus Derivatives Study Guide\n\n## Introduction...",
            content_sections=["Introduction", "Basic Rules", "Examples", "Practice Problems"],
            processing_time=4.1,
            success=True
        )
        print(f"✅ Material stored with ID: {material_result.id}")
        
        # Test guidance storage
        print("\n4. Testing guidance storage...")
        guidance_result = database_service.store_guidance(
            user_id=user_id,
            context="I'm struggling with time management and procrastination",
            guidance_type="Time Management",
            urgency_level="High",
            include_resources=True,
            guidance_content="Here are some strategies to improve your time management...",
            action_items=["Create a daily schedule", "Use the Pomodoro technique", "Set specific goals"],
            processing_time=1.8,
            success=True
        )
        print(f"✅ Guidance stored with ID: {guidance_result.id}")
        
        # Test query storage
        print("\n5. Testing query storage...")
        query_result = database_service.store_query(
            user_id=user_id,
            query_type="assessment",
            query_text="Please analyze my learning preferences...",
            query_data={"learning_style": "visual"},
            response_text="Based on your preferences, I recommend...",
            response_data={"recommendations": ["Use visual aids", "Create diagrams"]},
            processing_time=2.1,
            success=True,
            model_used="gemini-2.0-flash-lite",
            tokens_used=150
        )
        print(f"✅ Query stored with ID: {query_result.id}")
        
        # Test user statistics
        print("\n6. Testing user statistics...")
        stats = database_service.get_user_statistics(user_id)
        print(f"✅ User statistics retrieved:")
        print(f"   - Total interactions: {stats['total_interactions']}")
        print(f"   - Assessments: {stats['assessments']['total']}")
        print(f"   - Schedules: {stats['schedules']['total']}")
        print(f"   - Materials: {stats['materials']['total']}")
        print(f"   - Guidance: {stats['guidance']['total']}")
        print(f"   - Queries: {stats['queries']['total']}")
        
        # Test user history retrieval
        print("\n7. Testing user history retrieval...")
        history = database_service.get_user_history(user_id, limit=10)
        print(f"✅ User history retrieved:")
        print(f"   - Assessments: {len(history['assessments'])}")
        print(f"   - Schedules: {len(history['schedules'])}")
        print(f"   - Materials: {len(history['materials'])}")
        print(f"   - Guidance: {len(history['guidance'])}")
        print(f"   - Queries: {len(history['queries'])}")
        
        # Test specific history type
        print("\n8. Testing specific history type...")
        assessment_history = database_service.get_user_history(user_id, query_type="assessment", limit=5)
        print(f"✅ Assessment history retrieved: {len(assessment_history['assessments'])} records")
        
        print("\n🎉 All database tests passed successfully!")
        
        # Clean up test data
        print("\n9. Cleaning up test data...")
        database_service.delete_user_history(user_id)
        print("✅ Test data cleaned up")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_database_functionality()
