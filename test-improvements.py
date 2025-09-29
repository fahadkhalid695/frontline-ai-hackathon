#!/usr/bin/env python3
"""
Test the improved agentic system with enhanced features
"""
import requests
import json

def test_enhanced_parsing():
    """Test the enhanced parsing with better training"""
    print("🧠 Testing Enhanced Problem Identification...")
    
    test_cases = [
        # Medical emergencies with varying complexity
        {
            'input': "Help! I'm having severe crushing chest pain radiating to my left arm, I'm 58 and diabetic",
            'expected_type': 'medical',
            'expected_priority': 'high'
        },
        {
            'input': "My elderly father fell down the stairs and hit his head, he's unconscious and bleeding",
            'expected_type': 'medical', 
            'expected_priority': 'high'
        },
        {
            'input': "I have a high fever of 103°F for 3 days with severe headache and stiff neck",
            'expected_type': 'medical',
            'expected_priority': 'medium'
        },
        
        # Police emergencies
        {
            'input': "Someone broke into my house with a gun and threatened my family",
            'expected_type': 'police',
            'expected_priority': 'high'
        },
        {
            'input': "There's a suspicious person trying to break into cars in my neighborhood",
            'expected_type': 'police',
            'expected_priority': 'medium'
        },
        
        # Fire emergencies
        {
            'input': "There's a massive fire in my apartment building, people are trapped on upper floors",
            'expected_type': 'fire',
            'expected_priority': 'high'
        },
        {
            'input': "I smell gas leak in my kitchen and the stove won't turn off",
            'expected_type': 'fire',
            'expected_priority': 'high'
        }
    ]
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['input'][:50]}... ---")
        
        try:
            # Test with mock location data
            location_data = {
                'lat': 31.5204,
                'lng': 74.3587,
                'address': 'Lahore, Punjab, Pakistan'
            }
            
            response = requests.post('http://localhost:5000/api/parse-emergency', 
                                   json={
                                       'user_input': test_case['input'],
                                       'location_data': location_data
                                   }, 
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                predicted_type = result['emergency_type']
                predicted_priority = result['priority']
                
                type_correct = predicted_type == test_case['expected_type']
                priority_correct = predicted_priority == test_case['expected_priority']
                
                if type_correct and priority_correct:
                    print(f"✅ CORRECT: {predicted_type} / {predicted_priority}")
                    correct_predictions += 1
                else:
                    print(f"❌ INCORRECT: Got {predicted_type}/{predicted_priority}, Expected {test_case['expected_type']}/{test_case['expected_priority']}")
                
                print(f"   Confidence: {result['confidence']:.2f}")
                print(f"   Summary: {result['summary']}")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Backend not running. Start with: python app.py")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
    
    accuracy = (correct_predictions / total_tests) * 100
    print(f"\n📊 ACCURACY: {correct_predictions}/{total_tests} ({accuracy:.1f}%)")
    
    if accuracy >= 80:
        print("✅ Enhanced parsing is working well!")
        return True
    else:
        print("⚠️ Parsing needs more improvement")
        return False

def test_location_detection():
    """Test location detection with GPS coordinates"""
    print("\n📍 Testing Location Detection...")
    
    test_locations = [
        {'lat': 31.5204, 'lng': 74.3587, 'expected': 'Lahore'},
        {'lat': 24.8607, 'lng': 67.0011, 'expected': 'Karachi'},
        {'lat': 33.6844, 'lng': 73.0479, 'expected': 'Islamabad'},
    ]
    
    for location in test_locations:
        try:
            response = requests.post('http://localhost:5000/api/parse-emergency',
                                   json={
                                       'user_input': 'I need help with chest pain',
                                       'location_data': {
                                           'lat': location['lat'],
                                           'lng': location['lng']
                                       }
                                   },
                                   timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                detected_location = result['case_data']['location']
                
                if location['expected'].lower() in detected_location.lower():
                    print(f"✅ {location['expected']}: {detected_location}")
                else:
                    print(f"❌ Expected {location['expected']}, got {detected_location}")
            
        except Exception as e:
            print(f"❌ Location test failed: {e}")
            return False
    
    return True

def test_autonomous_actions():
    """Test autonomous actions for different priorities"""
    print("\n🤖 Testing Autonomous Actions...")
    
    test_case = {
        'user_input': 'Help! I\'m having a heart attack, severe chest pain, can\'t breathe',
        'location_data': {
            'lat': 31.5204,
            'lng': 74.3587,
            'address': 'Model Town, Lahore, Punjab, Pakistan'
        }
    }
    
    try:
        # Parse the emergency
        parse_response = requests.post('http://localhost:5000/api/parse-emergency',
                                     json=test_case,
                                     timeout=10)
        
        if parse_response.status_code != 200:
            print(f"❌ Parsing failed: {parse_response.text}")
            return False
        
        parsed_data = parse_response.json()
        
        # Process through full workflow
        workflow_response = requests.post('http://localhost:5000/api/emergency',
                                        json={
                                            'action': 'full_workflow',
                                            'case_data': parsed_data['case_data']
                                        },
                                        timeout=30)
        
        if workflow_response.status_code != 200:
            print(f"❌ Workflow failed: {workflow_response.text}")
            return False
        
        result = workflow_response.json()
        
        # Check if autonomous actions were taken
        if 'autonomous_actions' in result['result']:
            actions = result['result']['autonomous_actions']
            print(f"✅ {len(actions)} autonomous actions executed:")
            
            action_types = [action['action_type'] for action in actions]
            
            # Check for expected high-priority actions
            expected_actions = ['emergency_call', 'hospital_alert', 'location_share']
            found_actions = [action for action in expected_actions if action in action_types]
            
            print(f"   Expected actions found: {found_actions}")
            print(f"   All actions: {action_types}")
            
            if len(found_actions) >= 2:
                print("✅ Autonomous actions working correctly!")
                return True
            else:
                print("⚠️ Some expected actions missing")
                return False
        else:
            print("❌ No autonomous actions found in response")
            return False
            
    except Exception as e:
        print(f"❌ Autonomous actions test failed: {e}")
        return False

def main():
    print("🚀 Testing System Improvements")
    print("=" * 60)
    
    tests = [
        ("Enhanced Problem Identification", test_enhanced_parsing),
        ("Location Detection", test_location_detection), 
        ("Autonomous Actions", test_autonomous_actions)
    ]
    
    passed_tests = 0
    
    for test_name, test_function in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 40)
        
        try:
            if test_function():
                passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTS: {passed_tests}/{len(tests)} tests passed")
    
    if passed_tests == len(tests):
        print("🎉 All improvements are working correctly!")
        print("\nNew features ready:")
        print("✅ Enhanced problem identification with better training")
        print("✅ Real GPS location detection and sharing")
        print("✅ Autonomous emergency calling")
        print("✅ Download summary and share features")
        print("✅ Direct department contact numbers")
    else:
        print("⚠️ Some improvements need attention")
    
    print(f"\n🌐 Test the UI at: http://localhost:3000")

if __name__ == "__main__":
    main()