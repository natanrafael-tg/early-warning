import pickle
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import os

class RiskEngine:
    """ML model integration for risk assessment"""
    
    def __init__(self, model_path: str = "../models/dual_risk_models.pkl"):
        """Initialize risk engine with trained models"""
        self.models = self._load_models(model_path)
        self.feature_names = [
            'early_bet_count', 'early_avg_bet', 'early_std_bet', 
            'early_loss_rate', 'early_total_loss', 'early_unique_days',
            'early_bets_per_day', 'early_loss_gaps', 'early_immediate_rebet_pct',
            'early_sessions_session_count', 'early_sessions_avg_duration',
            'early_sessions_duration_cv', 'early_deposits_deposit_count',
            'early_deposits_avg_deposit'
        ]
    
    def _load_models(self, model_path: str) -> Dict:
        """Load trained models from pickle file"""
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        else:
            print(f"Warning: Model file not found at {model_path}, using mock models")
            return self._create_mock_models()
    
    def _create_mock_models(self) -> Dict:
        """Create mock models for demo purposes"""
        class MockModel:
            def predict_proba(self, X):
                np.random.seed(hash(str(X[0])) % 100)
                prob = np.random.beta(2, 2, 1)[0]
                return np.array([[1-prob, prob]])
        
        return {
            '7_day': {'model': MockModel(), 'threshold': 0.6},
            '30_day': {'model': MockModel(), 'threshold': 0.5}
        }
    
    def prepare_features(self, behavior_data: Dict) -> np.ndarray:
        """Convert behavior summary to model features"""
        features = {
            'early_bet_count': behavior_data['total_bets'],
            'early_avg_bet': behavior_data['avg_bet_amount'],
            'early_std_bet': behavior_data['avg_bet_amount'] * 0.5,
            'early_loss_rate': behavior_data['loss_rate'],
            'early_total_loss': behavior_data['total_loss_amount'],
            'early_unique_days': behavior_data['betting_days'],
            'early_bets_per_day': behavior_data['total_bets'] / max(behavior_data['betting_days'], 1),
            'early_loss_gaps': behavior_data['median_loss_gap_minutes'],
            'early_immediate_rebet_pct': 1 / (1 + behavior_data['median_loss_gap_minutes']/5),
            'early_sessions_session_count': behavior_data['betting_days'] * 2,
            'early_sessions_avg_duration': 45,
            'early_sessions_duration_cv': behavior_data['session_variance'],
            'early_deposits_deposit_count': behavior_data['total_deposits'],
            'early_deposits_avg_deposit': behavior_data['avg_deposit']
        }
        
        return np.array([[features.get(f, 0) for f in self.feature_names]])
    
    def predict_risk(self, behavior_data: Dict) -> Tuple[Dict[str, float], List[str]]:
        """Predict risk scores and identify risk factors"""
        features = self.prepare_features(behavior_data)
        
        # Get predictions from both models
        risk_scores = {}
        for window, model_info in self.models.items():
            model = model_info['model']
            prob = model.predict_proba(features)[0, 1]
            risk_scores[window] = float(prob)
        
        # Identify risk factors
        risk_factors = []
        if behavior_data['median_loss_gap_minutes'] < 5:
            risk_factors.append("Immediate loss chasing behavior")
        if behavior_data['total_deposits'] > 20:
            risk_factors.append("High deposit frequency")
        if behavior_data['late_night_percentage'] > 0.4:
            risk_factors.append("Excessive late-night gambling")
        if behavior_data['session_variance'] > 2:
            risk_factors.append("Erratic session patterns")
        if behavior_data['loss_rate'] > 0.8:
            risk_factors.append("Very high loss rate")
        
        return risk_scores, risk_factors
    
    def get_risk_level(self, risk_scores: Dict[str, float]) -> str:
        """Determine overall risk level from scores"""
        max_score = max(risk_scores.values())
        if max_score > 0.7:
            return "HIGH"
        elif max_score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_intervention_strategy(self, risk_7day: float, risk_30day: float) -> Dict:
        """Determine intervention based on dual risk scores"""
        
        if risk_7day > 0.7 and risk_30day > 0.7:
            return {
                "pattern": "IMMEDIATE_CRISIS",
                "urgency": "URGENT",
                "description": "Both short and long-term risk indicators show immediate danger",
                "actions": [
                    "Immediate deposit limit",
                    "Mandatory cooling period",
                    "Direct phone contact",
                    "Emergency resources"
                ]
            }
        
        elif risk_7day < 0.4 and risk_30day > 0.6:
            return {
                "pattern": "SLOW_BURN",
                "urgency": "PREVENTIVE", 
                "description": "Current behavior seems controlled but shows escalation trajectory",
                "actions": [
                    "Educational emails",
                    "Voluntary limit suggestions",
                    "Progress tracking tools",
                    "Scheduled check-ins"
                ]
            }
        
        elif 0.4 <= risk_7day <= 0.7 or 0.4 <= risk_30day <= 0.7:
            return {
                "pattern": "MODERATE_RISK",
                "urgency": "MONITOR",
                "description": "Showing concerning patterns that need monitoring",
                "actions": [
                    "In-app warnings",
                    "Session reminders", 
                    "Self-assessment tools"
                ]
            }
        
        else:
            return {
                "pattern": "CONTROLLED",
                "urgency": "STANDARD",
                "description": "Gambling behavior appears well-controlled",
                "actions": [
                    "Continue monitoring",
                    "Positive reinforcement"
                ]
            }