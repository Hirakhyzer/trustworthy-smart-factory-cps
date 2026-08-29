def health_band(health: float) -> str:
    if health >= 0.85: return 'healthy'
    if health >= 0.60: return 'degraded'
    if health >= 0.35: return 'maintenance_due'
    return 'critical'
