from dataclasses import dataclass

@dataclass
class OperatorDecision:
    action: str
    accepted: bool

class OperatorModel:
    def review(self, recommendation: str, confidence: float) -> OperatorDecision:
        if confidence >= 0.85: return OperatorDecision(recommendation,True)
        if confidence >= 0.60: return OperatorDecision('REQUEST_INSPECTION',False)
        return OperatorDecision('CONTINUE_MONITORING',False)
