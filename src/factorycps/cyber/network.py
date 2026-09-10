from dataclasses import dataclass
from copy import deepcopy
import numpy as np
from .telemetry import TelemetryPacket

@dataclass
class NetworkConfig:
    loss_probability: float = 0.01
    latency_steps: int = 1
    jitter_steps: int = 1
    seed: int = 7

class NetworkChannel:
    def __init__(self, config: NetworkConfig | None = None):
        self.c = config or NetworkConfig()
        self.rng = np.random.default_rng(self.c.seed)
        self.q: list[tuple[int,TelemetryPacket]] = []
        self.step_idx = 0
    def send(self, packet: TelemetryPacket) -> bool:
        if self.rng.random() < self.c.loss_probability:
            return False
        jitter = int(self.rng.integers(0, self.c.jitter_steps+1)) if self.c.jitter_steps else 0
        self.q.append((self.step_idx + self.c.latency_steps + jitter, deepcopy(packet)))
        return True
    def receive(self) -> list[TelemetryPacket]:
        ready=[p for t,p in self.q if t <= self.step_idx]
        self.q=[(t,p) for t,p in self.q if t > self.step_idx]
        self.step_idx += 1
        return ready
