"""
Follow-up Agent - Reminders and progress tracking
"""
import logging
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class FollowupAgent:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def process(self, case_data, system_status):
        """Process follow-up scheduling and tracking"""
        logger.info("FollowupAgent processing case")
        
        appointment_details = case_data.get('appointment_details', {})
        citizen_data = case_data.get('citizen_data', {})
        service_type = case_data.get('emergency_type', 'medical')
        priority = case_data.get('priority', 'medium')
        
        # Schedule reminders
        reminders = self.schedule_reminders(appointment_details, priority)
        
        # Generate tracking system
        tracking_system = self.generate_tracking_system(case_data)
        
        # Create follow-up plan
        followup_plan = self.create_followup_plan(service_type, priority)
        
        result = {
            'reminder_schedule': reminders,
            'tracking_system': tracking_system,
            'followup_plan': followup_plan,
            'contact_methods': self.determine_contact_methods(citizen_data),
            'agent': 'followup_agent',
            'timestamp': self.get_timestamp()
        }
        
        logger.info(f"Follow-up result: {result}")
        return result
    
    def schedule_reminders(self, appointment_details, priority):
        """Schedule reminders based on appointment and priority"""
        try:
            appointment_time = datetime.fromisoformat(appointment_details['appointment_time'].replace('Z', '+00:00'))
        except:
            # Fallback: 1 hour from now
            appointment_time = datetime.now() + timedelta(hours=1)
        
        reminders = []
        
        # High priority: multiple urgent reminders
        if priority == 'high':
            reminders.extend([
                {
                    'type': 'immediate_reminder',
                    'scheduled_time': (datetime.now() + timedelta(minutes=5)).isoformat(),
                    'message': 'EMERGENCY: Your appointment is confirmed. Proceed immediately.',
                    'channel': 'sms_priority'
                },
                {
                    'type': 'follow_up_1hr',
                    'scheduled_time': (appointment_time + timedelta(hours=1)).isoformat(),
                    'message': 'Follow-up: How was your emergency service experience?',
                    'channel': 'sms'
                }
            ])
        
        # Medium priority: standard reminders
        elif priority == 'medium':
            reminders.extend([
                {
                    'type': '24_hour_reminder',
                    'scheduled_time': (appointment_time - timedelta(hours=24)).isoformat(),
                    'message': f"Reminder: Your urgent appointment is in 24 hours at {appointment_time.strftime('%I:%M %p')}",
                    'channel': 'sms'
                },
                {
                    'type': '2_hour_reminder',
                    'scheduled_time': (appointment_time - timedelta(hours=2)).isoformat(),
                    'message': f"Reminder: Your appointment is in 2 hours. Please prepare to leave.",
                    'channel': 'sms'
                },
                {
                    'type': 'post_appointment_followup',
                    'scheduled_time': (appointment_time + timedelta(days=1)).isoformat(),
                    'message': 'Follow-up: How was your service experience?',
                    'channel': 'sms'
                }
            ])
        
        # Low priority: basic reminders
        else:
            reminders.extend([
                {
                    'type': '48_hour_reminder',
                    'scheduled_time': (appointment_time - timedelta(hours=48)).isoformat(),
                    'message': f"Reminder: Your appointment is in 48 hours.",
                    'channel': 'email'
                },
                {
                    'type': 'same_day_reminder',
                    'scheduled_time': (appointment_time.replace(hour=9, minute=0, second=0)).isoformat(),  # 9 AM on appointment day
                    'message': f"Reminder: Your appointment is today at {appointment_time.strftime('%I:%M %p')}",
                    'channel': 'sms'
                }
            ])
        
        return reminders
    
    def generate_tracking_system(self, case_data):
        """Generate case tracking system"""
        case_id = case_data.get('case_id', f"case_{random.randint(10000, 99999)}")
        
        return {
            'tracking_id': case_id,
            'status': 'in_progress',
            'current_stage': 'appointment_scheduled',
            'next_milestone': 'service_completion',
            'estimated_completion': self.estimate_completion_time(case_data.get('priority', 'medium')),
            'update_frequency': self.determine_update_frequency(case_data.get('priority', 'medium')),
            'tracking_url': f"https://tracking.frontline.gov.pk/cases/{case_id}",
            'support_contact': '1800-HELP-NOW'
        }
    
    def create_followup_plan(self, service_type, priority):
        """Create service-specific follow-up plan"""
        plans = {
            'medical': {
                'high': [
                    'Immediate post-treatment check',
                    '24-hour follow-up call',
                    'Medication adherence check',
                    '1-week progress assessment'
                ],
                'medium': [
                    'Post-appointment feedback',
                    '3-day symptom check',
                    '1-week follow-up call'
                ],
                'low': [
                    'Post-visit satisfaction survey',
                    '2-week check-in'
                ]
            },
            'police': {
                'high': [
                    'Immediate case status update',
                    'Daily progress reports',
                    'Victim support follow-up'
                ],
                'medium': [
                    'Case assignment confirmation',
                    'Weekly status updates',
                    'Resolution follow-up'
                ],
                'low': [
                    'Case submission confirmation',
                    'Final resolution update'
                ]
            }
        }
        
        service_plan = plans.get(service_type, {}).get(priority, ['Standard follow-up sequence'])
        
        return {
            'service_type': service_type,
            'priority_level': priority,
            'followup_steps': service_plan,
            'expected_duration': self.estimate_followup_duration(priority),
            'success_metrics': self.define_success_metrics(service_type)
        }
    
    def determine_contact_methods(self, citizen_data):
        """Determine available contact methods"""
        methods = []
        
        if citizen_data.get('phone'):
            methods.append({
                'method': 'sms',
                'priority': 'high',
                'number': citizen_data['phone']
            })
        
        if citizen_data.get('email'):
            methods.append({
                'method': 'email',
                'priority': 'medium',
                'address': citizen_data['email']
            })
        
        if citizen_data.get('whatsapp'):
            methods.append({
                'method': 'whatsapp',
                'priority': 'high',
                'number': citizen_data['whatsapp']
            })
        
        # Fallback method
        if not methods:
            methods.append({
                'method': 'in_app_notifications',
                'priority': 'medium',
                'description': 'Application notifications'
            })
        
        return methods
    
    def estimate_completion_time(self, priority):
        """Estimate case completion time"""
        estimates = {
            'high': '24-48 hours',
            'medium': '3-7 days',
            'low': '1-2 weeks'
        }
        return estimates.get(priority, '1-2 weeks')
    
    def determine_update_frequency(self, priority):
        """Determine how often to provide updates"""
        frequencies = {
            'high': 'Every 4 hours',
            'medium': 'Daily',
            'low': 'Every 3 days'
        }
        return frequencies.get(priority, 'Daily')
    
    def estimate_followup_duration(self, priority):
        """Estimate follow-up duration"""
        durations = {
            'high': '2-4 weeks',
            'medium': '1-2 weeks',
            'low': '1 week'
        }
        return durations.get(priority, '1-2 weeks')
    
    def define_success_metrics(self, service_type):
        """Define success metrics for the service"""
        metrics = {
            'medical': ['Symptom resolution', 'Patient satisfaction', 'Treatment adherence'],
            'police': ['Case resolution', 'Response time', 'Citizen satisfaction'],
            'fire': ['Safety compliance', 'Prevention measures', 'Response effectiveness']
        }
        return metrics.get(service_type, ['Service completion', 'Citizen satisfaction'])
    
    def get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
