def health_band(health: float) -> str:
    if health >= 0.85: return 'healthy'
    if health >= 0.60: return 'degraded'
    if health >= 0.35: return 'maintenance_due'
    return 'critical'


def estimate_health(measured: dict, load: float) -> float:
    """Estimate machine health from observable condition signals.

    This is a reduced-order, model-derived baseline estimator. It inverts the
    v0.1 vibration/current/cycle-time relations and uses the median estimate so
    one corrupted channel does not directly determine the supervisor state.
    """
    load=max(0.0,min(1.5,float(load)))
    degradation_from_vibration=(float(measured['vibration'])-0.22-0.18*load)/1.55
    degradation_from_current=(float(measured['motor_current_a'])-7.5-3.2*load)/5.5
    degradation_from_cycle=(float(measured['cycle_time_s'])/12.0-1.0-0.08*load)/0.55
    estimates=[
        1.0-degradation_from_vibration,
        1.0-degradation_from_current,
        1.0-degradation_from_cycle,
    ]
    estimates=sorted(max(0.0,min(1.0,e)) for e in estimates)
    return estimates[1]
