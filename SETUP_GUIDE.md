# Ascend Agent Setup Guide

## Quick Start

The database initialization issue has been fixed. You can now run the application using one of these methods:

### Method 1: Using the Run Script (Recommended)
```bash
python run_streamlit.py
```

### Method 2: Direct Streamlit Command
```bash
streamlit run streamlit_app.py
```

### Method 3: Python Module
```bash
python -m streamlit run streamlit_app.py
```

## What Was Fixed

1. **Database Migration**: Migrated from SQLite to MongoDB for better scalability and performance
2. **Database Initialization**: Fixed the directory creation issue that was causing the `os.makedirs` error on Windows
3. **Environment Configuration**: Made the Google API key optional so the app can run without it
4. **Error Handling**: Added better error handling for database initialization

## Configuration

### Optional: Google API Key Setup
To use the AI features, create a `.env` file in the project root with:
```
GOOGLE_API_KEY=your_actual_google_api_key_here
```

### Database
The application uses MongoDB for storing all history and activities. You need to have MongoDB installed and running.

**MongoDB Setup:**
1. Install MongoDB Community Edition from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service
3. The application will connect to `mongodb://localhost:27017/ascend` by default

**Environment Variables:**
```
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE_NAME=ascend
```

## Troubleshooting

### If you still get database errors:
1. Make sure MongoDB is installed and running
2. Check that PyMongo is installed: `pip install pymongo`
3. Verify MongoDB connection string in your environment
4. Try running with administrator privileges if on Windows

### If you get import errors:
1. Install dependencies: `pip install -r requirements.txt`
2. Make sure you're in the correct directory
3. Check that Python path includes the project directory

## Features Available

- **Without API Key**: Basic UI, database functionality, session management
- **With API Key**: Full AI-powered features including assessments, scheduling, and content generation

## Accessing the Application

Once running, the application will be available at:
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501 (if configured)

## Stopping the Application

Press `Ctrl+C` in the terminal to stop the Streamlit server.
