"""
Parsing Agent - Intelligent natural language understanding for emergency situations
"""
import logging
import re
from datetime import datetime
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class ParsingAgent:
    def __init__(self):
        self.medical_keywords = {
            'high_priority': [
                'chest pain', 'heart attack', 'stroke', 'unconscious', 'not breathing',
                'severe bleeding', 'overdose', 'suicide', 'cardiac arrest', 'choking',
                'severe burn', 'head injury', 'spinal injury', 'allergic reaction',
                'difficulty breathing', 'can\'t breathe', 'shortness of breath'
            ],
            'medium_priority': [
                'fever', 'vomiting', 'diarrhea', 'pain', 'broken bone', 'cut',
                'burn', 'fall', 'accident', 'bleeding', 'dizzy', 'nausea',
                'headache', 'stomach pain', 'back pain', 'sprained'
            ],
            'low_priority': [
                'cold', 'cough', 'minor cut', 'bruise', 'rash', 'sore throat',
                'runny nose', 'minor headache', 'tired', 'fatigue'
            ]
        }
        
        self.police_keywords = {
            'high_priority': [
                'robbery', 'burglary', 'assault', 'attack', 'shooting', 'stabbing',
                'domestic violence', 'kidnapping', 'rape', 'murder', 'threat',
                'weapon', 'gun', 'knife', 'violence', 'break in', 'breaking in'
            ],
            'medium_priority': [
                'theft', 'stolen', 'vandalism', 'harassment', 'suspicious person',
                'noise complaint', 'disturbance', 'fraud', 'scam', 'lost child'
            ],
            'low_priority': [
                'parking violation', 'minor dispute', 'lost property', 'noise'
            ]
        }
        
        self.fire_keywords = {
            'high_priority': [
                'fire', 'burning', 'smoke', 'explosion', 'gas leak', 'chemical spill',
                'building collapse', 'trapped', 'can\'t escape'
            ],
            'medium_priority': [
                'small fire', 'electrical problem', 'gas smell', 'smoke alarm'
            ],
            'low_priority': [
                'fire safety inspection', 'smoke detector'
            ]
        }
        
        self.location_patterns = [
            r'at (.+?)(?:\.|$|,)',
            r'in (.+?)(?:\.|$|,)',
            r'on (.+?)(?:\.|$|,)',
            r'near (.+?)(?:\.|$|,)',
            r'address is (.+?)(?:\.|$|,)',
            r'location (.+?)(?:\.|$|,)'
        ]
        
        self.personal_info_patterns = {
            'age': r'(?:i am|i\'m|age|years old)\s*(\d+)',
            'name': r'(?:my name is|i am|i\'m|name is)\s*([a-zA-Z\s]+)',
            'phone': r'(?:phone|number|call me|contact)\s*(?:is|at)?\s*([\+\d\s\-\(\)]+)'
        }

    def parse_emergency_input(self, user_input: str) -> Dict[str, Any]:
        """Parse natural language emergency input into structured data"""
        logger.info(f"Parsing emergency input: {user_input}")
        
        user_input_lower = user_input.lower()
        
        # Determine emergency type and priority
        emergency_type, priority = self._classify_emergency(user_input_lower)
        
        # Extract location
        location = self._extract_location(user_input)
        
        # Extract personal information
        personal_info = self._extract_personal_info(user_input)
        
        # Generate summary
        summary = self._generate_summary(user_input, emergency_type, priority)
        
        # Extract symptoms/incident details
        symptoms = self._extract_symptoms_or_incident(user_input, emergency_type)
        
        # Build case data
        case_data = {
            'symptoms': symptoms,
            'emergency_type': emergency_type,
            'location': location or 'Unknown',
            'citizen_data': {
                'name': personal_info.get('name', ''),
                'age': personal_info.get('age', 0),
                'phone': personal_info.get('phone', ''),
                'medical_conditions': [],
                'incident_details': user_input if emergency_type != 'medical' else ''
            },
            'priority': priority,
            'original_input': user_input,
            'parsed_timestamp': datetime.now().isoformat()
        }
        
        result = {
            'emergency_type': emergency_type,
            'priority': priority,
            'summary': summary,
            'case_data': case_data,
            'confidence': self._calculate_confidence(user_input, emergency_type, priority),
            'suggested_actions': self._suggest_immediate_actions(emergency_type, priority)
        }
        
        logger.info(f"Parsed result: {result}")
        return result

    def _classify_emergency(self, user_input: str) -> Tuple[str, str]:
        """Classify the type of emergency and its priority"""
        
        # Check for medical emergency
        medical_score = self._calculate_keyword_score(user_input, self.medical_keywords)
        police_score = self._calculate_keyword_score(user_input, self.police_keywords)
        fire_score = self._calculate_keyword_score(user_input, self.fire_keywords)
        
        # Determine emergency type
        max_score = max(medical_score['total'], police_score['total'], fire_score['total'])
        
        if max_score == 0:
            # Default to medical if no clear indicators
            emergency_type = 'medical'
            priority = 'low'
        elif medical_score['total'] == max_score:
            emergency_type = 'medical'
            priority = self._determine_priority(medical_score)
        elif police_score['total'] == max_score:
            emergency_type = 'police'
            priority = self._determine_priority(police_score)
        else:
            emergency_type = 'fire'
            priority = self._determine_priority(fire_score)
        
        return emergency_type, priority

    def _calculate_keyword_score(self, user_input: str, keywords: Dict[str, List[str]]) -> Dict[str, int]:
        """Calculate keyword matching score for emergency classification"""
        scores = {'high_priority': 0, 'medium_priority': 0, 'low_priority': 0}
        
        for priority_level, keyword_list in keywords.items():
            for keyword in keyword_list:
                if keyword in user_input:
                    scores[priority_level] += 1
        
        scores['total'] = sum(scores.values())
        return scores

    def _determine_priority(self, scores: Dict[str, int]) -> str:
        """Determine priority based on keyword scores"""
        if scores['high_priority'] > 0:
            return 'high'
        elif scores['medium_priority'] > 0:
            return 'medium'
        else:
            return 'low'

    def _extract_location(self, user_input: str) -> str:
        """Extract location from user input"""
        # Pakistani cities
        pakistani_cities = [
            'lahore', 'karachi', 'islamabad', 'rawalpindi', 'faisalabad',
            'multan', 'peshawar', 'quetta', 'sialkot', 'gujranwala'
        ]
        
        user_input_lower = user_input.lower()
        
        # Check for Pakistani cities
        for city in pakistani_cities:
            if city in user_input_lower:
                return city.title()
        
        # Try to extract location using patterns
        for pattern in self.location_patterns:
            match = re.search(pattern, user_input_lower)
            if match:
                location = match.group(1).strip()
                # Clean up the location
                location = re.sub(r'[^\w\s]', '', location)
                if len(location) > 2:
                    return location.title()
        
        return 'Lahore'  # Default location

    def _extract_personal_info(self, user_input: str) -> Dict[str, Any]:
        """Extract personal information from user input"""
        info = {}
        
        for info_type, pattern in self.personal_info_patterns.items():
            match = re.search(pattern, user_input.lower())
            if match:
                value = match.group(1).strip()
                
                if info_type == 'age':
                    try:
                        info['age'] = int(value)
                    except ValueError:
                        pass
                elif info_type == 'name':
                    # Clean up name
                    name = re.sub(r'[^\w\s]', '', value).title()
                    if len(name) > 1:
                        info['name'] = name
                elif info_type == 'phone':
                    # Clean up phone number
                    phone = re.sub(r'[^\d\+]', '', value)
                    if len(phone) >= 10:
                        info['phone'] = phone
        
        return info

    def _extract_symptoms_or_incident(self, user_input: str, emergency_type: str) -> str:
        """Extract symptoms for medical or incident description for others"""
        if emergency_type == 'medical':
            # For medical, try to extract symptom-related text
            medical_indicators = [
                'pain', 'hurt', 'ache', 'feel', 'symptom', 'sick', 'ill',
                'bleeding', 'fever', 'dizzy', 'nausea', 'vomit', 'breath'
            ]
            
            sentences = user_input.split('.')
            symptom_sentences = []
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                if any(indicator in sentence_lower for indicator in medical_indicators):
                    symptom_sentences.append(sentence.strip())
            
            if symptom_sentences:
                return '. '.join(symptom_sentences)
            else:
                return user_input
        else:
            # For police/fire, return the full incident description
            return user_input

    def _generate_summary(self, user_input: str, emergency_type: str, priority: str) -> str:
        """Generate a concise summary of the emergency"""
        
        # Extract key phrases
        key_phrases = []
        
        if emergency_type == 'medical':
            medical_terms = []
            for priority_level, keywords in self.medical_keywords.items():
                for keyword in keywords:
                    if keyword in user_input.lower():
                        medical_terms.append(keyword)
            
            if medical_terms:
                key_phrases.extend(medical_terms[:2])  # Top 2 medical terms
        
        elif emergency_type == 'police':
            police_terms = []
            for priority_level, keywords in self.police_keywords.items():
                for keyword in keywords:
                    if keyword in user_input.lower():
                        police_terms.append(keyword)
            
            if police_terms:
                key_phrases.extend(police_terms[:2])
        
        elif emergency_type == 'fire':
            fire_terms = []
            for priority_level, keywords in self.fire_keywords.items():
                for keyword in keywords:
                    if keyword in user_input.lower():
                        fire_terms.append(keyword)
            
            if fire_terms:
                key_phrases.extend(fire_terms[:2])
        
        if key_phrases:
            summary = f"{priority} priority {emergency_type} emergency involving {', '.join(key_phrases)}"
        else:
            summary = f"{priority} priority {emergency_type} emergency"
        
        return summary

    def _calculate_confidence(self, user_input: str, emergency_type: str, priority: str) -> float:
        """Calculate confidence score for the parsing"""
        
        # Base confidence
        confidence = 0.5
        
        # Increase confidence based on keyword matches
        if emergency_type == 'medical':
            score = self._calculate_keyword_score(user_input.lower(), self.medical_keywords)
        elif emergency_type == 'police':
            score = self._calculate_keyword_score(user_input.lower(), self.police_keywords)
        else:
            score = self._calculate_keyword_score(user_input.lower(), self.fire_keywords)
        
        # Adjust confidence based on matches
        if score['total'] > 0:
            confidence += min(0.4, score['total'] * 0.1)
        
        # Increase confidence if location is detected
        location = self._extract_location(user_input)
        if location and location != 'Lahore':  # Not default
            confidence += 0.1
        
        # Increase confidence if personal info is detected
        personal_info = self._extract_personal_info(user_input)
        if personal_info:
            confidence += len(personal_info) * 0.05
        
        return min(1.0, confidence)

    def _suggest_immediate_actions(self, emergency_type: str, priority: str) -> List[str]:
        """Suggest immediate actions based on emergency type and priority"""
        
        actions = []
        
        if priority == 'high':
            actions.append("Immediately contact emergency services")
            if emergency_type == 'medical':
                actions.extend([
                    "Stay calm and keep the person conscious if possible",
                    "Do not move the person unless in immediate danger",
                    "Be ready to provide CPR if needed"
                ])
            elif emergency_type == 'police':
                actions.extend([
                    "Ensure your safety first",
                    "Move to a safe location if possible",
                    "Do not confront the perpetrator"
                ])
            elif emergency_type == 'fire':
                actions.extend([
                    "Evacuate immediately if safe to do so",
                    "Stay low to avoid smoke",
                    "Do not use elevators"
                ])
        
        elif priority == 'medium':
            actions.append("Seek appropriate medical/emergency attention within 2 hours")
            actions.append("Monitor the situation closely")
        
        else:
            actions.append("Schedule appropriate care when convenient")
            actions.append("Monitor symptoms and seek help if they worsen")
        
        return actions