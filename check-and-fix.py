#!/usr/bin/env python3
"""
Comprehensive error checking and fixing script for Frontline Worker AI System
"""

import os
import sys
import json
import subprocess
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

def check_python_syntax():
    """Check Python files for syntax errors"""
    print_status("Checking Python syntax...", "info")
    
    python_files = [
        "app.py", "main.py", "config.py", "verify-setup.py",
        "agents/triage_agent.py", "agents/guidance_agent.py", 
        "agents/booking_agent.py", "agents/followup_agent.py",
        "utils/data_loader.py", "utils/degraded_mode.py"
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), file_path, 'exec')
                print_status(f"Syntax check {file_path}: OK", "success")
            except SyntaxError as e:
                print_status(f"Syntax error in {file_path}: {e}", "error")
                syntax_errors.append((file_path, str(e)))
            except Exception as e:
                print_status(f"Error reading {file_path}: {e}", "warning")
        else:
            print_status(f"File not found: {file_path}", "error")
    
    return len(syntax_errors) == 0

def check_imports():
    """Check if all imports can be resolved"""
    print_status("Checking import statements...", "info")
    
    try:
        # Add current directory to path
        sys.path.insert(0, '.')
        
        # Test critical imports
        import agents.triage_agent
        import agents.guidance_agent
        import agents.booking_agent
        import agents.followup_agent
        import utils.data_loader
        import utils.degraded_mode
        
        print_status("All imports: OK", "success")
        return True
        
    except ImportError as e:
        print_status(f"Import error: {e}", "error")
        return False
    except Exception as e:
        print_status(f"Unexpected error during import check: {e}", "error")
        return False

def check_json_files():
    """Check JSON files for validity"""
    print_status("Checking JSON files...", "info")
    
    json_files = [
        "data/frontline_worker_requests_clean_2_20.json",
        "frontend/package.json"
    ]
    
    all_valid = True
    
    for file_path in json_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json.load(f)
                print_status(f"JSON check {file_path}: OK", "success")
            except json.JSONDecodeError as e:
                print_status(f"JSON error in {file_path}: {e}", "error")
                all_valid = False
        else:
            print_status(f"JSON file not found: {file_path}", "warning")
    
    return all_valid

def check_data_files():
    """Check if data files exist and are readable"""
    print_status("Checking data files...", "info")
    
    required_files = [
        "data/frontline_worker_requests_clean_2_20.json",
        "data/pakistan.csv"
    ]
    
    all_exist = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if len(content) > 0:
                        print_status(f"Data file {file_path}: OK ({len(content)} bytes)", "success")
                    else:
                        print_status(f"Data file {file_path}: Empty", "warning")
            except Exception as e:
                print_status(f"Error reading {file_path}: {e}", "error")
                all_exist = False
        else:
            print_status(f"Data file missing: {file_path}", "error")
            all_exist = False
    
    return all_exist

def check_frontend_config():
    """Check frontend configuration"""
    print_status("Checking frontend configuration...", "info")
    
    config_files = [
        "frontend/package.json",
        "frontend/next.config.js",
        "frontend/tailwind.config.js",
        "frontend/.env.local"
    ]
    
    all_ok = True
    
    for file_path in config_files:
        if os.path.exists(file_path):
            print_status(f"Frontend config {file_path}: Found", "success")
        else:
            print_status(f"Frontend config missing: {file_path}", "error")
            all_ok = False
    
    # Check if node_modules exists
    if os.path.exists("frontend/node_modules"):
        print_status("Frontend dependencies: Installed", "success")
    else:
        print_status("Frontend dependencies: Not installed", "warning")
        print_status("Run: cd frontend && npm install", "info")
    
    return all_ok

def fix_common_issues():
    """Fix common issues automatically"""
    print_status("Attempting to fix common issues...", "info")
    
    fixes_applied = []
    
    # Create missing directories
    directories = ["data", "agents", "utils", "frontend/app/components"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            fixes_applied.append(f"Created directory: {directory}")
    
    # Fix file permissions for shell scripts
    shell_scripts = ["start-local.sh", "start-docker.sh"]
    for script in shell_scripts:
        if os.path.exists(script):
            try:
                os.chmod(script, 0o755)
                fixes_applied.append(f"Made executable: {script}")
            except Exception as e:
                print_status(f"Could not make {script} executable: {e}", "warning")
    
    # Check and fix environment variables
    env_file = "frontend/.env.local"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
            if "localhost:8000" in content:
                content = content.replace("localhost:8000", "localhost:5000")
                with open(env_file, 'w') as f:
                    f.write(content)
                fixes_applied.append("Fixed API URL in .env.local")
    
    if fixes_applied:
        for fix in fixes_applied:
            print_status(f"Applied fix: {fix}", "success")
    else:
        print_status("No automatic fixes needed", "info")
    
    return len(fixes_applied)

def test_basic_functionality():
    """Test basic functionality without running servers"""
    print_status("Testing basic functionality...", "info")
    
    try:
        # Test data loader
        sys.path.insert(0, '.')
        from utils.data_loader import DataLoader
        data_loader = DataLoader()
        print_status(f"Data loader: {len(data_loader.loaded_datasets)} datasets loaded", "success")
        
        # Test system status checker
        from utils.degraded_mode import SystemStatusChecker
        system_checker = SystemStatusChecker()
        status = system_checker.get_system_status()
        print_status(f"System status checker: {status['mode']} mode", "success")
        
        # Test agent instantiation
        from agents.triage_agent import TriageAgent
        triage_agent = TriageAgent(data_loader)
        print_status("Triage agent: Instantiated successfully", "success")
        
        return True
        
    except Exception as e:
        print_status(f"Basic functionality test failed: {e}", "error")
        return False

def generate_summary_report():
    """Generate comprehensive summary report"""
    print_status("=" * 60, "info")
    print_status("FRONTLINE WORKER AI SYSTEM - ERROR CHECK REPORT", "info")
    print_status("=" * 60, "info")
    
    checks = [
        ("Python Syntax", check_python_syntax),
        ("Import Statements", check_imports),
        ("JSON Files", check_json_files),
        ("Data Files", check_data_files),
        ("Frontend Config", check_frontend_config),
        ("Basic Functionality", test_basic_functionality),
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
    
    # Apply fixes
    print_status(f"\n--- Applying Fixes ---", "info")
    fixes_count = fix_common_issues()
    
    # Summary
    print_status("\n" + "=" * 60, "info")
    print_status("ERROR CHECK SUMMARY", "info")
    print_status("=" * 60, "info")
    
    for check_name, result in results.items():
        status = "success" if result else "error"
        print_status(f"{check_name}: {'PASSED' if result else 'FAILED'}", status)
    
    print_status(f"Fixes Applied: {fixes_count}", "info")
    
    if all_passed:
        print_status("\n🎉 ALL CHECKS PASSED! No errors found.", "success")
        print_status("\nYour system is ready to run:", "info")
        print_status("1. Backend: python app.py", "info")
        print_status("2. Frontend: cd frontend && npm run dev", "info")
        print_status("3. Or use: start-local.bat (Windows) / ./start-local.sh (Linux/Mac)", "info")
    else:
        print_status("\n⚠️ SOME CHECKS FAILED. Issues found:", "warning")
        failed_checks = [name for name, result in results.items() if not result]
        for check in failed_checks:
            print_status(f"- {check}", "error")
        
        print_status("\nRecommended actions:", "info")
        print_status("1. Install missing Python packages: pip install -r requirements-local.txt", "info")
        print_status("2. Install frontend dependencies: cd frontend && npm install", "info")
        print_status("3. Check file permissions and paths", "info")
        print_status("4. Re-run this script after fixes", "info")
    
    return all_passed

if __name__ == "__main__":
    print_status("Starting comprehensive error check...", "info")
    generate_summary_report()