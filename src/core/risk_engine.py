def normalize_risk(risk_score: int) -> tuple[int, str]:
    risk_score = max(0, min(10, risk_score))

    if risk_score <= 3:
        level = "Low"
    elif risk_score <= 6:
        level = "Medium"
    else:
        level = "High"

    return risk_score, level
