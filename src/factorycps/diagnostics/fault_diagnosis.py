def diagnose(measured: dict, predicted: dict, residuals: dict, freshness: float, trust: dict, true_health: float | None=None) -> str:
    """Return an interpretable diagnosis using only observable/model-derived evidence.

    ``true_health`` is retained for backward API compatibility with v0.1 callers,
    but is intentionally not used: ground-truth physical health is unavailable in
    a real deployment and using it would leak simulator oracle information.
    """
    if freshness >= 1.0:
        return 'CYBERATTACK'
    if min(trust.values()) < 0.55:
        return 'CYBERATTACK'

    degradation_pattern = (
        measured['vibration'] > 0.65
        and measured['motor_current_a'] > 11.0
        and measured['cycle_time_s'] > predicted.get('cycle_time_s', measured['cycle_time_s'])
        and residuals.get('vibration', 0.0) > 0.0
        and residuals.get('motor_current_a', 0.0) > 0.0
    )
    if degradation_pattern:
        return 'EQUIPMENT_DEGRADATION'

    if measured['quality_score'] < 0.82 and abs(residuals['quality_score']) < 2.5:
        return 'QUALITY_ANOMALY'
    max_r=max(abs(v) for v in residuals.values())
    if max_r >= 4.0:
        return 'SENSOR_FAULT'
    if max_r >= 2.5:
        return 'MODEL_MISMATCH'
    return 'NORMAL'
