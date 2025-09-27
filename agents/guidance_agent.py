"""
Guidance Agent - Service matching and routing
"""
import logging
import random
from utils.degraded_mode import DegradedModeHandler

logger = logging.getLogger(__name__)

class GuidanceAgent:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.degraded_handler = DegradedModeHandler()
    
    def process(self, case_data, system_status):
        """Process service guidance"""
        logger.info("GuidanceAgent processing case")
        
        priority = case_data.get('priority', 'medium')
        emergency_type = case_data.get('emergency_type', 'medical')
        location = case_data.get('location', 'unknown').lower()
        symptoms = case_data.get('symptoms', '')
        
        if system_status['mode'] == 'enhanced':
            result = self.enhanced_guidance(priority, emergency_type, location, symptoms)
        else:
            result = self.degraded_handler.simple_service_matching(priority, emergency_type, location)
        
        # Add metadata
        result.update({
            'agent': 'guidance_agent',
            'timestamp': self.get_timestamp(),
            'emergency_type': emergency_type
        })
        
        logger.info(f"Guidance result: {result}")
        return result
    
    def enhanced_guidance(self, priority, emergency_type, location, symptoms):
        """Enhanced service guidance with data matching"""
        if emergency_type == 'medical':
            return self.find_medical_services(priority, location, symptoms)
        elif emergency_type == 'police':
            return self.find_police_services(priority, location)
        elif emergency_type == 'fire':
            return self.find_fire_services(priority, location)
        else:
            return self.find_general_services(priority, location, emergency_type)
    
    def find_medical_services(self, priority, location, symptoms):
        """Find appropriate medical services"""
        hospitals = self.data_loader.query_data('hospitals', {'location': location})
        
        if not hospitals:
            hospitals = self.data_loader.query_data('hospitals')
        
        # Filter and prioritize based on needs
        suitable_hospitals = self.prioritize_hospitals(hospitals, priority, symptoms)
        
        if suitable_hospitals:
            best_hospital = suitable_hospitals[0]
            alternatives = suitable_hospitals[1:3]  # Top 2 alternatives
        else:
            best_hospital = self.get_fallback_hospital(location)
            alternatives = []
        
        return {
            'service_type': 'medical',
            'recommended_service': best_hospital,
            'alternative_services': alternatives,
            'instructions': self.get_medical_instructions(priority),
            'contact_information': best_hospital.get('emergency_contact', '1122'),
            'estimated_response_time': self.calculate_response_time(priority, location),
            'selection_criteria': self.get_selection_criteria(priority, symptoms)
        }
    
    def prioritize_hospitals(self, hospitals, priority, symptoms):
        """Prioritize hospitals based on priority and symptoms"""
        scored_hospitals = []
        
        for hospital in hospitals:
            score = 0
            
            # Priority-based scoring
            if priority == 'high' and 'Emergency' in hospital.get('specialties', []):
                score += 10
            if priority == 'medium' and 'Urgent Care' in hospital.get('services', []):
                score += 5
            
            # Symptom-based matching
            symptom_specialties = self.map_symptoms_to_specialties(symptoms)
            for specialty in symptom_specialties:
                if specialty in hospital.get('specialties', []):
                    score += 3
            
            # Capacity consideration
            if hospital.get('beds_available', 0) > 5:
                score += 2
            
            scored_hospitals.append((hospital, score))
        
        # Sort by score descending
        scored_hospitals.sort(key=lambda x: x[1], reverse=True)
        return [hospital for hospital, score in scored_hospitals if score > 0]
    
    def map_symptoms_to_specialties(self, symptoms):
        """Map symptoms to medical specialties"""
        symptom_mapping = {
            'chest': ['Cardiology', 'Emergency'],
            'heart': ['Cardiology', 'Emergency'],
            'breathing': ['Pulmonology', 'Emergency'],
            'fever': ['Infectious Disease', 'General Medicine'],
            'pain': ['Emergency', 'General Medicine'],
            'accident': ['Trauma', 'Emergency'],
            'broken': ['Orthopedics', 'Emergency']
        }
        
        specialties = set()
        symptoms_lower = symptoms.lower()
        
        for keyword, specialty_list in symptom_mapping.items():
            if keyword in symptoms_lower:
                specialties.update(specialty_list)
        
        return list(specialties)
    
    def find_police_services(self, priority, location):
        """Find police services"""
        return {
            'service_type': 'police',
            'recommended_service': {
                'name': f'{location.title()} Police Station',
                'type': 'Police Station',
                'emergency_contact': '15'
            },
            'instructions': self.get_police_instructions(priority),
            'contact_information': '15',
            'estimated_response_time': '5-15 minutes' if priority == 'high' else '30-60 minutes'
        }
    
    def get_medical_instructions(self, priority):
        instructions = {
            'high': 'Proceed immediately to emergency department. Call ahead if possible.',
            'medium': 'Visit urgent care center within 2 hours. Bring medical history.',
            'low': 'Schedule appointment with primary care provider.'
        }
        return instructions.get(priority, 'Seek medical attention as soon as possible.')
    
    def get_police_instructions(self, priority):
        instructions = {
            'high': 'Emergency response dispatched. Stay on the line for instructions.',
            'medium': 'Officer will respond within 1 hour. Secure the area if safe.',
            'low': 'File report at nearest police station during business hours.'
        }
        return instructions.get(priority, 'Contact local authorities.')
    
    def calculate_response_time(self, priority, location):
        """Calculate estimated response time"""
        base_times = {
            'high': '5-10 minutes',
            'medium': '15-30 minutes', 
            'low': '1-2 hours'
        }
        
        # Adjust for urban vs rural
        urban_areas = ['lahore', 'karachi', 'islamabad', 'rawalpindi']
        if location.lower() in urban_areas:
            return base_times[priority]
        else:
            adjusted_times = {
                'high': '10-20 minutes',
                'medium': '30-45 minutes',
                'low': '2-3 hours'
            }
            return adjusted_times.get(priority, base_times[priority])
    
    def get_selection_criteria(self, priority, symptoms):
        criteria = {
            'high': 'Emergency capacity and specialty match',
            'medium': 'Urgent care availability and proximity',
            'low': 'General medical services and convenience'
        }
        return criteria.get(priority, 'Service availability')
    
    def get_fallback_hospital(self, location):
        """Fallback hospital data"""
        return {
            'name': f'General Hospital {location.title()}',
            'type': 'General Hospital',
            'emergency_contact': '1122',
            'location': location
        }
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
