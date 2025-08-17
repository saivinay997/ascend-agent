# Ascend - Adaptive Student Companion for Educational Navigation & Development

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1+-green.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Ascend is an intelligent, adaptive academic support system that leverages a sophisticated multi-agent architecture to provide personalized assistance throughout a student's academic journey. The system conducts comprehensive initial assessments, optimizes learning processes, and continuously adapts to meet each student's unique needs.

## 🎯 Key Features

### 🌐 Web Interface
- **Streamlit UI**: Modern, responsive web interface for all features
- **Interactive Forms**: User-friendly input interfaces with validation
- **Real-time Feedback**: Live updates and progress indicators
- **Cross-platform**: Works on desktop, tablet, and mobile devices

### Comprehensive Student Assessment
- **Learning Preference Analysis**: Evaluates visual, auditory, kinesthetic, and reading/writing preferences
- **Cognitive Style Assessment**: Identifies processing patterns and thinking styles
- **Academic Commitment Tracking**: Monitors current course load and extracurricular activities
- **Challenge Identification**: Pinpoints specific areas requiring support

### Multi-Agent System Architecture
- **Coordinator Agent**: Central orchestrator managing workflow and agent communication
- **Planner Agent**: Schedule optimization and time management specialist
- **Notewriter Agent**: Academic content processing and study material generation
- **Advisor Agent**: Personalized guidance and support strategy provider

### Learning Process Optimization
- **Adaptive Study Schedules**: Personalized timetables based on energy patterns and preferences
- **Customized Learning Materials**: Tailored content matching individual learning styles
- **Real-time Monitoring**: Continuous adjustment based on performance and engagement
- **Proven Learning Techniques**: Spaced repetition and active recall integration

### Resource Management & Integration
- **Academic Calendar Synchronization**: Seamless integration with existing schedules
- **Digital Learning Environment Support**: LMS and educational platform connectivity
- **Educational Resource Coordination**: Access to supplementary materials and tools

### Emergency & Support Protocols
- **Stress Detection**: Academic pressure monitoring and intervention
- **Deadline Management**: Proactive deadline tracking and support
- **Crisis Intervention**: Immediate assistance during challenging periods

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Ascend System                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Coordinator │    │   Planner   │    │ Notewriter  │     │
│  │   Agent     │    │   Agent     │    │   Agent     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                   │                   │           │
│         └───────────────────┼───────────────────┘           │
│                             │                               │
│                    ┌─────────▼─────────┐                    │
│                    │   Advisor Agent   │                    │
│                    └───────────────────┘                    │
├─────────────────────────────────────────────────────────────┤
│                LangGraph Workflow Engine                    │
├─────────────────────────────────────────────────────────────┤
│              State Management System                        │
├─────────────────────────────────────────────────────────────┤
│              External Integrations                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Academic  │  │     LMS     │  │ Educational │         │
│  │   Calendar  │  │  Platforms  │  │  Resources  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Google API key for Gemini
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ascend-agent.git
   cd ascend-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Run the system**

   **Option A: Streamlit Web UI (Recommended)**
   ```bash
   # Use the launcher script
   python run_streamlit.py
   
   # Or run directly
   streamlit run streamlit_app.py
   ```
   
   **Option B: Command Line Interface**
   ```bash
   python main.py --mode cli --command assess --student-id test123
   ```
   
   **Option C: API Server**
   ```bash
   python main.py --mode server
   ```

## 📁 Project Structure

```
ascend-agent/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── main.py                  # Main application entry point
├── streamlit_app.py         # Streamlit web UI
├── run_streamlit.py         # Streamlit launcher script
├── demo_streamlit.py        # Demo UI with sample data
├── test_gemini_integration.py # Gemini integration test
├── GEMINI_SETUP.md          # Gemini setup guide
├── STREAMLIT_README.md      # Streamlit UI documentation
├── config/
│   ├── __init__.py
│   ├── settings.py          # Application configuration
│   └── logging_config.py    # Logging configuration
├── agents/
│   ├── __init__.py
│   ├── base_agent.py        # Base agent class
│   ├── coordinator.py       # Coordinator agent implementation
│   ├── planner.py           # Planner agent implementation
│   ├── notewriter.py        # Notewriter agent implementation
│   └── advisor.py           # Advisor agent implementation
├── workflows/
│   ├── __init__.py
│   ├── main_workflow.py     # Main LangGraph workflow
│   └── state_manager.py     # State management system
├── models/
│   ├── __init__.py
│   ├── base.py              # Base model and timestamp mixin
│   ├── user_history.py      # User history and query storage models
│   ├── student_profile.py   # Student profile data model
│   ├── assessment.py        # Assessment data models
│   └── learning_materials.py # Learning material models
├── services/
│   ├── __init__.py
│   ├── database_service.py   # Database and user history management
│   ├── assessment_service.py # Assessment logic
│   ├── schedule_service.py   # Schedule management
│   ├── content_service.py    # Content generation
│   └── integration_service.py # External integrations
├── utils/
│   ├── __init__.py
│   ├── helpers.py           # Utility functions
│   └── validators.py        # Data validation
├── tests/
│   ├── __init__.py
│   ├── test_agents.py       # Agent tests
│   ├── test_workflows.py    # Workflow tests
│   └── test_services.py     # Service tests
└── docs/
    ├── api.md               # API documentation
    ├── deployment.md        # Deployment guide
    └── contributing.md      # Contribution guidelines
```

## 🚀 Features

### 📋 Student Assessment
- **Learning Style Analysis**: Comprehensive assessment of visual, auditory, kinesthetic, and reading/writing preferences
- **Academic Commitments**: Track courses, credits, and academic workload
- **Personalized Recommendations**: AI-generated study strategies and learning approaches
- **Progress Tracking**: Monitor learning style evolution over time

### 📅 Schedule Optimization
- **Time Slot Management**: Define available study times and constraints
- **Study Preferences**: Configure duration, breaks, and energy levels
- **Smart Optimization**: AI-powered schedule generation with breaks and prioritization
- **Flexible Constraints**: Adapt to individual preferences and limitations

### 📚 Learning Materials Generation
- **Topic-Specific Content**: Generate materials for any subject or concept
- **Learning Style Adaptation**: Tailored content for different learning preferences
- **Material Types**: Study guides, practice problems, summaries, concept maps, video scripts
- **Customization Options**: Examples, practice exercises, visual elements, adaptive content

### 💡 Personalized Guidance
- **Context-Aware Support**: Situation-specific advice and recommendations
- **Guidance Types**: Study strategy, time management, motivation, exam preparation
- **Urgency Levels**: Prioritized responses based on immediate needs
- **Action Items**: Extracted actionable recommendations and next steps

### 📈 Analytics & Insights
- **Progress Tracking**: Learning analytics and performance metrics
- **Activity History**: Recent actions and outcomes tracking
- **Performance Charts**: Visual representation of learning progress
- **Data Export**: Session data management and export capabilities

### 📜 User History & Statistics
- **Comprehensive History**: Store all user interactions and queries
- **User Statistics**: Success rates, processing times, and usage metrics
- **History Filtering**: Filter by type (assessment, schedule, material, guidance)
- **Data Export**: Export complete history to JSON format
- **Data Management**: Clear specific history types or all data

### ⚙️ Settings & Configuration
- **System Status**: Configuration and health monitoring
- **Data Management**: Clear session data and export options
- **Health Monitoring**: System diagnostics and troubleshooting

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# LLM Configuration
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.0-flash-lite
GEMINI_TEMPERATURE=0.7

# Database Configuration
DATABASE_URL=sqlite:///ascend.db

# External Integrations
CALENDAR_API_KEY=your_calendar_api_key
LMS_API_KEY=your_lms_api_key

# Logging
LOG_LEVEL=INFO
LOG_FILE=ascend.log

# System Configuration
MAX_CONCURRENT_SESSIONS=10
SESSION_TIMEOUT=3600
```

## 📊 Usage Examples

### Initial Assessment
```python
from ascend.workflows.main_workflow import AscendWorkflow

# Initialize the system
workflow = AscendWorkflow()

# Conduct initial assessment
assessment_result = workflow.conduct_assessment(
    student_id="student_123",
    learning_preferences={
        "visual": 0.8,
        "auditory": 0.6,
        "kinesthetic": 0.4,
        "reading": 0.7
    },
    academic_commitments=[
        {"course": "Mathematics 101", "credits": 3},
        {"course": "Physics 101", "credits": 4}
    ]
)
```

### Schedule Optimization
```python
# Generate personalized schedule
schedule = workflow.optimize_schedule(
    student_id="student_123",
    available_time_slots=[
        {"day": "Monday", "start": "09:00", "end": "17:00"},
        {"day": "Tuesday", "start": "10:00", "end": "16:00"}
    ]
)
```

### Learning Material Generation
```python
# Generate customized study materials
materials = workflow.generate_materials(
    student_id="student_123",
    topic="Calculus Derivatives",
    learning_style="visual"
)
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/test_agents.py
python -m pytest tests/test_workflows.py
python -m pytest tests/test_services.py

# Run with coverage
python -m pytest --cov=ascend tests/
```

## 📈 Performance Monitoring

The system includes comprehensive monitoring capabilities:

- **Agent Performance Metrics**: Response times, success rates, error tracking
- **Student Progress Tracking**: Learning outcomes, engagement levels
- **System Health Monitoring**: Resource usage, API response times
- **Adaptation Effectiveness**: Strategy success rates and improvement metrics

## 🔒 Security & Privacy

- **Data Encryption**: All student data is encrypted at rest and in transit
- **Access Control**: Role-based permissions and authentication
- **Audit Logging**: Comprehensive activity tracking
- **GDPR Compliance**: Data protection and privacy controls
- **API Security**: Rate limiting and input validation

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `python -m pytest tests/`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangGraph Team**: For the excellent workflow framework
- **Google**: For providing the underlying Gemini LLM capabilities
- **Academic Community**: For research and best practices in adaptive learning

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/ascend-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ascend-agent/discussions)
- **Email**: support@ascend-edu.com

## 🔮 Roadmap

### Phase 1 (Current)
- [x] Multi-agent system architecture
- [x] Basic assessment framework
- [x] Schedule optimization
- [x] Learning material generation

### Phase 2 (Next)
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Integration with more LMS platforms
- [ ] Peer learning features

### Phase 3 (Future)
- [ ] AI-powered tutoring sessions
- [ ] Virtual study groups
- [ ] Career guidance integration
- [ ] Research collaboration tools

---

**Ascend** - Empowering students to reach their full potential through intelligent, adaptive academic support.