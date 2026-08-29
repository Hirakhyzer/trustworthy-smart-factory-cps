from dataclasses import dataclass

@dataclass
class InspectionResult:
    score: float
    passed: bool

class InspectionStation:
    def __init__(self, pass_threshold: float = 0.82):
        self.pass_threshold = pass_threshold
    def inspect(self, quality_score: float) -> InspectionResult:
        q = max(0.0, min(1.0, float(quality_score)))
        return InspectionResult(score=q, passed=q >= self.pass_threshold)
