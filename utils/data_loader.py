"""
Data loader for integrating mock datasets
"""
import json
import pandas as pd
import logging
import os
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)

class DataLoader:
    def __init__(self):
        self.loaded_datasets = {}
        self.load_all_datasets()
    
    def load_all_datasets(self):
        """Load all mock datasets"""
        try:
            # Load emergency requests
            self.loaded_datasets['emergency_requests'] = self.load_emergency_requests()
            
            # Load hospital data
            self.loaded_datasets['hospitals'] = self.load_hospital_data()
            
            # Load Pakistan location data
            self.loaded_datasets['locations'] = self.load_location_data()
            
            # Load emergency protocols
            self.loaded_datasets['protocols'] = self.load_emergency_protocols()
            
            logger.info(f"✅ Loaded {len(self.loaded_datasets)} datasets")
            
        except Exception as e:
            logger.error(f"❌ Error loading datasets: {str(e)}")
            # Load mock fallback data
            self.loaded_datasets = self.load_mock_fallback_data()
    
    def load_emergency_requests(self):
        """Load frontline worker requests data"""
        try:
            with open('data/frontline_worker_requests_clean_2_20.json', 'r') as f:
                data = json.load(f)
                logger.info(f"✅ Loaded {len(data)} emergency requests")
                return data
        except Exception as e:
            logger.warning(f"⚠️ Using mock emergency requests: {str(e)}")
            return self.generate_mock_emergency_requests()
    
    def load_hospital_data(self):
        """Load hospital data from PDF or create mock data"""
        try:
            # Try to extract from PDF
            if os.path.exists('data/hospitals.pdf'):
                return self.extract_hospital_data_from_pdf()
            else:
                return self.generate_mock_hospital_data()
        except Exception as e:
            logger.warning(f"⚠️ Using mock hospital data: {str(e)}")
            return self.generate_mock_hospital_data()
    
    def load_location_data(self):
        """Load Pakistan location data"""
        try:
            if os.path.exists('data/pakistan.csv'):
                df = pd.read_csv('data/pakistan.csv')
                return df.to_dict('records')
            else:
                return self.generate_mock_location_data()
        except Exception as e:
            logger.warning(f"⚠️ Using mock location data: {str(e)}")
            return self.generate_mock_location_data()
    
    def load_emergency_protocols(self):
        """Load emergency protocols"""
        return {
            'medical': {
                'high_priority': 'Immediate emergency response',
                'medium_priority': 'Urgent care within 2 hours',
                'low_priority': 'Primary care appointment'
            },
            'police': {
                'high_priority': 'Immediate dispatch',
                'medium_priority': 'Officer response within 1 hour',
                'low_priority': 'File report at station'
            },
            'fire': {
                'high_priority': 'Immediate fire response',
                'medium_priority': 'Fire safety inspection',
                'low_priority': 'Prevention advisory'
            }
        }
    
    def extract_hospital_data_from_pdf(self):
        """Extract hospital data from PDF"""
        try:
            with open('data/hospitals.pdf', 'rb') as file:
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                
                # Simple extraction - customize based on your PDF structure
                hospitals = []
                lines = text.split('\n')
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['hospital', 'medical', 'clinic']):
                        hospitals.append({
                            'name': line.strip(),
                            'type': 'hospital',
                            'location': 'Pakistan'  # Extract from text if available
                        })
                
                return hospitals if hospitals else self.generate_mock_hospital_data()
        except:
            return self.generate_mock_hospital_data()
    
    # Mock data generators
    def generate_mock_emergency_requests(self):
        return [
            {
                "request_id": "req_001",
                "symptoms": "chest pain and difficulty breathing",
                "emergency_type": "medical",
                "location": "Lahore",
                "priority": "high",
                "timestamp": "2024-01-15T08:30:00"
            },
            {
                "request_id": "req_002", 
                "symptoms": "high fever for 3 days",
                "emergency_type": "medical",
                "location": "Karachi",
                "priority": "medium",
                "timestamp": "2024-01-15T09:15:00"
            }
        ]
    
    def generate_mock_hospital_data(self):
        return [
            {
                "hospital_id": "H001",
                "name": "Jinnah Hospital Lahore",
                "location": "Lahore",
                "type": "General Hospital",
                "emergency_contact": "042-111-111-111",
                "beds_available": 25,
                "specialties": ["Emergency", "Cardiology", "Surgery"]
            },
            {
                "hospital_id": "H002",
                "name": "Aga Khan Hospital Karachi",
                "location": "Karachi", 
                "type": "Specialized Hospital",
                "emergency_contact": "021-222-222-222",
                "beds_available": 15,
                "specialties": ["Emergency", "Oncology", "Neurology"]
            }
        ]
    
    def generate_mock_location_data(self):
        return [
            {"city": "Lahore", "province": "Punjab", "emergency_services": 15},
            {"city": "Karachi", "province": "Sindh", "emergency_services": 20},
            {"city": "Islamabad", "province": "Federal", "emergency_services": 10}
        ]
    
    def get_mock_fallback_data(self):
        """Fallback when no datasets are available"""
        return {
            'emergency_requests': self.generate_mock_emergency_requests(),
            'hospitals': self.generate_mock_hospital_data(),
            'locations': self.generate_mock_location_data(),
            'protocols': self.load_emergency_protocols()
        }
    
    def query_data(self, dataset_name, filters=None):
        """Query datasets with filters"""
        if dataset_name not in self.loaded_datasets:
            return []
        
        data = self.loaded_datasets[dataset_name]
        if not filters:
            return data
        
        # Apply filters
        filtered_data = []
        for item in data:
            match = True
            for key, value in filters.items():
                if key in item:
                    if isinstance(value, list):
                        if item[key] not in value:
                            match = False
                            break
                    else:
                        if item[key] != value:
                            match = False
                            break
                else:
                    match = False
                    break
            if match:
                filtered_data.append(item)
        
        return filtered_data
