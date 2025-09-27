"""
Booking Agent - Appointment scheduling and form filling
"""
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class BookingAgent:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def process(self, case_data, system_status):
        """Process booking and appointment scheduling"""
        logger.info("BookingAgent processing case")
        
        service_info = case_data.get('recommended_service', {})
        priority = case_data.get('priority', 'medium')
        citizen_data = case_data.get('citizen_data', {})
        emergency_type = case_data.get('emergency_type', 'medical')
        
        # Generate appointment details
        appointment = self.generate_appointment(priority, service_info, emergency_type)
        
        # Generate form data
        form_data = self.generate_form_data(citizen_data, service_info, emergency_type)
        
        # Generate confirmation
        confirmation = self.generate_confirmation(appointment, form_data, citizen_data)
        
        result = {
            'appointment_details': appointment,
            'form_data': form_data,
            'confirmation_details': confirmation,
            'booking_status': 'confirmed',
            'agent': 'booking_agent',
            'timestamp': self.get_timestamp()
        }
        
        logger.info(f"Booking result: {result}")
        return result
    
    def generate_appointment(self, priority, service_info, emergency_type):
        """Generate appointment details based on priority"""
        now = datetime.now()
        
        if priority == 'high':
            # Immediate or within 30 minutes
            appointment_time = now + timedelta(minutes=15 + random.randint(0, 15))
            slot_type = 'Emergency'
            duration = 45  # minutes
        elif priority == 'medium':
            # Within 2 hours
            appointment_time = now + timedelta(hours=1, minutes=random.randint(0, 60))
            slot_type = 'Urgent'
            duration = 30
        else:
            # Next available slot (same day or next day)
            hours_ahead = random.randint(2, 24)
            appointment_time = now + timedelta(hours=hours_ahead)
            # Round to nearest 15 minutes
            appointment_time = appointment_time.replace(minute=(appointment_time.minute // 15) * 15)
            slot_type = 'Standard'
            duration = 20
        
        # Ensure appointment is during reasonable hours (8 AM - 8 PM)
        if appointment_time.hour < 8:
            appointment_time = appointment_time.replace(hour=8, minute=0)
        elif appointment_time.hour >= 20:
            appointment_time = appointment_time.replace(hour=8, minute=0) + timedelta(days=1)
        
        return {
            'appointment_id': f"APT-{random.randint(10000, 99999)}",
            'service_name': service_info.get('name', 'Service Provider'),
            'appointment_time': appointment_time.isoformat(),
            'slot_type': slot_type,
            'duration_minutes': duration,
            'priority': priority,
            'location': service_info.get('location', 'Not specified'),
            'instructions': self.get_appointment_instructions(priority, emergency_type)
        }
    
    def generate_form_data(self, citizen_data, service_info, emergency_type):
        """Generate pre-filled form data"""
        base_form = {
            'service_type': emergency_type,
            'service_provider': service_info.get('name', 'Unknown'),
            'submission_date': datetime.now().isoformat(),
            'status': 'pending_review',
            'form_version': '1.0'
        }
        
        # Add citizen data
        form_data = {**base_form, **citizen_data}
        
        # Add emergency-specific fields
        if emergency_type == 'medical':
            form_data.update({
                'medical_urgency': True,
                'triage_priority': citizen_data.get('priority', 'medium'),
                'required_documents': ['ID Card', 'Medical History if available']
            })
        elif emergency_type == 'police':
            form_data.update({
                'incident_report': True,
                'urgency_level': citizen_data.get('priority', 'medium'),
                'required_documents': ['ID Card', 'Incident Details']
            })
        
        # Generate form fields dynamically
        form_data['form_fields'] = self.generate_form_fields(citizen_data, emergency_type)
        
        return form_data
    
    def generate_form_fields(self, citizen_data, emergency_type):
        """Generate dynamic form fields based on emergency type"""
        base_fields = [
            {'field': 'full_name', 'value': citizen_data.get('name', ''), 'required': True},
            {'field': 'contact_number', 'value': citizen_data.get('phone', ''), 'required': True},
            {'field': 'emergency_contact', 'value': citizen_data.get('emergency_contact', ''), 'required': False}
        ]
        
        if emergency_type == 'medical':
            medical_fields = [
                {'field': 'symptoms', 'value': citizen_data.get('symptoms', ''), 'required': True},
                {'field': 'existing_conditions', 'value': ', '.join(citizen_data.get('medical_conditions', [])), 'required': False},
                {'field': 'allergies', 'value': citizen_data.get('allergies', ''), 'required': False}
            ]
            base_fields.extend(medical_fields)
        elif emergency_type == 'police':
            police_fields = [
                {'field': 'incident_description', 'value': citizen_data.get('incident_details', ''), 'required': True},
                {'field': 'incident_location', 'value': citizen_data.get('location', ''), 'required': True},
                {'field': 'witnesses', 'value': citizen_data.get('witnesses', ''), 'required': False}
            ]
            base_fields.extend(police_fields)
        
        return base_fields
    
    def generate_confirmation(self, appointment, form_data, citizen_data):
        """Generate booking confirmation"""
        confirmation_number = f"CNF-{random.randint(100000, 999999)}"
        
        return {
            'confirmation_number': confirmation_number,
            'confirmation_time': datetime.now().isoformat(),
            'customer_name': citizen_data.get('name', 'Customer'),
            'service_details': {
                'name': appointment['service_name'],
                'time': appointment['appointment_time'],
                'type': appointment['slot_type']
            },
            'next_steps': self.get_next_steps(appointment['priority'], appointment['slot_type']),
            'contact_information': appointment.get('location', 'Service Location'),
            'important_notes': self.get_important_notes(appointment['priority'])
        }
    
    def get_appointment_instructions(self, priority, emergency_type):
        """Get appointment instructions"""
        instructions = {
            'high': {
                'medical': 'Go directly to emergency department. Bring ID and insurance if available.',
                'police': 'Officer is en route. Stay in a safe location.',
                'fire': 'Fire team dispatched. Evacuate if necessary.'
            },
            'medium': {
                'medical': 'Visit within 2 hours. Bring medical records and medications.',
                'police': 'Officer will arrive within 1 hour. Secure evidence if safe.',
                'fire': 'Safety inspection scheduled. Ensure access to property.'
            },
            'low': {
                'medical': 'Schedule at your convenience. Bring relevant medical history.',
                'police': 'File report at station. Bring identification.',
                'fire': 'Prevention consultation scheduled.'
            }
        }
        
        return instructions.get(priority, {}).get(emergency_type, 'Follow service provider instructions.')
    
    def get_next_steps(self, priority, slot_type):
        """Get next steps after booking"""
        if priority == 'high':
            return [
                'Proceed immediately to service location',
                'Bring identification documents',
                'Inform emergency contact if possible'
            ]
        else:
            return [
                f'Arrive 15 minutes before {slot_type.lower()} appointment',
                'Bring required documents',
                'Contact service provider if unable to attend'
            ]
    
    def get_important_notes(self, priority):
        """Get important notes for the appointment"""
        notes = {
            'high': 'This is an emergency appointment. Time is critical.',
            'medium': 'This is an urgent appointment. Please arrive on time.',
            'low': 'This is a standard appointment. Reschedule if necessary.'
        }
        return notes.get(priority, 'Please arrive on time for your appointment.')
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
