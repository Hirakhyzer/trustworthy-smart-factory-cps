from dataclasses import dataclass
from factorycps.quality.predictor import predict_quality

@dataclass
class TwinState:
    health: float=1.0
    temperature_c: float=35.0
    vibration: float=0.22
    motor_current_a: float=7.5
    cycle_time_s: float=12.0
    quality_score: float=0.985

class FactoryDigitalTwin:
    def __init__(self, model_mismatch: float=0.0):
        self.state=TwinState(); self.mismatch=float(model_mismatch)
    def predict(self, load: float, wear_rate: float=0.00033) -> TwinState:
        s=self.state
        s.health=max(0.0,s.health-wear_rate*(0.6+load))
        d=1-s.health
        target=35.0+18.0*load+26.0*d
        s.temperature_c += 0.08*(target-s.temperature_c) + self.mismatch*0.02
        s.vibration=0.22+0.18*load+1.55*d + self.mismatch*0.002
        s.motor_current_a=7.5+3.2*load+5.5*d + self.mismatch*0.01
        s.cycle_time_s=12.0*(1+0.08*load+0.55*d)
        s.quality_score=predict_quality(s.temperature_c,s.vibration,s.health)
        return TwinState(**s.__dict__)
