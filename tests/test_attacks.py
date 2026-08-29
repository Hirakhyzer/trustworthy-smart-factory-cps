from factorycps.cyber.attacks import AttackEngine,AttackConfig
from factorycps.cyber.telemetry import TelemetryPacket

def test_temperature_bias():
    a=AttackEngine(AttackConfig(kind='temperature_bias',start_step=0,end_step=2,magnitude=5)); p=a.apply(TelemetryPacket(0,0,'m',{'temperature_c':30}),0); assert p.values['temperature_c']==35
