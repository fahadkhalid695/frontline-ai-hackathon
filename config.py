"""
Configuration settings for Frontline Worker AI
"""
import os

# GCP Configuration
PROJECT_ID = os.environ.get('GCP_PROJECT', 'frontline-ai-hackathon')
FIRESTORE_COLLECTION = 'cases'

# Service Configuration
HOSPITALS = {
    'lahore': ['Jinnah Hospital', 'Services Hospital', 'General Hospital'],
    'karachi': ['Aga Khan Hospital', 'Civil Hospital', 'Jinnah Postgraduate Medical Centre'],
    'islamabad': ['Pakistan Institute of Medical Sciences', 'Shifa International Hospital']
}

POLICE_STATIONS = {
    'lahore': ['Model Town Police Station', 'Gulberg Police Station', 'Cantt Police Station'],
    'karachi': ['Clifton Police Station', 'Saddar Police Station', 'Gulshan Police Station'],
    'islamabad': ['Margalla Police Station', 'Shalimar Police Station', 'Aabpara Police Station']
}

# Degraded Mode Settings
DEGRADED_MODE_TIMEOUT = 3  # seconds for connectivity check
CACHE_DURATION = 300  # 5 minutes for cached data

# Emergency Priority Thresholds
HIGH_PRIORITY_KEYWORDS = ['chest pain', 'bleeding', 'unconscious', 'heart attack', 'stroke']
MEDIUM_PRIORITY_KEYWORDS = ['fever', 'pain', 'accident', 'broken', 'cut']
