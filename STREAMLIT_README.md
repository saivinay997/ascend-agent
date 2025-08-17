# Ascend Streamlit UI

A comprehensive web interface for the Ascend Adaptive Student Companion system, built with Streamlit and powered by Google's Gemini LLM.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **Google API Key** for Gemini (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))
3. **Dependencies** installed

### Installation & Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

3. **Run the application:**
   ```bash
   # Option 1: Use the launcher script (recommended)
   python run_streamlit.py
   
   # Option 2: Run directly with Streamlit
   streamlit run streamlit_app.py
   ```

4. **Access the UI:**
   - The application will automatically open in your browser
   - Or navigate to: http://localhost:8501

## 🎯 Features Overview

### 📊 Dashboard
- **Overview**: Welcome screen with quick stats and recent activity
- **Quick Actions**: Direct access to main features
- **System Status**: Real-time connection status and configuration info

### 📋 Student Assessment
- **Learning Preferences**: Visual, auditory, kinesthetic, and reading/writing preferences
- **Academic Commitments**: Course management with credits
- **Additional Context**: Custom notes and requirements
- **AI-Powered Analysis**: Comprehensive assessment using Gemini

### 📅 Schedule Optimization
- **Time Slot Management**: Add/remove available study times
- **Study Preferences**: Duration, breaks, energy levels
- **Optimization Options**: Customizable scheduling parameters
- **Smart Recommendations**: AI-generated schedule with tips

### 📚 Learning Materials Generation
- **Topic Specification**: Subject and difficulty level
- **Learning Style Adaptation**: Tailored content for different styles
- **Material Types**: Study guides, practice problems, summaries, etc.
- **Customization Options**: Examples, practice exercises, visual elements

### 💡 Personalized Guidance
- **Context-Aware Support**: Situation-specific advice
- **Guidance Types**: Study strategy, time management, motivation, etc.
- **Urgency Levels**: Prioritized responses based on need
- **Action Items**: Extracted actionable recommendations

### 📈 Analytics & Insights
- **Progress Tracking**: Learning analytics and metrics
- **Activity History**: Recent actions and outcomes
- **Performance Charts**: Visual progress representation
- **Data Export**: Session data management

### ⚙️ Settings & Configuration
- **System Status**: Configuration and health checks
- **Data Management**: Clear session data and export options
- **Health Monitoring**: System diagnostics and troubleshooting

## 🎨 UI Components

### Navigation
- **Sidebar Navigation**: Easy access to all features
- **Student ID Management**: Switch between different students
- **System Status Indicators**: Real-time connection status

### Forms & Inputs
- **Interactive Forms**: User-friendly input interfaces
- **Dynamic Content**: Add/remove items (courses, time slots)
- **Validation**: Input validation and error handling
- **Progress Indicators**: Loading states and feedback

### Results Display
- **Structured Output**: Organized results and recommendations
- **Expandable Sections**: Collapsible content for better organization
- **Action Items**: Highlighted actionable recommendations
- **Timestamps**: Activity tracking and history

## 🔧 Configuration

### Environment Variables
```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (with defaults)
GEMINI_MODEL=gemini-2.0-flash-lite
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=4000
```

### Customization Options
- **Model Selection**: Choose different Gemini models
- **Temperature**: Adjust creativity vs. consistency
- **Token Limits**: Control response length
- **UI Theme**: Customizable styling and colors

## 📱 Usage Guide

### Getting Started
1. **Enter Student ID**: Start by entering a student ID in the sidebar
2. **Navigate**: Use the sidebar menu to access different features
3. **Complete Forms**: Fill out the interactive forms for each feature
4. **Review Results**: Examine AI-generated recommendations and content
5. **Take Action**: Follow the provided guidance and recommendations

### Assessment Workflow
1. Go to **Assessment** page
2. Set learning preferences using sliders
3. Add academic courses and commitments
4. Provide additional context
5. Submit and review comprehensive analysis

### Schedule Optimization
1. Navigate to **Schedule** page
2. Add available time slots for each day
3. Configure study preferences and constraints
4. Set optimization options
5. Generate and review optimized schedule

### Material Generation
1. Access **Materials** page
2. Specify topic and learning style
3. Choose material type and difficulty
4. Set generation options
5. Generate and review custom content

### Guidance Requests
1. Visit **Guidance** page
2. Describe your situation or challenge
3. Select guidance type and urgency
4. Submit and receive personalized advice
5. Review action items and follow-up suggestions

## 🔍 Troubleshooting

### Common Issues

**"Gemini Not Configured" Error**
- Check that your `.env` file exists and contains `GOOGLE_API_KEY`
- Verify the API key is valid and has access to Gemini models
- Ensure billing is enabled on your Google Cloud account

**"Failed to Initialize Services" Error**
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Python version is 3.9 or higher
- Check logs for specific error messages

**"Assessment Failed" or Similar Errors**
- Verify Gemini API key is working
- Check internet connection
- Review error messages for specific issues
- Try running the health check in Settings

**UI Not Loading or Slow Performance**
- Check system resources (CPU, memory)
- Verify network connection
- Try refreshing the browser
- Check browser console for errors

### Health Check
Use the **Settings** page to run a system health check:
1. Navigate to Settings
2. Click "Run Health Check"
3. Review results and address any issues

### Debug Mode
Enable debug mode in your `.env` file:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## 🚀 Advanced Features

### Session Management
- **Data Persistence**: Session state maintains data across page navigation
- **Student Switching**: Easily switch between different students
- **Data Export**: Export session data for external analysis

### Real-time Updates
- **Live Status**: Real-time system status indicators
- **Progress Tracking**: Live updates during processing
- **Error Handling**: Immediate feedback for issues

### Customization
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Theme Support**: Customizable colors and styling
- **Accessibility**: Keyboard navigation and screen reader support

## 📊 Data Flow

### Input Processing
1. **Form Validation**: Client-side input validation
2. **Data Preparation**: Structured data formatting
3. **API Integration**: Gemini API calls with proper error handling
4. **Response Processing**: AI response parsing and formatting

### Output Generation
1. **Content Analysis**: AI-generated content analysis
2. **Recommendation Extraction**: Automated extraction of actionable items
3. **Formatting**: Structured display with proper formatting
4. **Storage**: Session state management for persistence

## 🔒 Security & Privacy

### Data Handling
- **Local Storage**: All data stored locally in session state
- **No External Storage**: No data sent to external databases
- **API Security**: Secure API key handling
- **Session Isolation**: Data isolated per session

### Privacy Features
- **No Data Collection**: No analytics or tracking
- **Local Processing**: All processing done locally
- **Secure API Calls**: Encrypted communication with Gemini API

## 🛠️ Development

### Running in Development Mode
```bash
# Enable debug mode
export DEBUG=true

# Run with development settings
streamlit run streamlit_app.py --server.port 8501 --server.address localhost
```

### Customization
- **Styling**: Modify CSS in the `st.markdown` section
- **Components**: Add new UI components in the `StreamlitUI` class
- **Integration**: Extend with additional services and agents

### Testing
```bash
# Run the test script
python test_gemini_integration.py

# Test specific features
# (Add your own test scripts as needed)
```

## 📈 Performance Optimization

### Best Practices
- **Efficient API Calls**: Minimize redundant API requests
- **Caching**: Implement caching for repeated requests
- **Async Processing**: Use async/await for better performance
- **Resource Management**: Proper cleanup of resources

### Monitoring
- **Response Times**: Monitor API response times
- **Error Rates**: Track and analyze error patterns
- **Usage Metrics**: Monitor feature usage and performance

## 🤝 Contributing

### Adding New Features
1. **UI Components**: Add new pages and components to `StreamlitUI`
2. **Backend Integration**: Extend services and agents
3. **Testing**: Add comprehensive tests for new features
4. **Documentation**: Update documentation for new features

### Code Style
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type hints for better code clarity
- **Docstrings**: Comprehensive documentation for all functions
- **Error Handling**: Proper exception handling and user feedback

## 📞 Support

### Getting Help
- **Documentation**: Check this README and other documentation
- **Issues**: Report bugs and request features
- **Community**: Join discussions and share experiences

### Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google AI Studio](https://makersuite.google.com/)
- [LangChain Documentation](https://python.langchain.com/)

---

**Ascend Streamlit UI** - Empowering students with an intuitive, AI-powered learning companion interface.
