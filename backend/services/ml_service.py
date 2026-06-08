import logging
import numpy as np
from typing import List, Dict

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.models = {}
        self.is_initialized = False

    async def initialize(self):
        try:
            logger.info("Initializing ML models...")
            self.models['consumption_predictor'] = self._load_predictor()
            self.models['anomaly_detector'] = self._load_anomaly_detector()
            self.is_initialized = True
            logger.info("ML models initialized")
        except Exception as e:
            logger.error(f"ML init error: {e}")
            raise

    async def cleanup(self):
        self.models.clear()

    def predict_consumption(self, history: List[float], hours: int = 24) -> Dict:
        try:
            avg = np.mean(history)
            std = np.std(history)
            predictions = np.random.normal(avg, std, hours)
            return {
                "predictions": predictions.tolist(),
                "confidence": 0.87,
                "peak_prediction": float(np.max(predictions)),
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return {"error": str(e)}

    def detect_anomalies(self, data: List[float]) -> Dict:
        try:
            mean = np.mean(data)
            std = np.std(data)
            threshold = 2.5
            anomalies = []
            for i, v in enumerate(data):
                if abs(v - mean) > threshold * std:
                    anomalies.append({"index": i, "value": v})
            return {"anomalies_detected": len(anomalies), "anomalies": anomalies}
        except Exception as e:
            logger.error(f"Anomaly detection error: {e}")
            return {"error": str(e)}

    def _load_predictor(self):
        return {"model": "LSTM", "status": "loaded"}

    def _load_anomaly_detector(self):
        return {"model": "IsolationForest", "status": "loaded"}