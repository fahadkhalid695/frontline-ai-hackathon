#!/usr/bin/env python3
"""
Startup checker to identify why the system isn't working
"""
import subprocess
import requests
import time
import sys
import os

def print_status(message, status="info"):
    colors = {
        "info": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "reset": "\033[0m"
    }
    
    icons = {
        "info": "ℹ️",
        "success": "✅",
        "warning": "⚠️",
        "error": "❌"
    }
    
    print(f"{colors[status]}{icons[status]} {message}{colors['reset']}")

def check_port_availability(port):
    """Check if a port is available"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0  # Port is available if connection fails
    except:
        return True

def check_backend_health():
    """Check if backend is responding"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['flask', 'flask_cors', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def main():
    print_status("🔍 Checking Frontline Worker AI System Startup", "info")
    print("=" * 60)
    
    # Check 1: Dependencies
    print_status("Checking dependencies...", "info")
    missing_deps = check_dependencies()
    if missing_deps:
        print_status(f"Missing dependencies: {', '.join(missing_deps)}", "error")
        print_status("Fix: pip install flask flask-cors requests", "warning")
        return False
    else:
        print_status("All dependencies installed", "success")
    
    # Check 2: Port availability
    print_status("Checking port 5000 availability...", "info")
    if not check_port_availability(5000):
        print_status("Port 5000 is already in use", "warning")
        print_status("Something is already running on port 5000", "info")
        
        # Check if it's our backend
        if check_backend_health():
            print_status("Backend is already running and healthy!", "success")
            print_status("You can now use the frontend at http://localhost:3000", "info")
            return True
        else:
            print_status("Port 5000 is used by another service", "error")
            print_status("Fix: Kill the process using port 5000 or change the port", "warning")
            return False
    else:
        print_status("Port 5000 is available", "success")
    
    # Check 3: Try to start backend
    print_status("Attempting to start backend...", "info")
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print_status("app.py not found in current directory", "error")
        print_status("Make sure you're in the project root directory", "warning")
        return False
    
    print_status("Starting backend server (this may take a moment)...", "info")
    print_status("If successful, you should see server startup messages below:", "info")
    print("-" * 60)
    
    # Try to start the backend
    try:
        # Start backend in a way that shows output
        result = subprocess.run([sys.executable, 'app.py'], 
                              timeout=10, 
                              capture_output=False)
    except subprocess.TimeoutExpired:
        print("-" * 60)
        print_status("Backend startup timed out (this might be normal)", "warning")
        print_status("Checking if backend is now running...", "info")
        
        # Give it a moment to start
        time.sleep(2)
        
        if check_backend_health():
            print_status("Backend is now running!", "success")
            print_status("Frontend: http://localhost:3000", "info")
            print_status("Backend: http://localhost:5000", "info")
            return True
        else:
            print_status("Backend failed to start properly", "error")
            return False
    except KeyboardInterrupt:
        print_status("Startup interrupted by user", "warning")
        return False
    except Exception as e:
        print_status(f"Error starting backend: {e}", "error")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n" + "=" * 60)
        print_status("✨ System is ready!", "success")
        print_status("Next steps:", "info")
        print_status("1. Keep this terminal open (backend running)", "info")
        print_status("2. Open new terminal: cd frontend && npm run dev", "info")
        print_status("3. Open browser: http://localhost:3000", "info")
    else:
        print("\n" + "=" * 60)
        print_status("❌ System startup failed", "error")
        print_status("Try these fixes:", "warning")
        print_status("1. Install dependencies: pip install flask flask-cors requests", "info")
        print_status("2. Check you're in the right directory", "info")
        print_status("3. Run debug backend: python debug-backend.py", "info")
        print_status("4. Check troubleshooting guide: TROUBLESHOOTING.md", "info")