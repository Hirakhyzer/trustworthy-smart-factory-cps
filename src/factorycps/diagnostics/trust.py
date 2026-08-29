class TrustEngine:
    def __init__(self): self.values={k:1.0 for k in ['temperature','vibration','current','quality','network']}
    def update(self, residuals: dict[str,float], freshness: float) -> dict[str,float]:
        mapping={'temperature':'temperature_c','vibration':'vibration','current':'motor_current_a','quality':'quality_score'}
        for src,key in mapping.items():
            evidence=min(1.0,abs(residuals.get(key,0.0))/5.0)
            self.values[src]=max(0.0,min(1.0,0.92*self.values[src]+0.08*(1-evidence)))
        self.values['network']=max(0.0,min(1.0,0.92*self.values['network']+0.08*(1-freshness)))
        return dict(self.values)
