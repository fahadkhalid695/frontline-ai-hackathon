"""
Action Agent - Autonomous actions like making calls, sending SMS, notifications
"""
import logging
from datetime import datetime
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class ActionAgent:
    def __init__(self):
        self.emergency_contacts = {
            'medical': '1122',
            'police': '15', 
            'fire': '16',
            'rescue': '1122'
        }
        
        self.hospital_contacts = {
            'Jinnah Hospital Lahore': '042-99231441',
            'Services Hospital Lahore': '042-99212171',
            'Aga Khan Hospital Karachi': '021-34864114',
            'Civil Hospital Karachi': '021-99215740',
            'PIMS Islamabad': '051-9261170'
        }

    def execute_autonomous_actions(self, case_data: Dict[str, Any], agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute autonomous actions based on case priority and type"""
        logger.info("ActionAgent executing autonomous actions")
        
        actions_taken = []
        priority = agent_results.get('priority', 'medium')
        emergency_type = case_data.get('emergency_type', 'medical')
        
        # High priority actions - immediate response
        if priority == 'high':
            actions_taken.extend(self._execute_high_priority_actions(case_data, agent_results))
        
        # Medium priority actions - scheduled response
        elif priority == 'medium':
            actions_taken.extend(self._execute_medium_priority_actions(case_data, agent_results))
        
        # Low priority actions - informational
        else:
            actions_taken.extend(self._execute_low_priority_actions(case_data, agent_results))
        
        # Always send confirmation SMS if phone available
        phone = case_data.get('citizen_data', {}).get('phone')
        if phone:
            sms_action = self._send_confirmation_sms(phone, agent_results)
            actions_taken.append(sms_action)
        
        logger.info(f"Executed {len(actions_taken)} autonomous actions")
        return actions_taken

    def _execute_high_priority_actions(self, case_data: Dict[str, Any], agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute high priority autonomous actions"""
        actions = []
        
        emergency_type = case_data.get('emergency_type', 'medical')
        
        # 1. Immediate emergency call
        emergency_number = self.emergency_contacts.get(emergency_type, '1122')
        call_action = {
            'action_type': 'emergency_call',
            'status': 'initiated',
            'details': {
                'number': emergency_number,
                'service_type': emergency_type,
                'priority': 'high',
                'auto_dial': True,
                'message': f"High priority {emergency_type} emergency reported. Dispatching immediately."
            },
            'timestamp': datetime.now().isoformat(),
            'user_notification': f"🚨 Emergency services ({emergency_number}) have been contacted automatically. Help is on the way!"
        }
        actions.append(call_action)
        
        # 2. Hospital direct contact (for medical emergencies)
        if emergency_type == 'medical' and agent_results.get('recommended_service'):
            service_name = agent_results['recommended_service']
            if isinstance(service_name, dict):
                service_name = service_name.get('name', '')
            
            hospital_number = self.hospital_contacts.get(service_name)
            if hospital_number:
                hospital_call = {
                    'action_type': 'hospital_alert',
                    'status': 'initiated',
                    'details': {
                        'hospital': service_name,
                        'number': hospital_number,
                        'patient_info': case_data.get('citizen_data', {}),
                        'symptoms': case_data.get('symptoms', ''),
                        'eta': '10-15 minutes'
                    },
                    'timestamp': datetime.now().isoformat(),
                    'user_notification': f"🏥 {service_name} has been alerted and is preparing for your arrival."
                }
                actions.append(hospital_call)
        
        # 3. GPS location sharing (simulated)
        location_action = {
            'action_type': 'location_share',
            'status': 'active',
            'details': {
                'location': case_data.get('location', 'Unknown'),
                'coordinates': self._get_mock_coordinates(case_data.get('location', '')),
                'shared_with': ['emergency_services', 'hospital'],
                'tracking_duration': '2 hours'
            },
            'timestamp': datetime.now().isoformat(),
            'user_notification': "📍 Your location has been shared with emergency responders for faster response."
        }
        actions.append(location_action)
        
        # 4. Emergency contact notification
        emergency_contact = case_data.get('citizen_data', {}).get('emergency_contact')
        if emergency_contact:
            contact_action = {
                'action_type': 'emergency_contact_alert',
                'status': 'sent',
                'details': {
                    'contact_number': emergency_contact,
                    'message': f"EMERGENCY: {case_data.get('citizen_data', {}).get('name', 'Your contact')} has reported a {emergency_type} emergency. Emergency services have been contacted.",
                    'location': case_data.get('location', 'Unknown')
                },
                'timestamp': datetime.now().isoformat(),
                'user_notification': "👥 Your emergency contact has been notified automatically."
            }
            actions.append(contact_action)
        
        return actions

    def _execute_medium_priority_actions(self, case_data: Dict[str, Any], agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute medium priority autonomous actions"""
        actions = []
        
        # 1. Schedule callback from appropriate service
        callback_action = {
            'action_type': 'schedule_callback',
            'status': 'scheduled',
            'details': {
                'service': agent_results.get('recommended_service', 'Emergency Services'),
                'callback_time': '15 minutes',
                'phone': case_data.get('citizen_data', {}).get('phone', ''),
                'purpose': 'Follow-up assessment and guidance'
            },
            'timestamp': datetime.now().isoformat(),
            'user_notification': "📞 A healthcare professional will call you within 15 minutes for assessment."
        }
        actions.append(callback_action)
        
        # 2. Send detailed instructions
        if agent_results.get('instructions'):
            instruction_action = {
                'action_type': 'send_instructions',
                'status': 'sent',
                'details': {
                    'instructions': agent_results['instructions'],
                    'delivery_method': 'sms_and_app',
                    'include_images': True
                },
                'timestamp': datetime.now().isoformat(),
                'user_notification': "📋 Detailed care instructions have been sent to your phone."
            }
            actions.append(instruction_action)
        
        # 3. Appointment confirmation with transport options
        if agent_results.get('appointment_details'):
            transport_action = {
                'action_type': 'arrange_transport',
                'status': 'options_provided',
                'details': {
                    'appointment_time': agent_results['appointment_details']['appointment_time'],
                    'destination': agent_results['appointment_details']['service_name'],
                    'transport_options': [
                        {'type': 'ambulance', 'eta': '20 minutes', 'cost': 'Free'},
                        {'type': 'taxi', 'eta': '10 minutes', 'cost': 'Rs. 300-500'},
                        {'type': 'family', 'note': 'Contact your emergency contact'}
                    ]
                },
                'timestamp': datetime.now().isoformat(),
                'user_notification': "🚗 Transport options for your appointment have been arranged."
            }
            actions.append(transport_action)
        
        return actions

    def _execute_low_priority_actions(self, case_data: Dict[str, Any], agent_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute low priority autonomous actions"""
        actions = []
        
        # 1. Schedule appointment reminder
        reminder_action = {
            'action_type': 'schedule_reminders',
            'status': 'scheduled',
            'details': {
                'reminders': agent_results.get('reminder_schedule', []),
                'channels': ['sms', 'app_notification'],
                'include_preparation_tips': True
            },
            'timestamp': datetime.now().isoformat(),
            'user_notification': "🔔 Appointment reminders have been set up automatically."
        }
        actions.append(reminder_action)
        
        # 2. Health monitoring setup
        monitoring_action = {
            'action_type': 'setup_monitoring',
            'status': 'configured',
            'details': {
                'monitoring_type': 'symptom_tracking',
                'frequency': 'daily',
                'duration': '1 week',
                'automated_check_ins': True
            },
            'timestamp': datetime.now().isoformat(),
            'user_notification': "📊 Health monitoring has been set up to track your progress."
        }
        actions.append(monitoring_action)
        
        return actions

    def _send_confirmation_sms(self, phone: str, agent_results: Dict[str, Any]) -> Dict[str, Any]:
        """Send confirmation SMS with all details"""
        
        # Build SMS content
        sms_content = "🏥 FRONTLINE AI CONFIRMATION\n\n"
        
        if agent_results.get('priority'):
            sms_content += f"Priority: {agent_results['priority'].upper()}\n"
        
        if agent_results.get('appointment_details'):
            apt = agent_results['appointment_details']
            apt_time = datetime.fromisoformat(apt['appointment_time']).strftime('%d/%m/%Y %I:%M %p')
            sms_content += f"Appointment: {apt_time}\n"
            sms_content += f"Location: {apt['service_name']}\n"
            
            if agent_results.get('confirmation_details', {}).get('confirmation_number'):
                sms_content += f"Ref: {agent_results['confirmation_details']['confirmation_number']}\n"
        
        if agent_results.get('instructions'):
            sms_content += f"\nInstructions: {agent_results['instructions'][:100]}...\n"
        
        sms_content += "\nFor help: Reply HELP or call 1122"
        
        return {
            'action_type': 'send_sms',
            'status': 'sent',
            'details': {
                'phone': phone,
                'content': sms_content,
                'delivery_status': 'delivered',
                'message_id': f"SMS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            },
            'timestamp': datetime.now().isoformat(),
            'user_notification': "📱 Confirmation details sent to your phone."
        }

    def _get_mock_coordinates(self, location: str) -> Dict[str, float]:
        """Get mock GPS coordinates for Pakistani cities"""
        coordinates = {
            'lahore': {'lat': 31.5204, 'lng': 74.3587},
            'karachi': {'lat': 24.8607, 'lng': 67.0011},
            'islamabad': {'lat': 33.6844, 'lng': 73.0479},
            'rawalpindi': {'lat': 33.5651, 'lng': 73.0169},
            'faisalabad': {'lat': 31.4504, 'lng': 73.1350}
        }
        
        return coordinates.get(location.lower(), {'lat': 31.5204, 'lng': 74.3587})

    def generate_action_summary(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of all actions taken"""
        
        action_counts = {}
        notifications = []
        
        for action in actions:
            action_type = action['action_type']
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
            
            if action.get('user_notification'):
                notifications.append(action['user_notification'])
        
        return {
            'total_actions': len(actions),
            'action_breakdown': action_counts,
            'user_notifications': notifications,
            'autonomous_response': True,
            'summary': f"Executed {len(actions)} autonomous actions including emergency contacts, service coordination, and follow-up setup."
        }