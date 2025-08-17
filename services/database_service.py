"""
Database service for managing user history and queries using MongoDB.
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import json
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for managing user history and database operations using MongoDB."""
    
    def __init__(self):
        """Initialize the database service."""
        self.client = None
        self.database = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize MongoDB connection."""
        try:
            # Connect to MongoDB
            self.client = MongoClient(settings.MONGODB_CONNECTION_STRING)
            self.database = self.client[settings.MONGODB_DATABASE_NAME]
            
            # Test connection
            self.client.admin.command('ping')
            
            logger.info("MongoDB database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize MongoDB database: {e}")
            raise
    
    def _get_collection(self, collection_name: str) -> Collection:
        """Get a MongoDB collection."""
        if self.database is None:
            raise RuntimeError("Database not initialized")
        return self.database[collection_name]
    
    def get_or_create_user(self, user_id: str, session_id: str = None) -> Dict[str, Any]:
        """Get or create a user history record."""
        collection = self._get_collection("users")
        
        user = collection.find_one({"user_id": user_id})
        
        if not user:
            user = {
                "user_id": user_id,
                "session_id": session_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            collection.insert_one(user)
        else:
            # Update session_id if provided
            if session_id:
                collection.update_one(
                    {"user_id": user_id},
                    {"$set": {"session_id": session_id, "updated_at": datetime.utcnow()}}
                )
                user["session_id"] = session_id
        
        return user
    
    def store_query(
        self,
        user_id: str,
        query_type: str,
        query_text: str,
        query_data: Dict[str, Any] = None,
        response_text: str = None,
        response_data: Dict[str, Any] = None,
        processing_time: float = None,
        success: bool = True,
        error_message: str = None,
        model_used: str = None,
        tokens_used: int = None
    ) -> Dict[str, Any]:
        """Store a user query and response."""
        try:
            collection = self._get_collection("queries")
            
            # Get or create user
            self.get_or_create_user(user_id)
            
            # Create query record
            query = {
                "user_id": user_id,
                "query_type": query_type,
                "query_text": query_text,
                "query_data": query_data,
                "response_text": response_text,
                "response_data": response_data,
                "processing_time": processing_time,
                "success": success,
                "error_message": error_message,
                "model_used": model_used,
                "tokens_used": tokens_used,
                "created_at": datetime.utcnow()
            }
            
            result = collection.insert_one(query)
            query["_id"] = result.inserted_id
            
            logger.info(f"Stored query for user {user_id}: {query_type}")
            return query
            
        except Exception as e:
            logger.error(f"Failed to store query: {e}")
            raise
    
    def store_assessment(
        self,
        user_id: str,
        learning_preferences: Dict[str, float],
        academic_commitments: List[Dict[str, Any]] = None,
        additional_context: str = None,
        primary_learning_style: str = None,
        analysis_results: str = None,
        recommendations: List[str] = None,
        processing_time: float = None,
        success: bool = True,
        error_message: str = None
    ) -> Dict[str, Any]:
        """Store assessment history."""
        try:
            collection = self._get_collection("assessments")
            
            # Get or create user
            self.get_or_create_user(user_id)
            
            # Create assessment record
            assessment = {
                "user_id": user_id,
                "learning_preferences": learning_preferences,
                "academic_commitments": academic_commitments,
                "additional_context": additional_context,
                "primary_learning_style": primary_learning_style,
                "analysis_results": analysis_results,
                "recommendations": recommendations,
                "processing_time": processing_time,
                "success": success,
                "error_message": error_message,
                "created_at": datetime.utcnow()
            }
            
            result = collection.insert_one(assessment)
            assessment["_id"] = result.inserted_id
            
            logger.info(f"Stored assessment for user {user_id}")
            return assessment
            
        except Exception as e:
            logger.error(f"Failed to store assessment: {e}")
            raise
    
    def store_schedule(
        self,
        user_id: str,
        available_time_slots: List[Dict[str, Any]],
        study_preferences: Dict[str, Any],
        optimization_options: Dict[str, Any] = None,
        optimized_schedule: str = None,
        schedule_recommendations: List[str] = None,
        processing_time: float = None,
        success: bool = True,
        error_message: str = None
    ) -> Dict[str, Any]:
        """Store schedule optimization history."""
        try:
            collection = self._get_collection("schedules")
            
            # Get or create user
            self.get_or_create_user(user_id)
            
            # Create schedule record
            schedule = {
                "user_id": user_id,
                "available_time_slots": available_time_slots,
                "study_preferences": study_preferences,
                "optimization_options": optimization_options,
                "optimized_schedule": optimized_schedule,
                "schedule_recommendations": schedule_recommendations,
                "processing_time": processing_time,
                "success": success,
                "error_message": error_message,
                "created_at": datetime.utcnow()
            }
            
            result = collection.insert_one(schedule)
            schedule["_id"] = result.inserted_id
            
            logger.info(f"Stored schedule for user {user_id}")
            return schedule
            
        except Exception as e:
            logger.error(f"Failed to store schedule: {e}")
            raise
    
    def store_material(
        self,
        user_id: str,
        topic: str,
        learning_style: str,
        difficulty_level: str,
        material_type: str,
        additional_requirements: str = None,
        generation_options: Dict[str, Any] = None,
        generated_content: str = None,
        content_sections: List[str] = None,
        processing_time: float = None,
        success: bool = True,
        error_message: str = None
    ) -> Dict[str, Any]:
        """Store learning material generation history."""
        try:
            collection = self._get_collection("materials")
            
            # Get or create user
            self.get_or_create_user(user_id)
            
            # Create material record
            material = {
                "user_id": user_id,
                "topic": topic,
                "learning_style": learning_style,
                "difficulty_level": difficulty_level,
                "material_type": material_type,
                "additional_requirements": additional_requirements,
                "generation_options": generation_options,
                "generated_content": generated_content,
                "content_sections": content_sections,
                "processing_time": processing_time,
                "success": success,
                "error_message": error_message,
                "created_at": datetime.utcnow()
            }
            
            result = collection.insert_one(material)
            material["_id"] = result.inserted_id
            
            logger.info(f"Stored material for user {user_id}: {topic}")
            return material
            
        except Exception as e:
            logger.error(f"Failed to store material: {e}")
            raise
    
    def store_guidance(
        self,
        user_id: str,
        context: str,
        guidance_type: str,
        urgency_level: str,
        include_resources: bool = True,
        guidance_content: str = None,
        action_items: List[str] = None,
        processing_time: float = None,
        success: bool = True,
        error_message: str = None
    ) -> Dict[str, Any]:
        """Store guidance history."""
        try:
            collection = self._get_collection("guidance")
            
            # Get or create user
            self.get_or_create_user(user_id)
            
            # Create guidance record
            guidance = {
                "user_id": user_id,
                "context": context,
                "guidance_type": guidance_type,
                "urgency_level": urgency_level,
                "include_resources": include_resources,
                "guidance_content": guidance_content,
                "action_items": action_items,
                "processing_time": processing_time,
                "success": success,
                "error_message": error_message,
                "created_at": datetime.utcnow()
            }
            
            result = collection.insert_one(guidance)
            guidance["_id"] = result.inserted_id
            
            logger.info(f"Stored guidance for user {user_id}: {guidance_type}")
            return guidance
            
        except Exception as e:
            logger.error(f"Failed to store guidance: {e}")
            raise
    
    def get_user_history(
        self,
        user_id: str,
        query_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get user history for all types or specific type."""
        try:
            result = {
                "user_id": user_id,
                "assessments": [],
                "schedules": [],
                "materials": [],
                "guidance": [],
                "queries": []
            }
            
            # Get assessments
            if not query_type or query_type == "assessment":
                collection = self._get_collection("assessments")
                assessments = list(collection.find(
                    {"user_id": user_id}
                ).sort("created_at", -1).skip(offset).limit(limit))
                
                # Convert ObjectId to string for JSON serialization
                for assessment in assessments:
                    assessment["_id"] = str(assessment["_id"])
                    assessment["created_at"] = assessment["created_at"].isoformat()
                
                result["assessments"] = assessments
            
            # Get schedules
            if not query_type or query_type == "schedule":
                collection = self._get_collection("schedules")
                schedules = list(collection.find(
                    {"user_id": user_id}
                ).sort("created_at", -1).skip(offset).limit(limit))
                
                for schedule in schedules:
                    schedule["_id"] = str(schedule["_id"])
                    schedule["created_at"] = schedule["created_at"].isoformat()
                
                result["schedules"] = schedules
            
            # Get materials
            if not query_type or query_type == "material":
                collection = self._get_collection("materials")
                materials = list(collection.find(
                    {"user_id": user_id}
                ).sort("created_at", -1).skip(offset).limit(limit))
                
                for material in materials:
                    material["_id"] = str(material["_id"])
                    material["created_at"] = material["created_at"].isoformat()
                
                result["materials"] = materials
            
            # Get guidance
            if not query_type or query_type == "guidance":
                collection = self._get_collection("guidance")
                guidance = list(collection.find(
                    {"user_id": user_id}
                ).sort("created_at", -1).skip(offset).limit(limit))
                
                for g in guidance:
                    g["_id"] = str(g["_id"])
                    g["created_at"] = g["created_at"].isoformat()
                
                result["guidance"] = guidance
            
            # Get queries
            if not query_type or query_type == "query":
                collection = self._get_collection("queries")
                queries = list(collection.find(
                    {"user_id": user_id}
                ).sort("created_at", -1).skip(offset).limit(limit))
                
                for query in queries:
                    query["_id"] = str(query["_id"])
                    query["created_at"] = query["created_at"].isoformat()
                
                result["queries"] = queries
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get user history: {e}")
            raise
    
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics and summary."""
        try:
            # Count records by type
            assessment_count = self._get_collection("assessments").count_documents({"user_id": user_id})
            schedule_count = self._get_collection("schedules").count_documents({"user_id": user_id})
            material_count = self._get_collection("materials").count_documents({"user_id": user_id})
            guidance_count = self._get_collection("guidance").count_documents({"user_id": user_id})
            query_count = self._get_collection("queries").count_documents({"user_id": user_id})
            
            # Get success rates
            successful_assessments = self._get_collection("assessments").count_documents({
                "user_id": user_id,
                "success": True
            })
            
            successful_schedules = self._get_collection("schedules").count_documents({
                "user_id": user_id,
                "success": True
            })
            
            successful_materials = self._get_collection("materials").count_documents({
                "user_id": user_id,
                "success": True
            })
            
            successful_guidance = self._get_collection("guidance").count_documents({
                "user_id": user_id,
                "success": True
            })
            
            # Get average processing times
            pipeline = [
                {"$match": {"user_id": user_id, "processing_time": {"$ne": None}}},
                {"$group": {"_id": None, "avg_time": {"$avg": "$processing_time"}}}
            ]
            
            avg_assessment_time = 0
            avg_schedule_time = 0
            avg_material_time = 0
            avg_guidance_time = 0
            
            # Calculate average processing times
            assessment_avg = list(self._get_collection("assessments").aggregate(pipeline))
            if assessment_avg:
                avg_assessment_time = assessment_avg[0]["avg_time"]
            
            schedule_avg = list(self._get_collection("schedules").aggregate(pipeline))
            if schedule_avg:
                avg_schedule_time = schedule_avg[0]["avg_time"]
            
            material_avg = list(self._get_collection("materials").aggregate(pipeline))
            if material_avg:
                avg_material_time = material_avg[0]["avg_time"]
            
            guidance_avg = list(self._get_collection("guidance").aggregate(pipeline))
            if guidance_avg:
                avg_guidance_time = guidance_avg[0]["avg_time"]
            
            return {
                "user_id": user_id,
                "total_interactions": assessment_count + schedule_count + material_count + guidance_count + query_count,
                "assessments": {
                    "total": assessment_count,
                    "successful": successful_assessments,
                    "success_rate": (successful_assessments / assessment_count * 100) if assessment_count > 0 else 0,
                    "avg_processing_time": round(avg_assessment_time, 2)
                },
                "schedules": {
                    "total": schedule_count,
                    "successful": successful_schedules,
                    "success_rate": (successful_schedules / schedule_count * 100) if schedule_count > 0 else 0,
                    "avg_processing_time": round(avg_schedule_time, 2)
                },
                "materials": {
                    "total": material_count,
                    "successful": successful_materials,
                    "success_rate": (successful_materials / material_count * 100) if material_count > 0 else 0,
                    "avg_processing_time": round(avg_material_time, 2)
                },
                "guidance": {
                    "total": guidance_count,
                    "successful": successful_guidance,
                    "success_rate": (successful_guidance / guidance_count * 100) if guidance_count > 0 else 0,
                    "avg_processing_time": round(avg_guidance_time, 2)
                },
                "queries": {
                    "total": query_count
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get user statistics: {e}")
            raise
    
    def delete_user_history(self, user_id: str, query_type: str = None) -> bool:
        """Delete user history (all or specific type)."""
        try:
            if query_type == "assessment":
                self._get_collection("assessments").delete_many({"user_id": user_id})
            elif query_type == "schedule":
                self._get_collection("schedules").delete_many({"user_id": user_id})
            elif query_type == "material":
                self._get_collection("materials").delete_many({"user_id": user_id})
            elif query_type == "guidance":
                self._get_collection("guidance").delete_many({"user_id": user_id})
            elif query_type == "query":
                self._get_collection("queries").delete_many({"user_id": user_id})
            else:
                # Delete all history for user
                self._get_collection("assessments").delete_many({"user_id": user_id})
                self._get_collection("schedules").delete_many({"user_id": user_id})
                self._get_collection("materials").delete_many({"user_id": user_id})
                self._get_collection("guidance").delete_many({"user_id": user_id})
                self._get_collection("queries").delete_many({"user_id": user_id})
                self._get_collection("users").delete_many({"user_id": user_id})
            
            logger.info(f"Deleted history for user {user_id}: {query_type or 'all'}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete user history: {e}")
            raise
    
    def close_connection(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


# Global database service instance
database_service = DatabaseService()
