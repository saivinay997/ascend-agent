#!/usr/bin/env python3
"""
Test script to verify Gemini integration with the Ascend system.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from agents.base_agent import BaseAgent, AgentResponse


class TestAgent(BaseAgent):
    """Simple test agent to verify Gemini integration."""
    
    def __init__(self):
        super().__init__(
            name="TestAgent",
            description="A test agent for verifying Gemini integration"
        )
    
    async def process_task(
        self, 
        task: Dict[str, Any], 
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """Process a test task."""
        return await self.process_message(
            task.get("message", "Hello, this is a test message."),
            context
        )


async def test_gemini_integration():
    """Test the Gemini integration."""
    print("Testing Gemini integration...")
    
    # Check if API key is configured
    if not settings.has_gemini_config:
        print("❌ Error: Google API key not configured!")
        print("Please set GOOGLE_API_KEY in your .env file")
        return False
    
    print(f"✅ Google API key configured")
    print(f"✅ Using model: {settings.GEMINI_MODEL}")
    
    try:
        # Create test agent
        agent = TestAgent()
        print("✅ Test agent created successfully")
        
        # Test basic message processing
        print("Testing message processing...")
        response = await agent.process_message(
            "Hello! Can you tell me a short joke?"
        )
        
        if response.success:
            print("✅ Message processing successful")
            print(f"Response: {response.content}")
            print(f"Execution time: {response.execution_time:.2f}s")
        else:
            print(f"❌ Message processing failed: {response.error}")
            return False
        
        # Test health check
        print("Testing health check...")
        health_status = await agent.health_check()
        if health_status:
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
            return False
        
        print("🎉 All tests passed! Gemini integration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Run the test
    success = asyncio.run(test_gemini_integration())
    
    if success:
        print("\n✅ Gemini integration test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Gemini integration test failed!")
        sys.exit(1)
