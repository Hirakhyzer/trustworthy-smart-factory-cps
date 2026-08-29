from dataclasses import dataclass

STATES=['NORMAL','WATCH','DIAGNOSE','ISOLATE_SENSOR','DEGRADED_PRODUCTION','MAINTENANCE_REQUIRED','QUALITY_HOLD','SAFE_STOP','RECOVERY']

@dataclass
class SupervisorDecision:
    state: str
    load_command: float
    hold_quality: bool
    maintenance: bool

class ResilientSupervisor:
    def decide(self, diagnosis: str, anomaly: bool, min_trust: float, health: float, quality: float) -> SupervisorDecision:
        if health < 0.35: return SupervisorDecision('SAFE_STOP',0.0,True,True)
        if health < 0.60: return SupervisorDecision('MAINTENANCE_REQUIRED',0.55,False,True)
        if quality < 0.78: return SupervisorDecision('QUALITY_HOLD',0.55,True,False)
        if diagnosis=='CYBERATTACK' and min_trust < 0.45: return SupervisorDecision('ISOLATE_SENSOR',0.65,False,False)
        if anomaly: return SupervisorDecision('DEGRADED_PRODUCTION',0.65,False,False)
        if diagnosis not in ('NORMAL','EQUIPMENT_DEGRADATION'): return SupervisorDecision('WATCH',0.8,False,False)
        return SupervisorDecision('NORMAL',1.0,False,False)
