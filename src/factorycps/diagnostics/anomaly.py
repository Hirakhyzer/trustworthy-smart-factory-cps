from dataclasses import dataclass
from factorycps.twin.uncertainty import UncertaintyModel

@dataclass
class Detection:
    score: float
    anomaly: bool
    residuals: dict[str,float]

class PhysicsAnomalyDetector:
    def __init__(self, uncertainty: UncertaintyModel | None=None, threshold: float=3.0, persistence: int=2):
        self.u=uncertainty or UncertaintyModel(); self.threshold=threshold; self.persistence=persistence; self.count=0
    def evaluate(self, measured: dict, predicted: dict, freshness_score: float=0.0) -> Detection:
        residuals={}
        for k in ('temperature_c','vibration','motor_current_a','cycle_time_s','quality_score'):
            residuals[k]=(float(measured[k])-float(predicted[k]))/max(1e-9,float(getattr(self.u,k)))
        score=max([abs(v) for v in residuals.values()]+[4.0*freshness_score])
        self.count=self.count+1 if score >= self.threshold else 0
        return Detection(score=score, anomaly=self.count>=self.persistence, residuals=residuals)
