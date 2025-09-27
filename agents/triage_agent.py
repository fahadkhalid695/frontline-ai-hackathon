"""
Triage Agent - Emergency priority assessment
"""
import logging
from utils.degraded_mode import DegradedModeHandler

logger = logging.getLogger(__name__)

class TriageAgent:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.degraded_handler = DegradedModeHandler()
    
    def process(self, case_data, system_status):
        """Process triage assessment"""
        logger.info("TriageAgent processing case")
        
        symptoms = case_data.get('symptoms', '')
        emergency_type = case_data.get('emergency_type', 'medical')
        location = case_data.get('location', 'unknown')
        citizen_data = case_data.get('citizen_data', {})
        
        # Use AI if available, otherwise degraded mode
        if system_status['mode'] == 'enhanced':
            result = self.enhanced_triage(symptoms, emergency_type, location, citizen_data)
        else:
            result = self.degraded_handler.rule_based_triage(symptoms, emergency_type, location)
        
        # Add metadata
        result.update({
            'agent': 'triage_agent',
            'timestamp': self.get_timestamp(),
            'case_id': case_data.get('case_id', 'unknown')
        })
        
        logger.info(f"Triage result: {result}")
        return result
    
    def enhanced_triage(self, symptoms, emergency_type, location, citizen_data):
        """Enhanced triage with data analysis"""
        # Analyze symptoms with historical data patterns
        priority_score = self.analyze_symptom_patterns(symptoms)
        
        # Consider citizen factors (age, medical history)
        risk_factors = self.assess_risk_factors(citizen_data)
        
        # Combine assessments
        final_priority = self.determine_final_priority(priority_score, risk_factors)
        
        return {
            'priority': final_priority,
            'urgency': self.priority_to_urgency(final_priority),
            'risk_factors': risk_factors,
            'symptom_severity': priority_score,
            'assessment_method': 'data_enhanced',
            'confidence': self.calculate_confidence(symptoms, final_priority)
        }
    
    def analyze_symptom_patterns(self, symptoms):
        """Analyze symptoms against historical patterns"""
        historical_cases = self.data_loader.query_data('emergency_requests')
        
        symptom_keywords = symptoms.lower().split()
        high_priority_matches = 0
        total_keywords = len(symptom_keywords)
        
        for case in historical_cases:
            case_symptoms = case.get('symptoms', '').lower()
            if any(keyword in case_symptoms for keyword in symptom_keywords):
                if case.get('priority') == 'high':
                    high_priority_matches += 1
        
        # Calculate priority score
        if total_keywords == 0:
            return 'low'
        
        high_match_ratio = high_priority_matches / len(historical_cases) if historical_cases else 0
        
        if high_match_ratio > 0.3:
            return 'high'
        elif high_match_ratio > 0.1:
            return 'medium'
        else:
            return 'low'
    
    def assess_risk_factors(self, citizen_data):
        """Assess risk factors from citizen data"""
        age = citizen_data.get('age', 0)
        existing_conditions = citizen_data.get('medical_conditions', [])
        
        risk_score = 0
        
        # Age-based risk
        if age < 5 or age > 65:
            risk_score += 2
        elif age < 18 or age > 50:
            risk_score += 1
        
        # Condition-based risk
        high_risk_conditions = ['heart disease', 'diabetes', 'asthma', 'pregnancy']
        for condition in existing_conditions:
            if condition.lower() in high_risk_conditions:
                risk_score += 2
        
        return 'high' if risk_score >= 3 else 'medium' if risk_score >= 1 else 'low'
    
    def determine_final_priority(self, symptom_priority, risk_factors):
        """Determine final priority combining all factors"""
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        risk_map = {'high': 2, 'medium': 1, 'low': 0}
        
        total_score = priority_map.get(symptom_priority, 1) + risk_map.get(risk_factors, 0)
        
        if total_score >= 4:
            return 'high'
        elif total_score >= 2:
            return 'medium'
        else:
            return 'low'
    
    def priority_to_urgency(self, priority):
        urgency_map = {
            'high': 'immediate',
            'medium': 'within_2_hours',
            'low': 'within_24_hours'
        }
        return urgency_map.get(priority, 'within_24_hours')
    
    def calculate_confidence(self, symptoms, priority):
        """Calculate confidence level based on symptom specificity"""
        symptom_words = len(symptoms.split())
        if symptom_words >= 5 and priority == 'high':
            return 'very_high'
        elif symptom_words >= 3:
            return 'high'
        else:
            return 'medium'
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
