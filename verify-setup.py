#!/usr/bin/env python3
"""
Verification script for Frontline Worker AI System
Checks if all components are properly set up and working
"""

import os
import sys
import subprocess
import json
import time
import requests
from pathlib import Path

def print_status(message, status="info"):
    """Print colored status messages"""
    colors = {
        "info": "\033[94m",      # Blue
        "success": "\033[92m",   # Green
        "warning": "\033[93m",   # Yellow
        "error": "\033[91m",     # Red
        "reset": "\033[0m"       # Reset
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    print(f"{colors[status]}{icons[status]} {message}{colors['reset']}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_status(f"{description}: Found", "success")
        return True
    else:
        print_status(f"{description}: Missing", "error")
        return False

def check_directory_structure():
    """Check if all required directories and files exist"""
    print_status("Checking project structure...", "info")
    
    required_files = [
        ("app.py", "Flask backend"),
        ("main.py", "Cloud function entry point"),
        ("config.py", "Configuration file"),
        ("requirements.txt", "Python dependencies"),
        ("requirements-local.txt", "Local development dependencies"),
        ("agents/triage_agent.py", "Triage agent"),
        ("agents/guidance_agent.py", "Guidance agent"),
        ("agents/booking_agent.py", "Booking agent"),
        ("agents/followup_agent.py", "Follow-up agent"),
        ("utils/data_loader.py", "Data loader utility"),
        ("utils/degraded_mode.py", "Degraded mode utility"),
        ("data/frontline_worker_requests_clean_2_20.json", "Mock emergency data"),
        ("data/pakistan.csv", "Pakistan cities data"),
        ("frontend/package.json", "Frontend dependencies"),
        ("frontend/app/page.tsx", "Main frontend page"),
        ("frontend/app/components/EmergencyForm.tsx", "Emergency form component"),
        ("frontend/app/components/AgentProgress.tsx", "Agent progress component"),
        ("frontend/app/components/ResultsPanel.tsx", "Results panel component"),
        ("docker-compose.yml", "Docker compose configuration"),
        ("start-local.sh", "Linux/Mac startup script"),
        ("start-local.bat", "Windows startup script"),
    ]
    
    all_exist = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_python_dependencies():
    """Check if Python dependencies are installed"""
    print_status("Checking Python dependencies...", "info")
    
    required_packages = [
        "flask",
        "flask_cors", 
        "requests",
        "pandas",
        "PyPDF2"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print_status(f"Python package '{package}': Installed", "success")
        except ImportError:
            print_status(f"Python package '{package}': Missing", "error")
            missing_packages.append(package)
    
    if missing_packages:
        print_status("Install missing packages with: pip install -r requirements-local.txt", "warning")
        return False
    
    return True

def check_node_dependencies():
    """Check if Node.js dependencies are installed"""
    print_status("Checking Node.js dependencies...", "info")
    
    if not os.path.exists("frontend/node_modules"):
        print_status("Node.js dependencies: Not installed", "error")
        print_status("Run: cd frontend && npm install", "warning")
        return False
    else:
        print_status("Node.js dependencies: Installed", "success")
        return True

def test_backend_startup():
    """Test if backend can start properly"""
    print_status("Testing backend startup...", "info")
    
    try:
        # Import main modules to check for syntax errors
        sys.path.append('.')
        from agents.triage_agent import TriageAgent
        from agents.guidance_agent import GuidanceAgent
        from agents.booking_agent import BookingAgent
        from agents.followup_agent import FollowupAgent
        from utils.data_loader import DataLoader
        from utils.degraded_mode import SystemStatusChecker
        
        print_status("All agent modules: Import successful", "success")
        
        # Test data loader
        data_loader = DataLoader()
        print_status(f"Data loader: {len(data_loader.loaded_datasets)} datasets loaded", "success")
        
        # Test system checker
        system_checker = SystemStatusChecker()
        status = system_checker.get_system_status()
        print_status(f"System status: {status['mode']} mode", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Backend startup test failed: {str(e)}", "error")
        return False

def test_agents_functionality():
    """Test if all agents work properly"""
    print_status("Testing agent functionality...", "info")
    
    try:
        sys.path.append('.')
        from agents.triage_agent import TriageAgent
        from agents.guidance_agent import GuidanceAgent
        from agents.booking_agent import BookingAgent
        from agents.followup_agent import FollowupAgent
        from utils.data_loader import DataLoader
        from utils.degraded_mode import SystemStatusChecker
        
        data_loader = DataLoader()
        system_checker = SystemStatusChecker()
        system_status = system_checker.get_system_status()
        
        test_case = {
            "symptoms": "chest pain and difficulty breathing",
            "emergency_type": "medical",
            "location": "Lahore",
            "citizen_data": {
                "name": "Test Patient",
                "age": 45,
                "phone": "+923001234567"
            }
        }
        
        # Test Triage Agent
        triage_agent = TriageAgent(data_loader)
        triage_result = triage_agent.process(test_case, system_status)
        print_status("Triage Agent: Working", "success")
        
        # Test Guidance Agent
        guidance_agent = GuidanceAgent(data_loader)
        guidance_data = {**test_case, **triage_result}
        guidance_result = guidance_agent.process(guidance_data, system_status)
        print_status("Guidance Agent: Working", "success")
        
        # Test Booking Agent
        booking_agent = BookingAgent(data_loader)
        booking_data = {**guidance_data, **guidance_result}
        booking_result = booking_agent.process(booking_data, system_status)
        print_status("Booking Agent: Working", "success")
        
        # Test Follow-up Agent
        followup_agent = FollowupAgent(data_loader)
        followup_data = {**booking_data, **booking_result}
        followup_result = followup_agent.process(followup_data, system_status)
        print_status("Follow-up Agent: Working", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Agent functionality test failed: {str(e)}", "error")
        return False

def check_data_integrity():
    """Check if data files are valid"""
    print_status("Checking data file integrity...", "info")
    
    try:
        # Check JSON data
        with open('data/frontline_worker_requests_clean_2_20.json', 'r') as f:
            emergency_data = json.load(f)
            print_status(f"Emergency requests data: {len(emergency_data)} records", "success")
        
        # Check CSV data
        try:
            import pandas as pd
            pakistan_data = pd.read_csv('data/pakistan.csv')
            print_status(f"Pakistan cities data: {len(pakistan_data)} cities", "success")
        except ImportError:
            # Fallback CSV reading
            import csv
            with open('data/pakistan.csv', 'r') as f:
                reader = csv.DictReader(f)
                pakistan_data = list(reader)
            print_status(f"Pakistan cities data: {len(pakistan_data)} cities (CSV fallback)", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Data integrity check failed: {str(e)}", "error")
        return False

def generate_setup_report():
    """Generate a comprehensive setup report"""
    print_status("=" * 60, "info")
    print_status("FRONTLINE WORKER AI SYSTEM - SETUP VERIFICATION", "info")
    print_status("=" * 60, "info")
    
    checks = [
        ("Project Structure", check_directory_structure),
        ("Python Dependencies", check_python_dependencies),
        ("Node.js Dependencies", check_node_dependencies),
        ("Data Integrity", check_data_integrity),
        ("Backend Startup", test_backend_startup),
        ("Agent Functionality", test_agents_functionality),
    ]
    
    results = {}
    all_passed = True
    
    for check_name, check_function in checks:
        print_status(f"\n--- {check_name} ---", "info")
        try:
            result = check_function()
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print_status(f"Check failed with error: {str(e)}", "error")
            results[check_name] = False
            all_passed = False
    
    # Summary
    print_status("\n" + "=" * 60, "info")
    print_status("SETUP VERIFICATION SUMMARY", "info")
    print_status("=" * 60, "info")
    
    for check_name, result in results.items():
        status = "success" if result else "error"
        print_status(f"{check_name}: {'PASSED' if result else 'FAILED'}", status)
    
    if all_passed:
        print_status("\n🎉 ALL CHECKS PASSED! Your system is ready to run.", "success")
        print_status("\nNext steps:", "info")
        print_status("1. Run: python app.py (in one terminal)", "info")
        print_status("2. Run: cd frontend && npm run dev (in another terminal)", "info")
        print_status("3. Open: http://localhost:3000", "info")
        print_status("\nOr use the startup scripts:", "info")
        print_status("- Windows: start-local.bat", "info")
        print_status("- Linux/Mac: ./start-local.sh", "info")
    else:
        print_status("\n❌ SOME CHECKS FAILED. Please fix the issues above.", "error")
        print_status("\nCommon solutions:", "warning")
        print_status("- Install Python dependencies: pip install -r requirements-local.txt", "warning")
        print_status("- Install Node.js dependencies: cd frontend && npm install", "warning")
        print_status("- Check Python version: python --version (should be 3.11+)", "warning")
        print_status("- Check Node.js version: node --version (should be 18+)", "warning")
    
    return all_passed

if __name__ == "__main__":
    generate_setup_report()