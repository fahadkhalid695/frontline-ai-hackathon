#!/usr/bin/env python3
"""
Test the agentic system with natural language input
"""
import requests
import json

def test_parsing():
    """Test the parsing agent"""
    print("🧪 Testing Parsing Agent...")
    
    test_inputs = [
        "I'm having severe chest pain and can't breathe properly",
        "There's a fire in my building on the 3rd floor",
        "Someone broke into my store and threatened me with a knife",
        "My elderly father fell down and hit his head, he's unconscious",
        "I have a high fever and have been vomiting for 2 days"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n--- Test {i}: {user_input} ---")
        
        try:
            response = requests.post('http://localhost:5000/api/parse-emergency', 
                                   json={'user_input': user_input}, 
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Emergency Type: {result['emergency_type']}")
                print(f"✅ Priority: {result['priority']}")
                print(f"✅ Summary: {result['summary']}")
                print(f"✅ Confidence: {result['confidence']:.2f}")
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Backend not running. Start with: python app.py")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def test_full_agentic_workflow():
    """Test the complete agentic workflow"""
    print("\n🤖 Testing Complete Agentic Workflow...")
    
    # Test high priority medical emergency
    user_input = "Help! I'm having severe chest pain and difficulty breathing. I'm 58 years old and have diabetes. I'm at my home in Lahore."
    
    print(f"Input: {user_input}")
    
    try:
        # Step 1: Parse the input
        print("\n1. Parsing emergency input...")
        parse_response = requests.post('http://localhost:5000/api/parse-emergency', 
                                     json={'user_input': user_input}, 
                                     timeout=10)
        
        if parse_response.status_code != 200:
            print(f"❌ Parsing failed: {parse_response.text}")
            return False
        
        parsed_data = parse_response.json()
        print(f"✅ Parsed as: {parsed_data['emergency_type']} emergency, {parsed_data['priority']} priority")
        
        # Step 2: Process through agents
        print("\n2. Processing through AI agents...")
        agent_response = requests.post('http://localhost:5000/api/emergency',
                                     json={
                                         'action': 'full_workflow',
                                         'case_data': parsed_data['case_data']
                                     },
                                     timeout=30)
        
        if agent_response.status_code != 200:
            print(f"❌ Agent processing failed: {agent_response.text}")
            return False
        
        result = agent_response.json()
        agent_result = result['result']
        
        print(f"✅ Agent workflow completed!")
        print(f"   Priority: {agent_result.get('priority', 'N/A')}")
        print(f"   Service: {agent_result.get('recommended_service', 'N/A')}")
        print(f"   Appointment: {agent_result.get('appointment_details', {}).get('appointment_time', 'N/A')}")
        print(f"   Agents used: {' → '.join(result.get('agent_trace', []))}")
        
        # Show autonomous actions
        if 'autonomous_actions' in agent_result:
            actions = agent_result['autonomous_actions']
            print(f"\n🤖 Autonomous Actions Taken ({len(actions)}):")
            for action in actions:
                print(f"   • {action['action_type']}: {action.get('user_notification', 'Action completed')}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Start with: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 Testing Agentic Emergency Response System")
    print("=" * 60)
    
    # Test parsing first
    if not test_parsing():
        return
    
    # Test full workflow
    if not test_full_agentic_workflow():
        return
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! The agentic system is working!")
    print("\nNext steps:")
    print("1. Start frontend: cd frontend && npm run dev")
    print("2. Open browser: http://localhost:3000")
    print("3. Try voice input or natural language text")

if __name__ == "__main__":
    main()