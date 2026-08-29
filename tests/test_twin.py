from factorycps.twin.digital_twin import FactoryDigitalTwin

def test_twin_finite():
    t=FactoryDigitalTwin(); s=t.predict(1.0); assert 0 <= s.health <= 1 and s.temperature_c > 0
