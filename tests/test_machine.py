from factorycps.physical.machine import Machine

def test_machine_health_degrades():
    m=Machine(); h=m.state.health
    for _ in range(10): m.step(1.0)
    assert m.state.health < h
