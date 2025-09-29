# 🚀 Frontline Worker AI System

[![Deploy Status](https://img.shields.io/badge/deploy-active-brightgreen)](https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://python.org)
[![Google Cloud](https://img.shields.io/badge/platform-Google%20Cloud-orange)](https://cloud.google.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> **Intelligent Multi-Agent Emergency Response System for Pakistan's Frontline Workers**

An AI-powered orchestration system that streamlines emergency response workflows through intelligent triage, service guidance, appointment booking, and follow-up management. Built specifically for Pakistan's emergency services ecosystem.

## 🎯 Overview

The Frontline Worker AI System revolutionizes emergency response by deploying four specialized AI agents that work together to provide comprehensive support from initial triage to follow-up care. The system operates in both enhanced (AI-powered) and degraded (rule-based) modes to ensure reliability even in challenging conditions.

### ✨ Key Features

- **🧠 Intelligent Triage**: AI-powered priority assessment with fallback rule-based system
- **🎯 Smart Service Matching**: Context-aware routing to appropriate emergency services
- **📅 Automated Booking**: Seamless appointment scheduling with form pre-filling
- **📞 Proactive Follow-up**: Automated reminders and progress tracking
- **🔄 Degraded Mode Support**: Continues operation even when AI services are unavailable
- **🌍 Pakistan-Focused**: Tailored for Pakistani emergency services and healthcare system

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontline Worker AI System                   │
├─────────────────────────────────────────────────────────────────┤
│                     Cloud Function Entry Point                  │
│                        (main.py)                               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Orchestrator                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │   Triage    │  │  Guidance   │  │   Booking   │  │Follow-up│ │
│  │   Agent     │→ │   Agent     │→ │   Agent     │→ │ Agent   │ │
│  │             │  │             │  │             │  │         │ │
│  │ • Priority  │  │ • Service   │  │ • Appoint.  │  │ • Remind│ │
│  │ • Urgency   │  │   Matching  │  │ • Forms     │  │ • Track │ │
│  │ • Risk      │  │ • Routing   │  │ • Confirm   │  │ • Plan  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Support Systems                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Data Loader │  │System Status│  │   Config    │              │
│  │             │  │  Checker    │  │  Manager    │              │
│  │ • Hospitals │  │ • AI Status │  │ • Services  │              │
│  │ • Locations │  │ • Degraded  │  │ • Contacts  │              │
│  │ • Protocols │  │   Mode      │  │ • Settings  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
frontline-ai-system/
├── 📄 main.py                    # Cloud Function entry point & orchestrator
├── ⚙️ config.py                  # System configuration & settings
├── 📋 requirements.txt           # Python dependencies
├── 🚀 deploy.sh                  # Deployment script
├── 🧪 test_system.py             # Comprehensive test suite
├── 📖 README.md                  # This documentation
│
├── 🤖 agents/                    # AI Agent implementations
│   ├── triage_agent.py          # Emergency priority assessment
│   ├── guidance_agent.py        # Service matching & routing
│   ├── booking_agent.py         # Appointment & form management
│   └── followup_agent.py        # Reminders & progress tracking
│
└── 🛠️ utils/                     # Utility modules
    ├── data_loader.py           # Dataset integration & management
    └── degraded_mode.py         # Offline operation support
```

## 🚀 Quick Start

### 🏠 Local Development (Recommended)

#### Option 1: One-Command Setup
```bash
# Windows
start-local.bat

# Linux/Mac
chmod +x start-local.sh
./start-local.sh
```

#### Option 2: Docker Setup
```bash
chmod +x start-docker.sh
./start-docker.sh
```

#### Option 3: Manual Setup
```bash
# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-local.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

**Access Points:**
- 🎨 **Beautiful UI**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:5000
- ❤️ **Health Check**: http://localhost:5000/health

### 🌐 Cloud Testing

#### Health Check
```bash
curl "https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai/health"
```

#### Simple Triage Test
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{"action":"triage","case_data":{"symptoms":"fever"}}'
```

#### Complete Workflow Test
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{"action":"full_workflow","case_data":{"symptoms":"chest pain","emergency_type":"medical","location":"Lahore"}}'
```

## 🧪 Comprehensive Testing Guide

### 1. Health Check
Verify system availability:
```bash
curl "https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai/health"
```

### 2. Individual Agent Testing

#### Triage Agent Only
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "triage",
    "case_data": {
      "symptoms": "chest pain and difficulty breathing",
      "emergency_type": "medical",
      "location": "Lahore"
    }
  }'
```

#### Guidance Agent Only
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "guidance",
    "case_data": {
      "priority": "high",
      "emergency_type": "medical",
      "location": "Karachi"
    }
  }'
```

#### Booking Agent Only
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "booking",
    "case_data": {
      "service_name": "Jinnah Hospital",
      "priority": "medium",
      "citizen_data": {
        "name": "Ali Ahmed",
        "phone": "+923001234567"
      }
    }
  }'
```

#### Follow-up Agent Only
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "followup",
    "case_data": {
      "appointment_time": "2024-09-28T10:00:00",
      "service_type": "medical",
      "citizen_contact": {
        "phone": "+923001234567"
      }
    }
  }'
```

### 3. Complete Workflow Testing

#### High-Priority Medical Emergency
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "severe chest pain radiating to left arm",
      "emergency_type": "medical",
      "location": "Islamabad",
      "citizen_data": {
        "name": "Mr. Asif Khan",
        "age": 58,
        "phone": "+923331234567",
        "medical_conditions": ["hypertension", "diabetes"]
      }
    }
  }'
```

#### Medium-Priority Case
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "high fever with cough for 3 days",
      "emergency_type": "medical",
      "location": "Rawalpindi",
      "citizen_data": {
        "name": "Ms. Ayesha Ahmed",
        "age": 25,
        "phone": "+923332223344"
      }
    }
  }'
```

#### Police Emergency
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "robbery incident with threat",
      "emergency_type": "police",
      "location": "Karachi",
      "citizen_data": {
        "name": "Mr. Raza",
        "phone": "+923334445556",
        "incident_details": "Armed robbery at store"
      }
    }
  }'
```

### 4. Degraded Mode Testing
Simulate offline operation:
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "triage",
    "case_data": {
      "symptoms": "minor cut on finger",
      "emergency_type": "medical",
      "location": "Remote Village"
    },
    "force_degraded": true
  }'
```

### 5. Enhanced Testing with Pretty Output

#### Format JSON Responses
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "triage",
    "case_data": {
      "symptoms": "broken arm from fall",
      "emergency_type": "medical",
      "location": "Lahore"
    }
  }' | python -m json.tool
```

#### Save Response to File
```bash
curl -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "heart palpitations",
      "emergency_type": "medical",
      "location": "Lahore",
      "citizen_data": {
        "name": "Test Patient",
        "age": 45
      }
    }
  }' > response.json

# View the saved response
cat response.json | python -m json.tool
```

### 6. Automated Test Script

Create `test_agents.sh`:
```bash
#!/bin/bash

BASE_URL="https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai"

echo "🚀 Testing Frontline Worker AI Agents"
echo "======================================"

# Health check
echo "1. Health Check:"
curl -s "$BASE_URL/health" | python -m json.tool
echo

# Triage agent
echo "2. Triage Agent Test:"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "triage",
    "case_data": {
      "symptoms": "chest pain",
      "emergency_type": "medical",
      "location": "Lahore"
    }
  }' | python -m json.tool
echo

# Full workflow
echo "3. Full Workflow Test:"
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "high fever and vomiting",
      "emergency_type": "medical",
      "location": "Karachi",
      "citizen_data": {
        "name": "Test User",
        "age": 30
      }
    }
  }' | python -m json.tool
```

Make executable and run:
```bash
chmod +x test_agents.sh
./test_agents.sh
```

## 📊 Expected Response Formats

### Successful Triage Response
```json
{
  "status": "success",
  "action": "triage",
  "result": {
    "priority": "high",
    "urgency": "immediate",
    "assessment_method": "rule_based",
    "agent": "triage",
    "agent_trace": ["triage_agent"]
  }
}
```

### Full Workflow Response
```json
{
  "status": "success",
  "action": "full_workflow",
  "result": {
    "priority": "high",
    "urgency": "immediate",
    "recommended_service": "General Hospital Emergency",
    "appointment_time": "2024-09-27T14:30:00",
    "confirmation_number": "CNF-12345",
    "reminders_scheduled": 2,
    "agent_trace": ["triage_agent", "guidance_agent", "booking_agent", "followup_agent"],
    "workflow_complete": true
  }
}
```

## 🔧 Troubleshooting

### Check Service Accessibility
```bash
curl -I "https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai/health"
```

### Verbose Output for Debugging
```bash
curl -v -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{"action":"triage","case_data":{"symptoms":"fever"}}'
```

### Check Function Logs (if you have access)
```bash
gcloud functions logs read frontline-ai --limit=10
```

## 🎯 One-Command Demo

Test the complete system with a single command:
```bash
curl -s -X POST https://us-central1-frontline-ai-hackathon.cloudfunctions.net/frontline-ai \
  -H "Content-Type: application/json" \
  -d '{
    "action": "full_workflow",
    "case_data": {
      "symptoms": "severe accident injuries",
      "emergency_type": "medical",
      "location": "Islamabad",
      "citizen_data": {
        "name": "Demo Patient",
        "age": 35,
        "phone": "+923001234567"
      }
    }
  }' | python -c "
import sys, json
data = json.load(sys.stdin)
print('🎯 FRONTLINE AI DEMO RESULTS:')
print('Status:', data.get('status'))
print('Priority:', data['result'].get('priority'))
print('Service:', data['result'].get('recommended_service'))
print('Appointment:', data['result'].get('appointment_time'))
print('Agents:', ' → '.join(data['result'].get('agent_trace', [])))
"
```

## 🚀 Deployment

### Prerequisites
- Google Cloud SDK installed
- Project ID: `frontline-ai-hackathon`
- Required APIs enabled (Cloud Functions, Firestore)

### Deploy to Google Cloud
```bash
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment
```bash
gcloud functions deploy frontline-ai \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=frontline_ai \
  --trigger-http \
  --allow-unauthenticated \
  --memory=512MB \
  --timeout=300s
```

## 🧪 Local Testing

### Verify Setup
```bash
python verify-setup.py
```

### Test Complete System
```bash
python test_system.py
```

### Test Individual Components
```bash
# Test backend health
curl http://localhost:5000/health

# Test all agents
curl http://localhost:5000/api/test-agents

# Test emergency workflow
curl -X POST http://localhost:5000/api/emergency \
  -H "Content-Type: application/json" \
  -d '{"action":"full_workflow","case_data":{"symptoms":"chest pain","emergency_type":"medical","location":"Lahore","citizen_data":{"name":"Test","age":30,"phone":"+923001234567"}}}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

For support and questions:
- 📧 Email: support@frontline-ai.gov.pk
- 📞 Emergency Hotline: 1122 (Medical), 15 (Police)
- 🌐 Documentation: [docs.frontline-ai.gov.pk](https://docs.frontline-ai.gov.pk)

---

**Built with ❤️ for Pakistan's Frontline Workers**