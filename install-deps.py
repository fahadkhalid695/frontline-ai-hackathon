#!/usr/bin/env python3
"""
Quick dependency installer
"""
import subprocess
import sys

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🔧 Installing Frontline Worker AI Dependencies")
    print("=" * 50)
    
    # Essential packages
    packages = [
        'flask>=2.0.0',
        'flask-cors>=4.0.0', 
        'requests>=2.25.0',
        'python-dateutil>=2.8.0'
    ]
    
    success_count = 0
    
    for package in packages:
        print(f"Installing {package}...")
        if install_package(package):
            print(f"✅ {package} installed successfully")
            success_count += 1
        else:
            print(f"❌ Failed to install {package}")
    
    print("\n" + "=" * 50)
    
    if success_count == len(packages):
        print("🎉 All dependencies installed successfully!")
        print("\nNext steps:")
        print("1. Start backend: python app.py")
        print("2. Start frontend: cd frontend && npm run dev")
        print("3. Open browser: http://localhost:3000")
    else:
        print(f"⚠️ {len(packages) - success_count} packages failed to install")
        print("\nTry manual installation:")
        print("pip install flask flask-cors requests python-dateutil")

if __name__ == "__main__":
    main()