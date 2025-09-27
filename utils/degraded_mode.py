"""
Degraded mode utilities for offline operation
"""
import urllib.request
import socket
import time
import logging

logger = logging.getLogger(__name__)

class SystemStatusChecker:
    def __init__(self):
        self.last_check = None
        self.cached_status = None
    
    def get_system_status(self):
        """Check system status for degraded mode decisions"""
        # Cache status for 1 minute
        if self.last_check and time.time() - self.last_check < 60:
            return self.cached_status
        
        ai_available = self.check_ai_availability()
        internet_available = self.check_internet_connectivity()
        api_available = self.check_external_apis()
        
        status = {
            'ai_available': ai_available,
            'internet_available': internet_available,
            'api_available': api_available,
            'mode': 'enhanced' if (ai_available and internet_available) else 'degraded',
            'last_checked': time.time(),
            'debug': False  # Set to True for development
        }
        
        self.cached_status = status
        self.last_check = time.time()
        
        logger.info(f"System status: {status}")
        return status
    
    def check_internet_connectivity(self):
        """Check if internet connection is available"""
        try:
            urllib.request.urlopen('https://www.google.com', timeout=3)
            return True
        except:
            return False
    
    def check_ai_availability(self):
        """Check if AI services are available"""
        # For now, assume AI is available if internet is available
        # In real implementation, check specific AI service endpoints
        return self.check_internet_connectivity()
    
    def check_external_apis(self):
        """Check availability of external APIs"""
        # Check common emergency service APIs
        test_endpoints = [
            'https://api.emergency-services.com/status',  # Example
            'https://health-api.gov.pk/status'  # Example
        ]
        
        available_count = 0
        for endpoint in test_endpoints:
            try:
                urllib.request.urlopen(endpoint, timeout=2)
                available_count += 1
            except:
                continue
        
        return available_count > 0  # At least one API available

class DegradedModeHandler:
    """Handle degraded mode operations"""
    
    @staticmethod
    def rule_based_triage(symptoms, emergency_type, location):
        """Rule-based triage for degraded mode"""
        symptoms_lower = symptoms.lower()
        
        # High priority indicators
        high_priority_keywords = [
            'chest pain', 'heart attack', 'stroke', 'unconscious',
            'bleeding heavily', 'difficulty breathing', 'severe burn'
        ]
        
        # Medium priority indicators  
        medium_priority_keywords = [
            'fever', 'pain', 'accident', 'broken', 'cut', 'vomiting',
            'dizziness', 'high temperature'
        ]
        
        if any(keyword in symptoms_lower for keyword in high_priority_keywords):
            priority = 'high'
            urgency = 'immediate'
        elif any(keyword in symptoms_lower for keyword in medium_priority_keywords):
            priority = 'medium' 
            urgency = 'within_2_hours'
        else:
            priority = 'low'
            urgency = 'within_24_hours'
        
        return {
            'priority': priority,
            'urgency': urgency,
            'assessment_method': 'rule_based',
            'confidence': 'high' if priority == 'high' else 'medium'
        }
    
    @staticmethod
    def simple_service_matching(priority, emergency_type, location):
        """Simple service matching for degraded mode"""
        base_services = {
            'medical': {
                'high': 'Emergency Department',
                'medium': 'Urgent Care Center', 
                'low': 'Primary Care Clinic'
            },
            'police': {
                'high': 'Emergency Response Unit',
                'medium': 'Police Station',
                'low': 'Community Police'
            },
            'fire': {
                'high': 'Fire Emergency Response',
                'medium': 'Fire Safety Inspection',
                'low': 'Fire Prevention Office'
            }
        }
        
        service_type = base_services.get(emergency_type, {}).get(priority, 'General Services')
        
        return {
            'recommended_service': service_type,
            'location': location,
            'contact': '1122' if emergency_type == 'medical' else '15',
            'matching_method': 'rule_based'
        }
