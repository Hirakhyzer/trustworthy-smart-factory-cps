def predict_quality(temperature_c: float, vibration: float, health: float) -> float:
    penalty=0.50*(1-health)+0.016*max(0,temperature_c-55)+0.12*max(0,vibration-0.6)
    return max(0.0,min(1.0,0.985-penalty))
