from __future__ import annotations
from dataclasses import dataclass, asdict
import numpy as np
from factorycps.physical.factory import FactorySnapshot

@dataclass
class SensorConfig:
    temp_std: float = 0.18
    vibration_std: float = 0.012
    current_std: float = 0.08
    cycle_std: float = 0.04
    quality_std: float = 0.008
    seed: int = 42

class SensorSuite:
    def __init__(self, config: SensorConfig | None = None):
        self.c = config or SensorConfig()
        self.rng = np.random.default_rng(self.c.seed)
    def read(self, snap: FactorySnapshot) -> dict:
        m = snap.machine
        return {
            'temperature_c': float(m.temperature_c + self.rng.normal(0,self.c.temp_std)),
            'vibration': float(m.vibration + self.rng.normal(0,self.c.vibration_std)),
            'motor_current_a': float(m.motor_current_a + self.rng.normal(0,self.c.current_std)),
            'cycle_time_s': float(m.cycle_time_s + self.rng.normal(0,self.c.cycle_std)),
            'quality_score': float(snap.inspection.score + self.rng.normal(0,self.c.quality_std)),
            'production_count': int(m.produced),
        }
