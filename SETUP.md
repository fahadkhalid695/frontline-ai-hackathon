# 🚀 Frontline Worker AI System - Local Setup Guide

This guide will help you set up and run the complete Frontline Worker AI System locally with a beautiful UI.

## 📋 Prerequisites

### Required Software
- **Python 3.11+** - [Download here](https://python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### Optional (for Docker setup)
- **Docker** - [Download here](https://docker.com/get-started)
- **Docker Compose** - Usually included with Docker Desktop

## 🎯 Quick Start Options

### Option 1: Automatic Setup (Recommended)

#### For Windows:
```bash
# Double-click or run in Command Prompt
start-local.bat
```

#### For macOS/Linux:
```bash
# Make script executable and run
chmod +x start-local.sh
./start-local.sh
```

### Option 2: Docker Setup
```bash
# Make script executable and run
chmod +x start-docker.sh
./start-docker.sh
```

### Option 3: Manual Setup

#### Step 1: Clone and Setup Backend
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-local.txt

# Create data directory
mkdir data
```

#### Step 2: Setup Frontend
```bash
cd frontend
npm install
cd ..
```

#### Step 3: Start Services
```bash
# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

## 🌐 Access Points

Once running, you can access:

- **🎨 Frontend UI**: http://localhost:3000
- **🔧 Backend API**: http://localhost:5000
- **❤️ Health Check**: http://localhost:5000/health
- **🧪 Test Agents**: http://localhost:5000/api/test-agents

## 🧪 Testing the System

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Test Individual Agent
```bash
curl -X POST http://localhost:5000/api/emergency \
  -H "Content-Type: application/json" \
  -d '{
    "action": "triage",
    "case_data": {
      "symptoms": "chest pain",
      "emergency_type": "medical",
      "location": "Lahore"
    }
  }'
```

### 3. Test Complete Workflow
```bash
curl -X POST http://localhost:5000/api/emergency \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "severe chest pain",
      "emergency_type": "medical",
      "location": "Lahore",
      "citizen_data": {
        "name": "Test Patient",
        "age": 45,
        "phone": "+923001234567"
      }
    }
  }'
```

## 🎨 UI Features

The beautiful web interface includes:

### 🏠 Main Dashboard
- Emergency hotlines banner
- System status indicator
- Beautiful gradient backgrounds
- Responsive design

### 📝 Emergency Form
- Multi-step form with validation
- Emergency type selection (Medical/Police/Fire)
- Dynamic fields based on emergency type
- Medical conditions and allergies tracking
- Pakistan cities dropdown

### ⚡ Real-time Processing
- Animated agent progress indicators
- Live status updates
- Processing timeline
- Beautiful loading animations

### 📊 Results Display
- Comprehensive results panel
- Priority assessment with color coding
- Service recommendations
- Appointment scheduling details
- Follow-up and reminder information
- Tracking system integration

## 🔧 System Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (Next.js)     │◄──►│   (Flask)       │
│   Port: 3000    │    │   Port: 5000    │
└─────────────────┘    └─────────────────┘
         │                       │
         │                       ▼
         │              ┌─────────────────┐
         │              │   AI Agents     │
         │              │   - Triage      │
         │              │   - Guidance    │
         │              │   - Booking     │
         │              │   - Follow-up   │
         │              └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   UI Components │    │   Data Layer    │
│   - Forms       │    │   - Mock Data   │
│   - Progress    │    │   - Hospitals   │
│   - Results     │    │   - Locations   │
└─────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
frontline-ai-system/
├── 🎨 frontend/                 # Next.js Frontend
│   ├── app/
│   │   ├── components/         # React Components
│   │   │   ├── EmergencyForm.tsx
│   │   │   ├── AgentProgress.tsx
│   │   │   ├── ResultsPanel.tsx
│   │   │   └── StatusDisplay.tsx
│   │   ├── globals.css         # Global Styles
│   │   ├── layout.tsx          # App Layout
│   │   └── page.tsx            # Main Page
│   ├── package.json
│   └── tailwind.config.js
│
├── 🤖 agents/                   # AI Agents
│   ├── triage_agent.py
│   ├── guidance_agent.py
│   ├── booking_agent.py
│   └── followup_agent.py
│
├── 🛠️ utils/                    # Utilities
│   ├── data_loader.py
│   └── degraded_mode.py
│
├── 📊 data/                     # Mock Data
│   ├── frontline_worker_requests_clean_2_20.json
│   └── pakistan.csv
│
├── 🚀 Backend Files
│   ├── app.py                  # Flask Backend
│   ├── main.py                 # Cloud Function
│   ├── config.py               # Configuration
│   └── requirements.txt
│
└── 🔧 Setup Files
    ├── start-local.sh          # Linux/Mac Startup
    ├── start-local.bat         # Windows Startup
    ├── docker-compose.yml      # Docker Setup
    └── SETUP.md               # This Guide
```

## 🎯 Key Features Implemented

### ✅ Complete AI Agent System
- **Triage Agent**: Symptom analysis and priority assessment
- **Guidance Agent**: Service matching and routing
- **Booking Agent**: Appointment scheduling and form filling
- **Follow-up Agent**: Reminders and progress tracking

### ✅ Beautiful Web Interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Live progress tracking
- **Smooth Animations**: Framer Motion animations
- **Modern UI**: Tailwind CSS with custom components

### ✅ Production-Ready Backend
- **Flask API**: RESTful endpoints
- **CORS Enabled**: Frontend-backend communication
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed system logging

### ✅ Local Development
- **Hot Reload**: Both frontend and backend
- **Mock Data**: Realistic test datasets
- **Easy Setup**: One-command startup
- **Docker Support**: Containerized deployment

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Kill processes on ports 3000 and 5000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:3000 | xargs kill -9
lsof -ti:5000 | xargs kill -9
```

#### Python Virtual Environment Issues
```bash
# Delete and recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-local.txt
```

#### Node.js Dependencies Issues
```bash
# Clear npm cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Backend Not Starting
```bash
# Check Python version
python --version  # Should be 3.11+

# Check if all dependencies are installed
pip list

# Run with debug mode
python app.py
```

### Getting Help

If you encounter issues:

1. **Check the logs** in the terminal where you started the services
2. **Verify all prerequisites** are installed correctly
3. **Try the Docker setup** if local setup fails
4. **Check port availability** (3000 and 5000)

## 🚀 Next Steps

Once you have the system running:

1. **Test the UI** by submitting different emergency scenarios
2. **Explore the API** using the provided curl commands
3. **Customize the agents** by modifying the Python files
4. **Enhance the UI** by updating the React components
5. **Deploy to production** using the provided deployment scripts

## 📞 Support

For additional help:
- Check the main README.md for API documentation
- Review the agent code for customization options
- Test individual components using the provided endpoints

---

**🎉 Congratulations! You now have a complete, beautiful, and functional Frontline Worker AI System running locally!**