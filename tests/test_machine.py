from factorycps.physical.machine import Machine, MachineParams

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
