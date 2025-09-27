"""
Complete Frontline Worker Support AI System
Multi-agent orchestrator with degraded mode support
"""
import functions_framework
import json
import logging
import traceback
from datetime import datetime

from agents.triage_agent import TriageAgent
from agents.guidance_agent import GuidanceAgent
from agents.booking_agent import BookingAgent
from agents.followup_agent import FollowupAgent
from utils.data_loader import DataLoader
from utils.degraded_mode import SystemStatusChecker

# Initialize components
data_loader = DataLoader()
system_checker = SystemStatusChecker()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@functions_framework.http
def frontline_ai(request):
    """Main Cloud Function - Complete Frontline Worker AI"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    if request.method == 'OPTIONS':
        return ('', 204, headers)
    
    try:
        # Parse request
        request_json = request.get_json(silent=True) or {}
        logger.info(f"Received request: {request_json}")
        
        # Get action and case data
        action = request_json.get('action', 'full_workflow')
        case_data = request_json.get('case_data', {})
        citizen_id = case_data.get('citizen_id', f"citizen_{datetime.now().strftime('%H%M%S')}")
        
        # Check system status for degraded mode
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
        
        logger.info(f"Response: {response}")
        return (json.dumps(response), 200, headers)
        
    except Exception as e:
        logger.error(f"Error: {str(e)}\n{traceback.format_exc()}")
        error_response = {
            'status': 'error',
            'message': str(e),
            'traceback': traceback.format_exc() if system_status.get('debug', False) else None
        }
        return (json.dumps(error_response), 500, headers)

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
    
    # 1. Triage Agent
    triage_agent = TriageAgent(data_loader)
    triage_result = triage_agent.process(case_data, system_status)
    results['triage'] = triage_result
    agent_trace.append('triage_agent')
    
    # 2. Guidance Agent
    guidance_data = {**case_data, **triage_result}
    guidance_agent = GuidanceAgent(data_loader)
    guidance_result = guidance_agent.process(guidance_data, system_status)
    results['guidance'] = guidance_result
    agent_trace.append('guidance_agent')
    
    # 3. Booking Agent
    booking_data = {**guidance_data, **guidance_result}
    booking_agent = BookingAgent(data_loader)
    booking_result = booking_agent.process(booking_data, system_status)
    results['booking'] = booking_result
    agent_trace.append('booking_agent')
    
    # 4. Follow-up Agent
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
    
    return combined_result

# Health check endpoint
@functions_framework.http
def health_check(request):
    """System health check"""
    status = system_checker.get_system_status()
    return json.dumps({
        'status': 'healthy',
        'service': 'Frontline Worker AI',
        'system_mode': status['mode'],
        'datasets_loaded': len(data_loader.loaded_datasets),
        'timestamp': datetime.now().isoformat()
    }), 200
