from factorycps.physical.machine import Machine, MachineParams
from factorycps.maintenance.degradation import estimate_health

def test_machine_health_degrades():
    m=Machine(); h=m.state.health
    for _ in range(10): m.step(1.0)
    assert m.state.health < h

def test_ambient_temperature_shifts_thermal_response():
    cool=Machine(MachineParams(ambient_c=20.0))
    hot=Machine(MachineParams(ambient_c=30.0))
    for _ in range(80):
        cool.step(0.0)
        hot.step(0.0)
    assert hot.state.temperature_c > cool.state.temperature_c + 5.0

def test_observable_health_estimator_matches_reduced_order_model():
    m=Machine()
    state=None
    for _ in range(120):
        state=m.step(1.0)
    measured={
        'vibration':state.vibration,
        'motor_current_a':state.motor_current_a,
        'cycle_time_s':state.cycle_time_s,
    }
    assert abs(estimate_health(measured,1.0)-state.health) < 1e-9

def test_health_estimator_is_robust_to_one_corrupted_channel():
    m=Machine(); state=m.step(1.0)
    measured={
        'vibration':99.0,
        'motor_current_a':state.motor_current_a,
        'cycle_time_s':state.cycle_time_s,
    }
    assert abs(estimate_health(measured,1.0)-state.health) < 1e-9
