from dataclasses import dataclass
from copy import deepcopy
from .telemetry import TelemetryPacket

@dataclass
class AttackConfig:
    kind: str = 'none'
    start_step: int = 120
    end_step: int = 220
    magnitude: float = 0.0
    rewrite_metadata: bool = False

class AttackEngine:
    def __init__(self, config: AttackConfig | None = None):
        self.c=config or AttackConfig()
        self.replay_packet: TelemetryPacket | None = None
    def active(self, step: int) -> bool:
        return self.c.start_step <= step < self.c.end_step
    def apply(self, packet: TelemetryPacket, step: int) -> TelemetryPacket:
        if not self.active(step) or self.c.kind=='none':
            if step < self.c.start_step:
                self.replay_packet = deepcopy(packet)
            return packet
        p=deepcopy(packet)
        k=self.c.kind
        if k=='temperature_bias': p.values['temperature_c'] += self.c.magnitude
        elif k=='vibration_spoof': p.values['vibration'] += self.c.magnitude
        elif k=='current_bias': p.values['motor_current_a'] += self.c.magnitude
        elif k=='quality_falsification': p.values['quality_score'] = max(0,min(1,p.values['quality_score']+self.c.magnitude))
        elif k=='production_count_bias': p.values['production_count'] += int(self.c.magnitude)
        elif k=='sensor_freeze':
            if self.replay_packet is not None:
                frozen=deepcopy(self.replay_packet)
                if self.c.rewrite_metadata:
                    frozen.seq=p.seq; frozen.timestamp_s=p.timestamp_s
                p=frozen
        elif k=='replay':
            if self.replay_packet is not None:
                p=deepcopy(self.replay_packet)
                if self.c.rewrite_metadata:
                    p.seq=packet.seq; p.timestamp_s=packet.timestamp_s
        return p
