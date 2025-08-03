# Sample user behaviors

DEMO_USERS = {
    # Pattern 1: immediate crisis (High 7-day, High 30-day)
    12345: {
        "behavior": {
            "total_bets": 287,
            "avg_bet_amount": 1543.25,
            "total_deposits": 23,
            "avg_deposit": 2500.00,
            "loss_rate": 0.82,
            "median_loss_gap_minutes": 2.3,
            "late_night_percentage": 0.45,
            "session_variance": 3.2,
            "total_loss_amount": 45230.50,
            "betting_days": 14
        },
        "risk_7day": 0.847,
        "risk_30day": 0.721
    },
    
    # Pattern 2: slow burn (Low 7-day, High 30-day)
    67890: {
        "behavior": {
            "total_bets": 45,
            "avg_bet_amount": 250.00,
            "total_deposits": 3,
            "avg_deposit": 500.00,
            "loss_rate": 0.55,
            "median_loss_gap_minutes": 180.0,
            "late_night_percentage": 0.10,
            "session_variance": 0.8,
            "total_loss_amount": 2500.00,
            "betting_days": 8
        },
        "risk_7day": 0.235,
        "risk_30day": 0.712
    },
    
    # Pattern 3: weekend warrior (Medium both)
    23456: {
        "behavior": {
            "total_bets": 95,
            "avg_bet_amount": 450.00,
            "total_deposits": 8,
            "avg_deposit": 1000.00,
            "loss_rate": 0.65,
            "median_loss_gap_minutes": 45.5,
            "late_night_percentage": 0.25,
            "session_variance": 1.8,
            "total_loss_amount": 8500.00,
            "betting_days": 10
        },
        "risk_7day": 0.432,
        "risk_30day": 0.389
    },
    
    # Pattern 4: controlled user (Low both)
    34567: {
        "behavior": {
            "total_bets": 28,
            "avg_bet_amount": 100.00,
            "total_deposits": 2,
            "avg_deposit": 500.00,
            "loss_rate": 0.54,
            "median_loss_gap_minutes": 480.0,
            "late_night_percentage": 0.10,
            "session_variance": 0.5,
            "total_loss_amount": 1200.00,
            "betting_days": 7
        },
        "risk_7day": 0.125,
        "risk_30day": 0.098
    }
}


def get_demo_user(user_id: int):
    return DEMO_USERS.get(user_id, None)