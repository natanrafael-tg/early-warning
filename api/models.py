from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class UserBehaviorSummary(BaseModel):
    """Summary of user's 14-day behavior"""
    total_bets: int = Field(..., description="Total number of bets in 14 days")
    avg_bet_amount: float = Field(..., description="Average bet amount in $")
    total_deposits: int = Field(..., description="Number of deposits made")
    avg_deposit: float = Field(..., description="Average deposit amount in $")
    loss_rate: float = Field(..., description="Percentage of bets lost", ge=0, le=1)
    median_loss_gap_minutes: float = Field(..., description="Median time between loss and next bet")
    late_night_percentage: float = Field(..., description="Percentage of late night gambling", ge=0, le=1)
    session_variance: float = Field(..., description="Coefficient of variation in session durations")
    total_loss_amount: float = Field(..., description="Total amount lost in $")
    betting_days: int = Field(..., description="Number of days with betting activity")

class RiskAssessmentRequest(BaseModel):
    """Request for risk assessment"""
    user_id: int = Field(..., description="TG Lab user ID", example=12345)
    assessment_date: Optional[datetime] = Field(
        default=None, 
        description="Date of assessment (defaults to now)"
    )

class RiskPrediction(BaseModel):
    """Individual risk prediction"""
    window_days: int = Field(..., description="Prediction window (7 or 30 days)")
    risk_score: float = Field(..., description="Risk probability 0-1", ge=0, le=1)
    confidence: float = Field(..., description="Model confidence", ge=0, le=1)
    predicted_behaviors: List[str] = Field(..., description="Likely escalation behaviors")

class InterventionStrategy(BaseModel):
    """Intervention strategy based on dual risk scores"""
    pattern: str = Field(..., description="Risk pattern: IMMEDIATE_CRISIS, SLOW_BURN, MODERATE_RISK, CONTROLLED")
    urgency: str = Field(..., description="Urgency level: URGENT, PREVENTIVE, MONITOR, STANDARD")
    description: str = Field(..., description="Explanation of the risk pattern")
    actions: List[str] = Field(..., description="Recommended intervention actions")

class RiskAssessmentResponse(BaseModel):
    """Complete risk assessment response"""
    user_id: int
    account_age_days: int = Field(..., description="Days since first bet")
    assessment_date: datetime
    behavior_summary: UserBehaviorSummary
    risk_predictions: Dict[str, RiskPrediction] = Field(..., description="7-day and 30-day predictions")
    overall_risk_level: RiskLevel
    risk_factors: List[str] = Field(..., description="Key risk factors identified")
    intervention_strategy: InterventionStrategy = Field(..., description="Dual-model intervention strategy")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class HealthCheckResponse(BaseModel):
    """API health check response"""
    status: str = "healthy"
    version: str = "1.0.0"
    models_loaded: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)