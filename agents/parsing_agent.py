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
        # Enhanced medical keywords with more comprehensive training data
        self.medical_keywords = {
            'high_priority': [
                # Cardiac emergencies
                'chest pain', 'heart attack', 'cardiac arrest', 'heart palpitations', 'chest tightness',
                'crushing chest pain', 'radiating pain', 'left arm pain', 'jaw pain',
                
                # Respiratory emergencies  
                'difficulty breathing', 'can\'t breathe', 'shortness of breath', 'not breathing',
                'choking', 'gasping for air', 'blue lips', 'wheezing severely',
                
                # Neurological emergencies
                'stroke', 'unconscious', 'seizure', 'head injury', 'spinal injury',
                'paralysis', 'can\'t move', 'slurred speech', 'confusion', 'loss of consciousness',
                
                # Trauma emergencies
                'severe bleeding', 'heavy bleeding', 'blood loss', 'deep cut', 'stabbed',
                'shot', 'gunshot', 'severe burn', 'third degree burn', 'explosion',
                
                # Poisoning/overdose
                'overdose', 'poisoned', 'suicide attempt', 'drug overdose', 'chemical exposure',
                
                # Allergic reactions
                'allergic reaction', 'anaphylaxis', 'swollen throat', 'hives all over',
                
                # Obstetric emergencies
                'labor pains', 'water broke', 'pregnancy bleeding', 'miscarriage'
            ],
            'medium_priority': [
                # General pain and injuries
                'severe pain', 'broken bone', 'fracture', 'sprained ankle', 'dislocated',
                'fall', 'accident', 'cut', 'burn', 'bleeding', 'wound',
                
                # Infections and fever
                'high fever', 'fever over 102', 'infection', 'severe headache',
                'stiff neck', 'rash with fever',
                
                # Gastrointestinal
                'severe vomiting', 'blood in vomit', 'severe diarrhea', 'dehydration',
                'severe stomach pain', 'appendicitis symptoms',
                
                # Other concerning symptoms
                'dizzy', 'fainting', 'nausea', 'severe headache', 'migraine',
                'back pain', 'kidney pain', 'urinary problems'
            ],
            'low_priority': [
                'cold', 'cough', 'runny nose', 'sore throat', 'minor headache',
                'tired', 'fatigue', 'minor cut', 'small bruise', 'rash',
                'mild fever', 'upset stomach', 'constipation', 'minor ache'
            ]
        }
        
        self.police_keywords = {
            'high_priority': [
                # Violent crimes
                'robbery', 'armed robbery', 'burglary', 'home invasion', 'break in', 'breaking in',
                'assault', 'attack', 'beating', 'mugging', 'carjacking',
                
                # Weapons involved
                'shooting', 'gunshot', 'stabbing', 'knife attack', 'weapon', 'gun', 'knife',
                'armed', 'threatened with weapon', 'pistol', 'rifle',
                
                # Serious crimes
                'kidnapping', 'abduction', 'rape', 'sexual assault', 'murder', 'homicide',
                'domestic violence', 'child abuse', 'human trafficking',
                
                # Immediate threats
                'threat to kill', 'death threat', 'bomb threat', 'terrorist', 'explosion',
                'active shooter', 'hostage situation', 'gang violence',
                
                # Drug-related violence
                'drug deal gone wrong', 'drug violence', 'dealer threatening'
            ],
            'medium_priority': [
                'theft', 'stolen car', 'stolen property', 'pickpocket', 'shoplifting',
                'vandalism', 'property damage', 'graffiti', 'broken windows',
                'harassment', 'stalking', 'threatening behavior', 'suspicious person',
                'noise complaint', 'disturbance', 'loud party', 'neighbor dispute',
                'fraud', 'scam', 'identity theft', 'credit card fraud',
                'lost child', 'missing person', 'runaway', 'trespassing'
            ],
            'low_priority': [
                'parking violation', 'minor dispute', 'lost property', 'noise',
                'littering', 'minor traffic violation', 'civil matter'
            ]
        }
        
        self.fire_keywords = {
            'high_priority': [
                # Active fires
                'fire', 'house fire', 'building fire', 'forest fire', 'car fire',
                'burning', 'flames', 'smoke everywhere', 'heavy smoke',
                
                # Explosions and hazards
                'explosion', 'blast', 'gas explosion', 'chemical explosion',
                'gas leak', 'propane leak', 'natural gas smell', 'chemical spill',
                'toxic fumes', 'hazardous materials',
                
                # Structural emergencies
                'building collapse', 'roof collapse', 'wall falling', 'structural damage',
                'earthquake damage', 'flood damage',
                
                # Rescue situations
                'trapped in fire', 'can\'t escape', 'people trapped', 'rescue needed',
                'elevator stuck', 'confined space rescue'
            ],
            'medium_priority': [
                'small fire', 'kitchen fire', 'electrical fire', 'electrical problem',
                'sparks', 'overheating', 'burning smell', 'gas smell',
                'smoke alarm going off', 'carbon monoxide alarm', 'water leak'
            ],
            'low_priority': [
                'fire safety inspection', 'smoke detector battery', 'fire prevention',
                'safety check', 'fire extinguisher check'
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

    def parse_emergency_input(self, user_input: str, location_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Parse natural language emergency input into structured data"""
        logger.info(f"Parsing emergency input: {user_input}")
        
        user_input_lower = user_input.lower()
        
        # Determine emergency type and priority
        emergency_type, priority = self._classify_emergency(user_input_lower)
        
        # Extract location (prioritize GPS data if available)
        location = self._extract_location(user_input, location_data)
        
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
        """Classify the type of emergency and its priority with advanced pattern recognition"""
        
        # Enhanced scoring with context analysis
        medical_score = self._calculate_enhanced_score(user_input, self.medical_keywords, 'medical')
        police_score = self._calculate_enhanced_score(user_input, self.police_keywords, 'police')
        fire_score = self._calculate_enhanced_score(user_input, self.fire_keywords, 'fire')
        
        # Context-based adjustments
        medical_score = self._apply_context_adjustments(user_input, medical_score, 'medical')
        police_score = self._apply_context_adjustments(user_input, police_score, 'police')
        fire_score = self._apply_context_adjustments(user_input, fire_score, 'fire')
        
        # Determine emergency type
        max_score = max(medical_score['total'], police_score['total'], fire_score['total'])
        
        if max_score == 0:
            # Use intelligent fallback based on context clues
            emergency_type, priority = self._intelligent_fallback_classification(user_input)
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

    def _calculate_enhanced_score(self, user_input: str, keywords: Dict[str, List[str]], category: str) -> Dict[str, int]:
        """Enhanced scoring with phrase matching and context"""
        scores = {'high_priority': 0, 'medium_priority': 0, 'low_priority': 0}
        
        for priority_level, keyword_list in keywords.items():
            for keyword in keyword_list:
                # Exact phrase matching (higher weight)
                if keyword in user_input:
                    scores[priority_level] += 2
                
                # Partial word matching (lower weight)
                keyword_words = keyword.split()
                if len(keyword_words) > 1:
                    word_matches = sum(1 for word in keyword_words if word in user_input)
                    if word_matches >= len(keyword_words) * 0.7:  # 70% of words match
                        scores[priority_level] += 1
        
        scores['total'] = sum(scores.values())
        return scores

    def _apply_context_adjustments(self, user_input: str, scores: Dict[str, int], category: str) -> Dict[str, int]:
        """Apply context-based adjustments to improve accuracy"""
        
        # Urgency indicators
        urgency_words = ['help', 'emergency', 'urgent', 'now', 'immediately', 'asap', 'hurry', '911', '1122']
        urgency_count = sum(1 for word in urgency_words if word in user_input.lower())
        
        if urgency_count > 0:
            scores['high_priority'] += urgency_count
        
        # Severity indicators
        severity_words = ['severe', 'serious', 'critical', 'life threatening', 'dying', 'critical condition']
        severity_count = sum(1 for word in severity_words if word in user_input.lower())
        
        if severity_count > 0:
            scores['high_priority'] += severity_count * 2
        
        # Time-based urgency
        time_urgent = ['right now', 'happening now', 'currently', 'at this moment']
        if any(phrase in user_input.lower() for phrase in time_urgent):
            scores['high_priority'] += 2
        
        # Multiple victim indicators
        multiple_victims = ['multiple people', 'several people', 'many injured', 'mass casualty']
        if any(phrase in user_input.lower() for phrase in multiple_victims):
            scores['high_priority'] += 3
        
        # Age-based priority (children, elderly)
        age_priority = ['child', 'baby', 'infant', 'elderly', 'old person', 'senior citizen']
        if any(word in user_input.lower() for word in age_priority):
            scores['high_priority'] += 1
        
        scores['total'] = sum(scores.values())
        return scores

    def _intelligent_fallback_classification(self, user_input: str) -> Tuple[str, str]:
        """Intelligent fallback when no clear keywords match"""
        
        # Look for general emergency indicators
        emergency_indicators = {
            'medical': ['hurt', 'pain', 'sick', 'ill', 'injured', 'bleeding', 'unconscious', 'fell', 'accident'],
            'police': ['crime', 'criminal', 'thief', 'violence', 'threat', 'danger', 'suspicious', 'illegal'],
            'fire': ['smoke', 'burning', 'hot', 'explosion', 'gas', 'chemical', 'hazard']
        }
        
        scores = {}
        for category, indicators in emergency_indicators.items():
            score = sum(1 for indicator in indicators if indicator in user_input.lower())
            scores[category] = score
        
        if max(scores.values()) > 0:
            emergency_type = max(scores, key=scores.get)
            # Default to medium priority for fallback cases
            priority = 'medium'
        else:
            # Ultimate fallback - assume medical with low priority
            emergency_type = 'medical'
            priority = 'low'
        
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

    def _extract_location(self, user_input: str, location_data: Dict[str, Any] = None) -> str:
        """Extract location from user input, prioritizing GPS data"""
        
        # If GPS location is available, use it
        if location_data:
            if location_data.get('address'):
                return location_data['address']
            elif location_data.get('lat') and location_data.get('lng'):
                lat, lng = location_data['lat'], location_data['lng']
                # Determine Pakistani city based on coordinates
                city = self._coordinates_to_city(lat, lng)
                return f"{city} (GPS: {lat:.4f}, {lng:.4f})"
        
        # Pakistani cities
        pakistani_cities = [
            'lahore', 'karachi', 'islamabad', 'rawalpindi', 'faisalabad',
            'multan', 'peshawar', 'quetta', 'sialkot', 'gujranwala'
        ]
        
        user_input_lower = user_input.lower()
        
        # Check for Pakistani cities in text
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

    def _coordinates_to_city(self, lat: float, lng: float) -> str:
        """Determine Pakistani city from GPS coordinates"""
        # Major Pakistani cities with approximate coordinates
        cities = {
            'Lahore': (31.5204, 74.3587),
            'Karachi': (24.8607, 67.0011),
            'Islamabad': (33.6844, 73.0479),
            'Rawalpindi': (33.5651, 73.0169),
            'Faisalabad': (31.4504, 73.1350),
            'Multan': (30.1575, 71.5249),
            'Peshawar': (34.0151, 71.5249),
            'Quetta': (30.1798, 66.9750),
            'Sialkot': (32.4945, 74.5229),
            'Gujranwala': (32.1877, 74.1945)
        }
        
        # Find closest city
        min_distance = float('inf')
        closest_city = 'Lahore'
        
        for city, (city_lat, city_lng) in cities.items():
            # Simple distance calculation
            distance = ((lat - city_lat) ** 2 + (lng - city_lng) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_city = city
        
        return closest_city

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