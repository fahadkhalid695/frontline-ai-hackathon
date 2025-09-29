#!/usr/bin/env python3
"""
Debug version of the backend to identify issues
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import logging
from datetime import datetime
import traceback

app = Flask(__name__)
CORS(app)

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check"""
    logger.info("Health check requested")
    return jsonify({
        'status': 'healthy',
        'service': 'Frontline Worker AI - Debug Mode',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/emergency', methods=['POST', 'OPTIONS'])
def process_emergency():
    """Debug emergency processing endpoint"""
    
    if request.method == 'OPTIONS':
        logger.info("CORS preflight request")
        return '', 204
    
    logger.info("Emergency request received")
    
    try:
        # Parse request
        request_data = request.get_json()
        logger.info(f"Request data: {request_data}")
        
        if not request_data:
            raise ValueError("No JSON data received")
        
        # Get action and case data
        action = request_data.get('action', 'full_workflow')
        case_data = request_data.get('case_data', {})
        
        logger.info(f"Action: {action}")
        logger.info(f"Case data keys: {list(case_data.keys())}")
        
        # Try importing agents one by one
        logger.info("Testing agent imports...")
        
        try:
            from agents.triage_agent import TriageAgent
            logger.info("✅ TriageAgent imported")
        except Exception as e:
            logger.error(f"❌ TriageAgent import failed: {e}")
            raise
        
        try:
            from agents.guidance_agent import GuidanceAgent
            logger.info("✅ GuidanceAgent imported")
        except Exception as e:
            logger.error(f"❌ GuidanceAgent import failed: {e}")
            raise
        
        try:
            from agents.booking_agent import BookingAgent
            logger.info("✅ BookingAgent imported")
        except Exception as e:
            logger.error(f"❌ BookingAgent import failed: {e}")
            raise
        
        try:
            from agents.followup_agent import FollowupAgent
            logger.info("✅ FollowupAgent imported")
        except Exception as e:
            logger.error(f"❌ FollowupAgent import failed: {e}")
            raise
        
        try:
            from agents.equity_agent import EquityAgent
            logger.info("✅ EquityAgent imported")
        except Exception as e:
            logger.error(f"❌ EquityAgent import failed: {e}")
            raise
        
        try:
            from utils.data_loader import DataLoader
            from utils.degraded_mode import SystemStatusChecker
            logger.info("✅ Utils imported")
        except Exception as e:
            logger.error(f"❌ Utils import failed: {e}")
            raise
        
        # Initialize components
        logger.info("Initializing components...")
        data_loader = DataLoader()
        system_checker = SystemStatusChecker()
        system_status = system_checker.get_system_status()
        
        logger.info(f"System status: {system_status}")
        logger.info(f"Datasets loaded: {len(data_loader.loaded_datasets)}")
        
        # Test simple triage
        logger.info("Testing triage agent...")
        triage_agent = TriageAgent(data_loader)
        triage_result = triage_agent.process(case_data, system_status)
        logger.info(f"Triage result: {triage_result}")
        
        # Simple response
        response = {
            'status': 'success',
            'message': 'Debug test completed successfully',
            'action': action,
            'triage_result': triage_result,
            'system_status': system_status,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("Sending successful response")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing emergency: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        error_response = {
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__,
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }
        return jsonify(error_response), 500

@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 error: {request.url}")
    return jsonify({'error': 'Endpoint not found', 'url': request.url}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({'error': 'Internal server error', 'details': str(error)}), 500

if __name__ == '__main__':
    print("🐛 Starting Debug Backend Server")
    print("📍 Backend running on: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/health")
    print("🧪 Emergency endpoint: http://localhost:5000/api/emergency")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)