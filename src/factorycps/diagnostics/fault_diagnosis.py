def diagnose(measured: dict, predicted: dict, residuals: dict, freshness: float, trust: dict, true_health: float | None=None) -> str:
    if freshness >= 1.0: return 'CYBERATTACK'
    if min(trust.values()) < 0.55: return 'CYBERATTACK'
    if true_health is not None and true_health < 0.75:
        if measured['vibration'] > 0.65 and measured['motor_current_a'] > 11.0:
            return 'EQUIPMENT_DEGRADATION'
    if measured['quality_score'] < 0.82 and abs(residuals['quality_score']) < 2.5:
        return 'QUALITY_ANOMALY'
    max_r=max(abs(v) for v in residuals.values())
    if max_r >= 4.0: return 'SENSOR_FAULT'
    if max_r >= 2.5: return 'MODEL_MISMATCH'
    return 'NORMAL'
