from factorycps.cyber.network import NetworkChannel,NetworkConfig
from factorycps.cyber.telemetry import TelemetryPacket

def test_zero_latency_delivery():
    n=NetworkChannel(NetworkConfig(loss_probability=0,latency_steps=0,jitter_steps=0)); n.send(TelemetryPacket(1,0,'x',{})); assert n.receive()[0].seq==1
