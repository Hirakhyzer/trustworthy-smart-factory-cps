from dataclasses import dataclass

@dataclass
class UncertaintyModel:
    temperature_c: float=0.8
    vibration: float=0.05
    motor_current_a: float=0.35
    cycle_time_s: float=0.25
    quality_score: float=0.025
    production_count: float=2.0
