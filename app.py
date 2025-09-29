"""
Local Flask Backend for Frontline Worker AI System
Development server for testing the complete system locally
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime
import traceback

# Import your existing agents
from agents.triage_agent import TriageAgent
from agents.guidance_agent import GuidanceAgent
from agents.booking_agent import BookingAgent
from agents.followup_agent import FollowupAgent
from utils.data_loader import DataLoader
from utils.degraded_mode import SystemStatusChecker

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize components
data_loader = DataLoader()
system_checker = SystemStatusChecker()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    try:
        status = system_checker.get_system_status()
        return jsonify({
            'status': 'healthy',
            'service': 'Frontline Worker AI - Local Development',
            'system_mode': status['mode'],
            'datasets_loaded': len(data_loader.loaded_datasets),
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0-dev'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/emergency', methods=['POST', 'OPTIONS'])
def process_emergency():
    """Main emergency processing endpoint"""
    
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Parse request
        request_data = request.get_json() or {}
        logger.info(f"Received emergency request: {request_data}")
        
        # Get action and case data
        action = request_data.get('action', 'full_workflow')
        case_data = request_data.get('case_data', {})
        citizen_id = case_data.get('citizen_id', f"citizen_{datetime.now().strftime('%H%M%S')}")
        
        # Check system status
        system_status = system_checker.get_system_status()
        
        # Execute workflow based on action
        if action == 'triage':
            result = execute_triage(case_data, system_status)
        elif action == 'guidance':
            result = execute_guidance(case_data, system_status)
        elif action == 'booking':
            result = execute_booking(case_data, system_status)
        elif action == 'followup':
            result = execute_followup(case_data, system_status)
        else:  # full_workflow
            result = execute_full_workflow(case_data, system_status)
        
        # Prepare response
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'system_mode': system_status['mode'],
            'action': action,
            'citizen_id': citizen_id,
            'result': result,
            'agent_trace': result.get('agent_trace', [])
        }
        
        logger.info(f"Emergency processed successfully for citizen: {citizen_id}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing emergency: {str(e)}\n{traceback.format_exc()}")
        error_response = {
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        return jsonify(error_response), 500

def execute_triage(case_data, system_status):
    """Execute triage agent only"""
    agent = TriageAgent(data_loader)
    result = agent.process(case_data, system_status)
    return result

def execute_guidance(case_data, system_status):
    """Execute guidance agent only"""
    agent = GuidanceAgent(data_loader)
    result = agent.process(case_data, system_status)
    return result

def execute_booking(case_data, system_status):
    """Execute booking agent only"""
    agent = BookingAgent(data_loader)
    result = agent.process(case_data, system_status)
    return result

def execute_followup(case_data, system_status):
    """Execute follow-up agent only"""
    agent = FollowupAgent(data_loader)
    result = agent.process(case_data, system_status)
    return result

def execute_full_workflow(case_data, system_status):
    """Execute complete agent workflow"""
    agent_trace = []
    results = {}
    
    try:
        # 1. Triage Agent
        logger.info("Starting Triage Agent...")
        triage_agent = TriageAgent(data_loader)
        triage_result = triage_agent.process(case_data, system_status)
        results['triage'] = triage_result
        agent_trace.append('triage_agent')
        
        # 2. Guidance Agent
        logger.info("Starting Guidance Agent...")
        guidance_data = {**case_data, **triage_result}
        guidance_agent = GuidanceAgent(data_loader)
        guidance_result = guidance_agent.process(guidance_data, system_status)
        results['guidance'] = guidance_result
        agent_trace.append('guidance_agent')
        
        # 3. Booking Agent
        logger.info("Starting Booking Agent...")
        booking_data = {**guidance_data, **guidance_result}
        booking_agent = BookingAgent(data_loader)
        booking_result = booking_agent.process(booking_data, system_status)
        results['booking'] = booking_result
        agent_trace.append('booking_agent')
        
        # 4. Follow-up Agent
        logger.info("Starting Follow-up Agent...")
        followup_data = {**booking_data, **booking_result}
        followup_agent = FollowupAgent(data_loader)
        followup_result = followup_agent.process(followup_data, system_status)
        results['followup'] = followup_result
        agent_trace.append('followup_agent')
        
        # Combine all results
        combined_result = {}
        for stage_result in results.values():
            combined_result.update(stage_result)
        
        combined_result['agent_trace'] = agent_trace
        combined_result['workflow_complete'] = True
        combined_result['processing_stages'] = results  # Include individual stage results
        
        logger.info("Full workflow completed successfully")
        return combined_result
        
    except Exception as e:
        logger.error(f"Error in workflow execution: {str(e)}")
        # Return partial results if available
        combined_result = {}
        for stage_result in results.values():
            combined_result.update(stage_result)
        combined_result['agent_trace'] = agent_trace
        combined_result['workflow_complete'] = False
        combined_result['error'] = str(e)
        return combined_result

@app.route('/api/test-agents', methods=['GET'])
def test_agents():
    """Test endpoint to verify all agents are working"""
    try:
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
        
        system_status = system_checker.get_system_status()
        
        # Test each agent individually
        agents_status = {}
        
        # Test Triage Agent
        try:
            triage_agent = TriageAgent(data_loader)
            triage_result = triage_agent.process(test_case, system_status)
            agents_status['triage'] = {'status': 'working', 'result': triage_result}
        except Exception as e:
            agents_status['triage'] = {'status': 'error', 'error': str(e)}
        
        # Test Guidance Agent
        try:
            guidance_agent = GuidanceAgent(data_loader)
            guidance_result = guidance_agent.process({**test_case, 'priority': 'high'}, system_status)
            agents_status['guidance'] = {'status': 'working', 'result': guidance_result}
        except Exception as e:
            agents_status['guidance'] = {'status': 'error', 'error': str(e)}
        
        # Test Booking Agent
        try:
            booking_agent = BookingAgent(data_loader)
            booking_result = booking_agent.process({**test_case, 'priority': 'high'}, system_status)
            agents_status['booking'] = {'status': 'working', 'result': booking_result}
        except Exception as e:
            agents_status['booking'] = {'status': 'error', 'error': str(e)}
        
        # Test Follow-up Agent
        try:
            followup_agent = FollowupAgent(data_loader)
            followup_result = followup_agent.process({**test_case, 'priority': 'high'}, system_status)
            agents_status['followup'] = {'status': 'working', 'result': followup_result}
        except Exception as e:
            agents_status['followup'] = {'status': 'error', 'error': str(e)}
        
        return jsonify({
            'status': 'success',
            'message': 'Agent testing completed',
            'agents': agents_status,
            'system_status': system_status,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Agent testing failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Frontline Worker AI - Local Development Server")
    print("📍 Backend running on: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/health")
    print("🧪 Test agents: http://localhost:5000/api/test-agents")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)