#!/usr/bin/env python3
"""
Ascend - Adaptive Student Companion for Educational Navigation & Development

Main application entry point for the Ascend system.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from workflows.main_workflow import AscendWorkflow
from services.assessment_service import AssessmentService
from services.schedule_service import ScheduleService
from services.content_service import ContentService
from services.integration_service import IntegrationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ascend.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class AscendApplication:
    """Main application class for Ascend system."""
    
    def __init__(self):
        """Initialize the Ascend application."""
        self.settings = Settings()
        self.workflow = None
        self.app = None
        self.services = {}
        
    async def initialize(self):
        """Initialize all components of the Ascend system."""
        logger.info("Initializing Ascend system...")
        
        try:
            # Initialize services
            self.services['assessment'] = AssessmentService()
            self.services['schedule'] = ScheduleService()
            self.services['content'] = ContentService()
            self.services['integration'] = IntegrationService()
            
            # Initialize main workflow
            self.workflow = AscendWorkflow(services=self.services)
            await self.workflow.initialize()
            
            # Initialize FastAPI application
            self.app = self._create_fastapi_app()
            
            logger.info("Ascend system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Ascend system: {e}")
            raise
    
    def _create_fastapi_app(self) -> FastAPI:
        """Create and configure the FastAPI application."""
        app = FastAPI(
            title="Ascend API",
            description="Adaptive Student Companion for Educational Navigation & Development",
            version="1.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Add CORS middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add routes
        self._add_routes(app)
        
        return app
    
    def _add_routes(self, app: FastAPI):
        """Add API routes to the FastAPI application."""
        
        @app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "message": "Welcome to Ascend",
                "version": "1.0.0",
                "status": "running"
            }
        
        @app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy",
                "services": {
                    "workflow": self.workflow is not None,
                    "assessment": "assessment" in self.services,
                    "schedule": "schedule" in self.services,
                    "content": "content" in self.services,
                    "integration": "integration" in self.services
                }
            }
        
        @app.post("/assessment/conduct")
        async def conduct_assessment(student_data: dict):
            """Conduct initial student assessment."""
            try:
                result = await self.workflow.conduct_assessment(
                    student_id=student_data.get("student_id"),
                    learning_preferences=student_data.get("learning_preferences", {}),
                    academic_commitments=student_data.get("academic_commitments", [])
                )
                return {"success": True, "data": result}
            except Exception as e:
                logger.error(f"Assessment failed: {e}")
                return {"success": False, "error": str(e)}
        
        @app.post("/schedule/optimize")
        async def optimize_schedule(schedule_data: dict):
            """Optimize student schedule."""
            try:
                result = await self.workflow.optimize_schedule(
                    student_id=schedule_data.get("student_id"),
                    available_time_slots=schedule_data.get("available_time_slots", [])
                )
                return {"success": True, "data": result}
            except Exception as e:
                logger.error(f"Schedule optimization failed: {e}")
                return {"success": False, "error": str(e)}
        
        @app.post("/materials/generate")
        async def generate_materials(material_data: dict):
            """Generate customized learning materials."""
            try:
                result = await self.workflow.generate_materials(
                    student_id=material_data.get("student_id"),
                    topic=material_data.get("topic"),
                    learning_style=material_data.get("learning_style")
                )
                return {"success": True, "data": result}
            except Exception as e:
                logger.error(f"Material generation failed: {e}")
                return {"success": False, "error": str(e)}
        
        @app.post("/guidance/provide")
        async def provide_guidance(guidance_data: dict):
            """Provide personalized guidance."""
            try:
                result = await self.workflow.provide_guidance(
                    student_id=guidance_data.get("student_id"),
                    context=guidance_data.get("context"),
                    challenge=guidance_data.get("challenge")
                )
                return {"success": True, "data": result}
            except Exception as e:
                logger.error(f"Guidance provision failed: {e}")
                return {"success": False, "error": str(e)}
    
    async def run_server(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the FastAPI server."""
        if not self.app:
            await self.initialize()
        
        logger.info(f"Starting Ascend server on {host}:{port}")
        config = uvicorn.Config(
            app=self.app,
            host=host,
            port=port,
            log_level="info",
            reload=self.settings.DEBUG
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    async def run_cli(self, command: str, **kwargs):
        """Run CLI commands."""
        if not self.workflow:
            await self.initialize()
        
        if command == "assess":
            student_id = kwargs.get("student_id")
            if not student_id:
                print("Error: student_id is required for assessment")
                return
            
            result = await self.workflow.conduct_assessment(
                student_id=student_id,
                learning_preferences=kwargs.get("learning_preferences", {}),
                academic_commitments=kwargs.get("academic_commitments", [])
            )
            print(f"Assessment completed for student {student_id}")
            print(f"Result: {result}")
        
        elif command == "schedule":
            student_id = kwargs.get("student_id")
            if not student_id:
                print("Error: student_id is required for schedule optimization")
                return
            
            result = await self.workflow.optimize_schedule(
                student_id=student_id,
                available_time_slots=kwargs.get("available_time_slots", [])
            )
            print(f"Schedule optimized for student {student_id}")
            print(f"Result: {result}")
        
        elif command == "materials":
            student_id = kwargs.get("student_id")
            topic = kwargs.get("topic")
            if not student_id or not topic:
                print("Error: student_id and topic are required for material generation")
                return
            
            result = await self.workflow.generate_materials(
                student_id=student_id,
                topic=topic,
                learning_style=kwargs.get("learning_style", "visual")
            )
            print(f"Materials generated for student {student_id} on topic {topic}")
            print(f"Result: {result}")
        
        else:
            print(f"Unknown command: {command}")
            print("Available commands: assess, schedule, materials")


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ascend - Adaptive Student Companion")
    parser.add_argument("--mode", choices=["server", "cli"], default="server",
                       help="Run mode: server or cli")
    parser.add_argument("--host", default="0.0.0.0", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--command", help="CLI command to run")
    parser.add_argument("--student-id", help="Student ID for CLI commands")
    parser.add_argument("--topic", help="Topic for material generation")
    parser.add_argument("--learning-style", help="Learning style preference")
    
    args = parser.parse_args()
    
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    app = AscendApplication()
    
    try:
        if args.mode == "server":
            await app.run_server(host=args.host, port=args.port)
        elif args.mode == "cli":
            await app.run_cli(
                command=args.command,
                student_id=args.student_id,
                topic=args.topic,
                learning_style=args.learning_style
            )
    except KeyboardInterrupt:
        logger.info("Shutting down Ascend system...")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
