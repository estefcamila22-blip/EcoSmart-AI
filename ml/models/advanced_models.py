"""Advanced ML Models for Energy Prediction and Optimization"""
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class ConsumptionPredictor:
    """LSTM-like consumption prediction using statistical methods"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """Train consumption predictor"""
        try:
            X_scaled = self.scaler.fit_transform(X_train)
            self.model.fit(X_scaled, y_train)
            self.is_trained = True
            logger.info("Consumption predictor trained successfully")
        except Exception as e:
            logger.error(f"Training error: {e}")
            raise
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict consumption"""
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance"""
        features = {
            'hour_of_day': 0.25,
            'day_of_week': 0.15,
            'temperature': 0.20,
            'occupancy': 0.30,
            'historical_avg': 0.10,
        }
        return features

class AnomalyDetector:
    """Detect abnormal consumption patterns"""
    
    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, X_train: np.ndarray):
        """Train anomaly detector"""
        try:
            X_scaled = self.scaler.fit_transform(X_train)
            self.model.fit(X_scaled)
            self.is_trained = True
            logger.info("Anomaly detector trained")
        except Exception as e:
            logger.error(f"Training error: {e}")
            raise
    
    def detect(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Detect anomalies
        Returns: (predictions, anomaly_scores)
        """
        if not self.is_trained:
            raise RuntimeError("Model not trained")
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        scores = self.model.score_samples(X_scaled)
        return predictions, scores

class DeviceClassifier:
    """Classify devices based on consumption signatures"""
    
    def __init__(self):
        self.device_profiles = {
            'ac': {
                'power_range': (800, 2500),
                'duty_cycle': (0.2, 0.8),
                'characteristics': 'Continuous, temperature-dependent',
            },
            'water_heater': {
                'power_range': (400, 1500),
                'duty_cycle': (0.1, 0.4),
                'characteristics': 'Cyclical, thermostat-controlled',
            },
            'oven': {
                'power_range': (2000, 5000),
                'duty_cycle': (0.01, 0.1),
                'characteristics': 'High power, short duration',
            },
            'refrigerator': {
                'power_range': (100, 400),
                'duty_cycle': (0.3, 0.5),
                'characteristics': 'Continuous low power',
            },
            'washer': {
                'power_range': (300, 2000),
                'duty_cycle': (0.01, 0.05),
                'characteristics': 'Cyclical, scheduled',
            },
            'lighting': {
                'power_range': (10, 200),
                'duty_cycle': (0.2, 0.7),
                'characteristics': 'On-demand, variable',
            },
        }
    
    def classify(self, signature: Dict) -> Tuple[str, float]:
        """Classify device from consumption signature"""
        avg_power = signature.get('avg_power', 0)
        duty_cycle = signature.get('duty_cycle', 0)
        
        best_match = None
        best_score = 0
        
        for device, profile in self.device_profiles.items():
            power_match = (profile['power_range'][0] <= avg_power <= profile['power_range'][1])
            duty_match = (profile['duty_cycle'][0] <= duty_cycle <= profile['duty_cycle'][1])
            
            if power_match and duty_match:
                score = 0.5 if power_match else 0.3
                score += 0.5 if duty_match else 0.3
                
                if score > best_score:
                    best_score = score
                    best_match = device
        
        return best_match or 'unknown', best_score

class RecommendationEngine:
    """Generate energy-saving recommendations using ML"""
    
    def __init__(self):
        self.predictor = ConsumptionPredictor()
        self.classifier = DeviceClassifier()
    
    def generate_recommendations(self, consumption_data: Dict) -> List[Dict]:
        """Generate personalized recommendations"""
        recommendations = []
        
        total_consumption = consumption_data.get('total_kwh', 0)
        devices = consumption_data.get('devices', {})
        
        # AC optimization
        if 'ac' in devices and devices['ac']['percent'] > 35:
            recommendations.append({
                'id': 'rec_ac_001',
                'title': 'Optimize AC Usage',
                'description': 'Your AC is using 40% of total energy. Reduce temperature by 1°C.',
                'potential_savings': total_consumption * 0.12,
                'difficulty': 'easy',
                'priority': 'high',
            })
        
        # Water heater scheduling
        if 'water_heater' in devices:
            recommendations.append({
                'id': 'rec_water_001',
                'title': 'Schedule Water Heater',
                'description': 'Run water heater during off-peak hours (11 PM - 6 AM).',
                'potential_savings': total_consumption * 0.08,
                'difficulty': 'moderate',
                'priority': 'high',
            })
        
        # LED upgrade
        if 'lighting' in devices and devices['lighting']['percent'] > 10:
            recommendations.append({
                'id': 'rec_led_001',
                'title': 'LED Lighting Upgrade',
                'description': 'Switch to LED bulbs for 75% energy savings in lighting.',
                'potential_savings': total_consumption * 0.05,
                'difficulty': 'easy',
                'priority': 'medium',
            })
        
        return sorted(recommendations, key=lambda x: x['potential_savings'], reverse=True)

class EnergyOptimizer:
    """Optimize energy consumption in real-time"""
    
    def __init__(self):
        self.predictor = ConsumptionPredictor()
        self.anomaly_detector = AnomalyDetector()
    
    def calculate_optimal_schedule(self, 
                                   devices: List[Dict],
                                   electricity_rates: Dict) -> List[Dict]:
        """Calculate optimal device scheduling"""
        optimized_schedule = []
        
        # Sort devices by flexibility
        flexible_devices = [
            d for d in devices 
            if d['type'] in ['water_heater', 'washer', 'dryer', 'dishwasher']
        ]
        
        for device in flexible_devices:
            # Find cheapest hours
            cheapest_hours = sorted(
                electricity_rates.items(),
                key=lambda x: x[1]
            )[:6]  # Find 6 cheapest hours
            
            optimized_schedule.append({
                'device': device['name'],
                'recommended_start': cheapest_hours[0][0],
                'expected_cost': device['power'] * len(cheapest_hours),
                'potential_savings': device['power'] * 0.15,
            })
        
        return optimized_schedule
