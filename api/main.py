from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from models import (
    RiskAssessmentRequest, RiskAssessmentResponse, 
    UserBehaviorSummary, RiskPrediction, InterventionStrategy,
    HealthCheckResponse, RiskLevel
)
from risk_engine import RiskEngine
from demo_data import get_demo_user

app = FastAPI(
    title="TG Lab Early Warning System",
    description="AI-powered early detection of problematic gambling behavior",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize risk engine
risk_engine = RiskEngine()

# Dependency to get risk engine
def get_risk_engine():
    return risk_engine

@app.get("/", tags=["General"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "TG Lab Early Warning System API",
        "documentation": "/docs",
        "health_check": "/health"
    }

@app.get("/health", response_model=HealthCheckResponse, tags=["General"])
async def health_check():
    """Check API health status"""
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        models_loaded=True,
        timestamp=datetime.now()
    )

@app.post("/api/v1/risk/assess", response_model=RiskAssessmentResponse, tags=["Risk Assessment"])
async def assess_user_risk(
    request: RiskAssessmentRequest,
    engine: RiskEngine = Depends(get_risk_engine)
):
    """
    Assess gambling risk for a user based on their first 14 days of behavior.
    
    This endpoint would typically be called automatically on day 14 of a new account,
    but can be triggered manually for demo purposes.
    """
    
    demo_data = get_demo_user(request.user_id)
    
    if demo_data:
        behavior_data = demo_data["behavior"]
        risk_scores = {
            "7_day": demo_data["risk_7day"],
            "30_day": demo_data["risk_30day"]
        }
        # Still calculate risk factors from behavior
        _, risk_factors = engine.predict_risk(behavior_data)
    else:
        # In production, this would fetch from database
        # For now, return error for non-demo users
        raise HTTPException(
            status_code=404,
            detail=f"User {request.user_id} not found. Try demo users: 12345 (high risk), 23456 (medium risk), 34567 (low risk)"
        )
    
    # Create behavior summary
    behavior_summary = UserBehaviorSummary(**behavior_data)
    
    # Determine risk level
    risk_level = engine.get_risk_level(risk_scores)
    
    # Get intervention strategy based on dual risk scores
    intervention_strategy = engine.get_intervention_strategy(
        risk_scores["7_day"], 
        risk_scores["30_day"]
    )
    
    # Create risk predictions
    risk_predictions = {
        "7_day": RiskPrediction(
            window_days=7,
            risk_score=round(risk_scores["7_day"], 3),
            confidence=0.85,  # Mock confidence
            predicted_behaviors=["Frequency increase likely"] if risk_scores["7_day"] > 0.5 else []
        ),
        "30_day": RiskPrediction(
            window_days=30,
            risk_score=round(risk_scores["30_day"], 3),
            confidence=0.75,  # Mock confidence
            predicted_behaviors=["Potential loss spiral"] if risk_scores["30_day"] > 0.6 else []
        )
    }
    
    return RiskAssessmentResponse(
        user_id=request.user_id,
        account_age_days=14,
        assessment_date=request.assessment_date or datetime.now(),
        behavior_summary=behavior_summary,
        risk_predictions=risk_predictions,
        overall_risk_level=RiskLevel(risk_level),
        risk_factors=risk_factors,
        intervention_strategy=InterventionStrategy(**intervention_strategy),
        metadata={
            "model_version": "1.0.0",
            "assessment_type": "new_user_14_day"
        }
    )


@app.get("/api/v1/risk/demo/overview", tags=["Demo"])
async def get_demo_overview():
    """
    Get all 4 demo patterns at once for presentation
    """
    engine = get_risk_engine()
    
    demo_patterns = {
        "immediate_crisis": await assess_user_risk(RiskAssessmentRequest(user_id=12345), engine),
        "slow_burn": await assess_user_risk(RiskAssessmentRequest(user_id=67890), engine), 
        "moderate_risk": await assess_user_risk(RiskAssessmentRequest(user_id=23456), engine),
        "controlled": await assess_user_risk(RiskAssessmentRequest(user_id=34567), engine)
    }
    
    return {
        "generated_at": datetime.now(),
        "patterns": demo_patterns,
    }

@app.get("/api/v1/risk/demo/{risk_level}", tags=["Demo"])
async def get_demo_example(risk_level: str):
    """
    Get a pre-calculated example for demo purposes.
    
    Risk levels: high, medium, low, slowburn
    """
    risk_level = risk_level.upper()
    
    demo_mapping = {
        "HIGH": 12345,
        "MEDIUM": 23456,
        "LOW": 34567,
        "SLOWBURN": 67890
    }
    
    if risk_level not in demo_mapping:
        raise HTTPException(
            status_code=400,
            detail="Risk level must be one of: high, medium, low, slowburn"
        )
    
    request = RiskAssessmentRequest(user_id=demo_mapping[risk_level])
    engine = get_risk_engine()
    return await assess_user_risk(request, engine)

@app.get("/api/v1/risk/batch-summary", tags=["Analytics"])
async def get_batch_summary():
    """
    Get summary statistics for batch risk assessment (mock data for demo).
    
    This would show daily monitoring results in production.
    """
    total_at_risk = 55300
    users_protected = 10701
    total_assessed = total_at_risk + users_protected
    
    risk_distribution_pct = {"LOW": 60, "MEDIUM": 25, "HIGH": 12, "CRITICAL": 3}
    risk_distribution = {
        level: int(total_assessed * (pct/100)) 
        for level, pct in risk_distribution_pct.items()
    }
    
    return {
        "assessment_date": datetime.now().date(),
        "total_users_assessed": total_assessed,
        "users_protected": users_protected,
        "users_at_risk": total_at_risk,
        "protection_rate": round((users_protected / total_assessed) * 100, 1),
        "risk_distribution": risk_distribution,
        "risk_distribution_percentages": risk_distribution_pct,
        "intervention_triggered": risk_distribution["HIGH"] + risk_distribution["CRITICAL"],
        "model_performance": {
            "7_day_accuracy": 72.7,
            "30_day_accuracy": 64.5,
            "target_accuracy": 70.0
        },
        "estimated_revenue_protected": 26751,
        "intervention_cost": 446,
        "roi_percentage": round(((26751 - 446) / 446) * 100, 1),
        "processing_time_seconds": 45.2
    }




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)