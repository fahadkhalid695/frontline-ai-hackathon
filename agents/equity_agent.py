"""
Equity Oversight Agent - Tracks service demand vs capacity and generates insights
"""
import logging
from datetime import datetime, timedelta
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

class EquityAgent:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.demand_tracking = defaultdict(list)
        self.capacity_data = {}
        self.insights_cache = {}
    
    def process(self, case_data, system_status):
        """Process equity oversight and generate insights"""
        logger.info("EquityAgent processing case for oversight")
        
        # Track demand
        self.track_demand(case_data)
        
        # Update capacity data
        self.update_capacity_data()
        
        # Generate insights
        insights = self.generate_insights()
        
        # Create administrative report
        admin_report = self.create_admin_report(insights)
        
        result = {
            'demand_analysis': self.analyze_demand_patterns(),
            'capacity_analysis': self.analyze_capacity_utilization(),
            'equity_insights': insights,
            'administrative_report': admin_report,
            'recommendations': self.generate_recommendations(insights),
            'agent': 'equity_agent',
            'timestamp': self.get_timestamp()
        }
        
        logger.info(f"Equity oversight result: {result}")
        return result
    
    def track_demand(self, case_data):
        """Track demand patterns by location, type, and priority"""
        location = case_data.get('location', 'unknown').lower()
        emergency_type = case_data.get('emergency_type', 'unknown')
        priority = case_data.get('priority', 'medium')
        timestamp = datetime.now()
        
        demand_entry = {
            'timestamp': timestamp.isoformat(),
            'location': location,
            'emergency_type': emergency_type,
            'priority': priority,
            'citizen_data': case_data.get('citizen_data', {})
        }
        
        # Track by location
        self.demand_tracking[f"{location}_{emergency_type}"].append(demand_entry)
        
        # Keep only last 24 hours of data for real-time analysis
        cutoff_time = timestamp - timedelta(hours=24)
        for key in self.demand_tracking:
            self.demand_tracking[key] = [
                entry for entry in self.demand_tracking[key]
                if datetime.fromisoformat(entry['timestamp']) > cutoff_time
            ]
    
    def update_capacity_data(self):
        """Update capacity data from available services"""
        hospitals = self.data_loader.query_data('hospitals')
        locations = self.data_loader.query_data('locations')
        
        for hospital in hospitals:
            location = hospital.get('location', '').lower()
            capacity_key = f"{location}_medical"
            
            self.capacity_data[capacity_key] = {
                'total_beds': hospital.get('beds_available', 0),
                'specialties': hospital.get('specialties', []),
                'emergency_capacity': hospital.get('emergency_capacity', 10),
                'current_utilization': self.estimate_utilization(hospital),
                'last_updated': datetime.now().isoformat()
            }
        
        # Add police and fire capacity estimates
        for location_data in locations:
            city = location_data.get('city', '').lower()
            emergency_services = location_data.get('emergency_services', 5)
            
            self.capacity_data[f"{city}_police"] = {
                'total_officers': emergency_services * 2,
                'patrol_units': emergency_services,
                'response_capacity': emergency_services * 3,
                'current_utilization': 0.6,  # Estimated 60% utilization
                'last_updated': datetime.now().isoformat()
            }
            
            self.capacity_data[f"{city}_fire"] = {
                'fire_stations': max(1, emergency_services // 5),
                'fire_trucks': emergency_services // 3,
                'response_capacity': emergency_services,
                'current_utilization': 0.3,  # Estimated 30% utilization
                'last_updated': datetime.now().isoformat()
            }
    
    def estimate_utilization(self, hospital):
        """Estimate current hospital utilization"""
        total_beds = hospital.get('beds_available', 0)
        if total_beds == 0:
            return 1.0  # Assume full if no data
        
        # Simple estimation based on bed availability
        # In real system, this would come from live hospital data
        if total_beds > 20:
            return 0.7  # Large hospitals ~70% utilization
        elif total_beds > 10:
            return 0.8  # Medium hospitals ~80% utilization
        else:
            return 0.9  # Small hospitals ~90% utilization
    
    def analyze_demand_patterns(self):
        """Analyze demand patterns across locations and services"""
        analysis = {
            'total_requests_24h': 0,
            'by_location': {},
            'by_emergency_type': defaultdict(int),
            'by_priority': defaultdict(int),
            'peak_hours': self.identify_peak_hours(),
            'demand_trends': self.calculate_demand_trends()
        }
        
        for key, requests in self.demand_tracking.items():
            location, emergency_type = key.split('_', 1)
            
            analysis['total_requests_24h'] += len(requests)
            analysis['by_emergency_type'][emergency_type] += len(requests)
            
            if location not in analysis['by_location']:
                analysis['by_location'][location] = {
                    'total_requests': 0,
                    'by_priority': defaultdict(int),
                    'response_needed': 0
                }
            
            analysis['by_location'][location]['total_requests'] += len(requests)
            
            for request in requests:
                priority = request.get('priority', 'medium')
                analysis['by_priority'][priority] += 1
                analysis['by_location'][location]['by_priority'][priority] += 1
                
                if priority == 'high':
                    analysis['by_location'][location]['response_needed'] += 1
        
        return analysis
    
    def analyze_capacity_utilization(self):
        """Analyze capacity utilization across services"""
        analysis = {
            'overall_utilization': 0,
            'by_location': {},
            'bottlenecks': [],
            'underutilized': [],
            'capacity_gaps': []
        }
        
        total_utilization = 0
        capacity_count = 0
        
        for key, capacity in self.capacity_data.items():
            location, service_type = key.split('_', 1)
            utilization = capacity.get('current_utilization', 0)
            
            total_utilization += utilization
            capacity_count += 1
            
            if location not in analysis['by_location']:
                analysis['by_location'][location] = {}
            
            analysis['by_location'][location][service_type] = {
                'utilization': utilization,
                'capacity_status': self.get_capacity_status(utilization),
                'details': capacity
            }
            
            # Identify bottlenecks and underutilized resources
            if utilization > 0.9:
                analysis['bottlenecks'].append({
                    'location': location,
                    'service': service_type,
                    'utilization': utilization
                })
            elif utilization < 0.4:
                analysis['underutilized'].append({
                    'location': location,
                    'service': service_type,
                    'utilization': utilization
                })
        
        analysis['overall_utilization'] = total_utilization / capacity_count if capacity_count > 0 else 0
        
        return analysis
    
    def generate_insights(self):
        """Generate equity and efficiency insights"""
        demand_analysis = self.analyze_demand_patterns()
        capacity_analysis = self.analyze_capacity_utilization()
        
        insights = {
            'equity_score': self.calculate_equity_score(demand_analysis, capacity_analysis),
            'efficiency_score': self.calculate_efficiency_score(capacity_analysis),
            'access_gaps': self.identify_access_gaps(demand_analysis, capacity_analysis),
            'resource_imbalances': self.identify_resource_imbalances(capacity_analysis),
            'service_quality_indicators': self.calculate_service_quality_indicators(),
            'demographic_analysis': self.analyze_demographic_patterns(demand_analysis)
        }
        
        return insights
    
    def calculate_equity_score(self, demand_analysis, capacity_analysis):
        """Calculate equity score (0-100) based on demand vs capacity balance"""
        location_scores = []
        
        for location in demand_analysis['by_location']:
            demand = demand_analysis['by_location'][location]['total_requests']
            
            # Get capacity for this location
            location_capacity = 0
            if location in capacity_analysis['by_location']:
                for service in capacity_analysis['by_location'][location]:
                    capacity_info = capacity_analysis['by_location'][location][service]['details']
                    if 'total_beds' in capacity_info:
                        location_capacity += capacity_info['total_beds']
                    elif 'response_capacity' in capacity_info:
                        location_capacity += capacity_info['response_capacity']
            
            # Calculate balance score (closer to 1.0 is better)
            if location_capacity > 0:
                balance_ratio = min(demand / location_capacity, location_capacity / max(demand, 1))
                location_scores.append(balance_ratio * 100)
            else:
                location_scores.append(0)
        
        return sum(location_scores) / len(location_scores) if location_scores else 50
    
    def calculate_efficiency_score(self, capacity_analysis):
        """Calculate efficiency score based on utilization rates"""
        utilizations = []
        
        for location_data in capacity_analysis['by_location'].values():
            for service_data in location_data.values():
                utilization = service_data['utilization']
                # Optimal utilization is around 70-80%
                if 0.7 <= utilization <= 0.8:
                    efficiency = 100
                elif utilization < 0.7:
                    efficiency = utilization / 0.7 * 100
                else:
                    efficiency = max(0, 100 - (utilization - 0.8) * 200)
                
                utilizations.append(efficiency)
        
        return sum(utilizations) / len(utilizations) if utilizations else 50
    
    def identify_access_gaps(self, demand_analysis, capacity_analysis):
        """Identify locations with poor access to services"""
        gaps = []
        
        for location, demand_data in demand_analysis['by_location'].items():
            high_priority_requests = demand_data['by_priority']['high']
            total_requests = demand_data['total_requests']
            
            # Check if location has adequate capacity
            has_medical = f"{location}_medical" in self.capacity_data
            has_police = f"{location}_police" in self.capacity_data
            has_fire = f"{location}_fire" in self.capacity_data
            
            gap_score = 0
            missing_services = []
            
            if not has_medical and demand_analysis['by_emergency_type']['medical'] > 0:
                gap_score += 3
                missing_services.append('medical')
            
            if not has_police and demand_analysis['by_emergency_type']['police'] > 0:
                gap_score += 2
                missing_services.append('police')
            
            if not has_fire and demand_analysis['by_emergency_type']['fire'] > 0:
                gap_score += 1
                missing_services.append('fire')
            
            if gap_score > 0 or high_priority_requests > total_requests * 0.3:
                gaps.append({
                    'location': location,
                    'gap_score': gap_score,
                    'missing_services': missing_services,
                    'high_priority_ratio': high_priority_requests / max(total_requests, 1),
                    'total_requests': total_requests
                })
        
        return sorted(gaps, key=lambda x: x['gap_score'], reverse=True)
    
    def identify_resource_imbalances(self, capacity_analysis):
        """Identify resource imbalances between locations"""
        imbalances = []
        
        # Group by service type
        service_types = set()
        for location_data in capacity_analysis['by_location'].values():
            service_types.update(location_data.keys())
        
        for service_type in service_types:
            utilizations = []
            locations = []
            
            for location, location_data in capacity_analysis['by_location'].items():
                if service_type in location_data:
                    utilizations.append(location_data[service_type]['utilization'])
                    locations.append(location)
            
            if len(utilizations) > 1:
                max_util = max(utilizations)
                min_util = min(utilizations)
                
                if max_util - min_util > 0.4:  # 40% difference indicates imbalance
                    max_location = locations[utilizations.index(max_util)]
                    min_location = locations[utilizations.index(min_util)]
                    
                    imbalances.append({
                        'service_type': service_type,
                        'imbalance_severity': max_util - min_util,
                        'overutilized_location': max_location,
                        'underutilized_location': min_location,
                        'max_utilization': max_util,
                        'min_utilization': min_util
                    })
        
        return sorted(imbalances, key=lambda x: x['imbalance_severity'], reverse=True)
    
    def calculate_service_quality_indicators(self):
        """Calculate service quality indicators"""
        return {
            'average_response_time': '15 minutes',  # Would be calculated from real data
            'citizen_satisfaction': 0.85,  # Would come from feedback data
            'case_resolution_rate': 0.92,  # Would come from follow-up data
            'system_uptime': 0.99,  # Would come from system monitoring
            'accessibility_score': 0.78  # Would be calculated from access patterns
        }
    
    def analyze_demographic_patterns(self, demand_analysis):
        """Analyze demographic patterns in service demand"""
        # This would analyze age, gender, socioeconomic factors in real implementation
        return {
            'age_distribution': {
                'under_18': 0.15,
                '18_65': 0.70,
                'over_65': 0.15
            },
            'vulnerability_indicators': {
                'elderly_high_priority': 0.25,
                'pediatric_cases': 0.12,
                'chronic_conditions': 0.30
            },
            'geographic_equity': {
                'urban_access': 0.85,
                'rural_access': 0.65,
                'remote_access': 0.45
            }
        }
    
    def generate_recommendations(self, insights):
        """Generate actionable recommendations for administrators"""
        recommendations = []
        
        # Equity-based recommendations
        if insights['equity_score'] < 70:
            recommendations.append({
                'priority': 'high',
                'category': 'equity',
                'title': 'Address Service Equity Gaps',
                'description': 'Significant disparities in service access detected across locations',
                'actions': [
                    'Redistribute resources to underserved areas',
                    'Establish mobile service units for remote locations',
                    'Implement telemedicine for basic consultations'
                ]
            })
        
        # Efficiency-based recommendations
        if insights['efficiency_score'] < 60:
            recommendations.append({
                'priority': 'medium',
                'category': 'efficiency',
                'title': 'Optimize Resource Utilization',
                'description': 'Suboptimal resource utilization detected',
                'actions': [
                    'Implement dynamic resource allocation',
                    'Cross-train staff for multiple service types',
                    'Establish inter-facility resource sharing protocols'
                ]
            })
        
        # Access gap recommendations
        if insights['access_gaps']:
            top_gap = insights['access_gaps'][0]
            recommendations.append({
                'priority': 'high',
                'category': 'access',
                'title': f'Address Critical Gap in {top_gap["location"].title()}',
                'description': f'Missing services: {", ".join(top_gap["missing_services"])}',
                'actions': [
                    f'Establish {top_gap["missing_services"][0]} services in {top_gap["location"]}',
                    'Partner with nearby facilities for service coverage',
                    'Implement emergency transport protocols'
                ]
            })
        
        return recommendations
    
    def create_admin_report(self, insights):
        """Create administrative report for decision makers"""
        return {
            'report_id': f"EQUITY_RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'executive_summary': {
                'overall_equity_score': insights['equity_score'],
                'overall_efficiency_score': insights['efficiency_score'],
                'critical_issues': len([r for r in self.generate_recommendations(insights) if r['priority'] == 'high']),
                'total_recommendations': len(self.generate_recommendations(insights))
            },
            'key_findings': [
                f"System equity score: {insights['equity_score']:.1f}/100",
                f"Resource efficiency: {insights['efficiency_score']:.1f}/100",
                f"Access gaps identified: {len(insights['access_gaps'])}",
                f"Resource imbalances: {len(insights['resource_imbalances'])}"
            ],
            'next_review_date': (datetime.now() + timedelta(days=7)).isoformat()
        }
    
    def identify_peak_hours(self):
        """Identify peak demand hours"""
        # Simplified implementation - would analyze actual timestamps in real system
        return {
            'morning_peak': '08:00-10:00',
            'afternoon_peak': '14:00-16:00',
            'evening_peak': '18:00-20:00'
        }
    
    def calculate_demand_trends(self):
        """Calculate demand trends"""
        # Simplified implementation - would analyze historical data
        return {
            'weekly_trend': 'increasing',
            'seasonal_pattern': 'stable',
            'growth_rate': 0.05  # 5% monthly growth
        }
    
    def get_capacity_status(self, utilization):
        """Get capacity status based on utilization"""
        if utilization > 0.9:
            return 'critical'
        elif utilization > 0.8:
            return 'high'
        elif utilization > 0.6:
            return 'optimal'
        elif utilization > 0.4:
            return 'moderate'
        else:
            return 'low'
    
    def get_timestamp(self):
        return datetime.now().isoformat()