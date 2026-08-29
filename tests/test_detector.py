from factorycps.diagnostics.anomaly import PhysicsAnomalyDetector

def test_large_residual_triggers_with_persistence():
    d=PhysicsAnomalyDetector(persistence=2); m={'temperature_c':50,'vibration':.2,'motor_current_a':8,'cycle_time_s':12,'quality_score':.98}; p={'temperature_c':35,'vibration':.2,'motor_current_a':8,'cycle_time_s':12,'quality_score':.98}; assert not d.evaluate(m,p).anomaly; assert d.evaluate(m,p).anomaly
