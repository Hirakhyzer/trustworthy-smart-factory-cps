def cycles_to_threshold(health: float, wear_rate: float, threshold: float=0.6) -> float:
    if health <= threshold: return 0.0
    if wear_rate <= 0: return float('inf')
    return (health-threshold)/wear_rate
