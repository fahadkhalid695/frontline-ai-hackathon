"""
Complete test suite for Frontline Worker AI System
"""
import requests
import json
import time

# Update with your actual Cloud Function URL
BASE_URL = "https://us-central1-your-project.cloudfunctions.net/frontline-ai"

def test_health_check():
    """Test system health"""
    print("🧪 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(json.dumps(data, indent=2))
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_triage_agent():
    """Test triage agent"""
    print("\n🧪 Testing Triage Agent...")
    
    test_cases = [
        {
            "symptoms": "chest pain and difficulty breathing",
            "emergency_type": "medical",
            "location": "Lahore",
            "citizen_data": {
                "name": "Ali Ahmed",
                "age": 45,
                "phone": "+923001234567",
                "medical_conditions": ["hypertension"]
            }
        },
        {
            "symptoms": "high fever for 3 days",
            "emergency_type": "medical", 
            "location": "Karachi",
            "citizen_data": {
                "name": "Sara Khan",
                "age": 28,
                "phone": "+923007654321"
            }
        }
    ]
    
    for i, case_data in enumerate(test_cases):
        payload = {
            "action": "triage",
            "case_data": case_data
        }
        
        try:
            response = requests.post(BASE_URL, json=payload, timeout=10)
            print(f"Case {i+1} - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Triage successful! Priority: {data['result']['priority']}")
                print(f"   Urgency: {data['result']['urgency']}")
            else:
                print(f"❌ Triage failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

def test_full_workflow():
    """Test complete agent workflow"""
    print("\n🧪 Testing Complete Workflow...")
    
    emergency_case = {
        "symptoms": "severe accident with leg injury",
        "emergency_type": "medical",
        "location": "Islamabad",
        "citizen_data": {
            "name": "Ahmed Raza",
            "age": 35,
            "phone": "+923001122334",
            "address": "123 Main Street, Islamabad",
            "emergency_contact": "+923004455667"
        }
    }
    
    payload = {
        "action": "full_workflow",
        "case_data": emergency_case
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, timeout=15)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Full workflow completed successfully!")
            print(f"Agent Trace: {' → '.join(data['result']['agent_trace'])}")
            print(f"Final Priority: {data['result']['priority']}")
            print(f"Appointment Time: {data['result']['appointment_details']['appointment_time']}")
            print(f"Confirmation: {data['result']['confirmation_details']['confirmation_number']}")
        else:
            print(f"❌ Workflow failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_degraded_mode():
    """Test degraded mode functionality"""
    print("\n🧪 Testing Degraded Mode...")
    
    # Simulate a case that would trigger degraded mode
    simple_case = {
        "symptoms": "mild headache",
        "emergency_type": "medical",
        "location": "Rawalpindi",
        "citizen_data": {
            "name": "Test User",
            "age": 30
        }
    }
    
    payload = {
        "action": "triage",
        "case_data": simple_case,
        "force_degraded": True  # Simulate degraded mode
    }
    
    try:
        response = requests.post(BASE_URL, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Degraded mode test completed!")
            print(f"System Mode: {data['system_mode']}")
            print(f"Assessment Method: {data['result']['assessment_method']}")
        else:
            print(f"❌ Degraded mode test failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def run_complete_test_suite():
    """Run all tests"""
    print("🚀 Starting Frontline Worker AI Test Suite")
    print("=" * 60)
    
    # Test health check first
    if not test_health_check():
        print("❌ Cannot proceed - health check failed")
        return
    
    # Test individual agents
    test_triage_agent()
    
    # Test complete workflow
    test_full_workflow()
    
    # Test degraded mode
    test_degraded_mode()
    
    print("\n" + "=" * 60)
    print("🎉 Test Suite Complete!")

if __name__ == "__main__":
    run_complete_test_suite()
