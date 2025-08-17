#!/usr/bin/env python3
"""
Launcher script for the Ascend Streamlit UI.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import langchain
        import google.generativeai
        print("✅ All required dependencies are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_environment():
    """Check if environment is properly configured."""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("The application will run with default settings.")
        print("To use Gemini AI features, create a .env file with:")
        print("GOOGLE_API_KEY=your_actual_api_key_here")
        print("Continuing with limited functionality...")
        return True
    
    # Check if GOOGLE_API_KEY is set
    try:
        from config.settings import settings
        if settings.has_gemini_config:
            print("✅ Google API key is configured.")
            return True
        else:
            print("⚠️  Google API key not found in .env file!")
            print("The application will run with limited functionality.")
            print("To use Gemini AI features, add GOOGLE_API_KEY=your_actual_api_key_here to your .env file")
            return True  # Continue anyway
    except Exception as e:
        print(f"⚠️  Error checking configuration: {e}")
        print("Continuing with default settings...")
        return True

def create_logs_directory():
    """Create logs directory if it doesn't exist."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    print("✅ Logs directory ready.")

def check_database():
    """Check if database can be initialized."""
    try:
        from services.database_service import database_service
        print("✅ Database service initialized successfully.")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("This might be due to permission issues or missing dependencies.")
        return False

def main():
    """Main launcher function."""
    print("🎓 Ascend - Streamlit UI Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create logs directory
    create_logs_directory()
    
    # Check database
    if not check_database():
        print("⚠️  Database initialization failed, but continuing...")
        print("Some features may not work properly.")
    
    print("\n🚀 Starting Streamlit UI...")
    print("The application will open in your default web browser.")
    print("If it doesn't open automatically, go to: http://localhost:8501")
    print("\nPress Ctrl+C to stop the application.")
    print("=" * 50)
    
    try:
        # Run Streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user.")
    except Exception as e:
        print(f"\n❌ Error running Streamlit app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
