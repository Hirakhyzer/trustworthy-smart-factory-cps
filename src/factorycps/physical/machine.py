from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class MachineParams:
    ambient_c: float = 24.0
    base_temp_c: float = 35.0
    base_vibration: float = 0.22
    base_current_a: float = 7.5
    nominal_cycle_s: float = 12.0
    wear_rate_per_cycle: float = 0.00035
    cooling_rate: float = 0.08

@dataclass
class MachineState:
    health: float = 1.0
    temperature_c: float = 35.0
    vibration: float = 0.22
    motor_current_a: float = 7.5
    cycle_time_s: float = 12.0
    produced: int = 0

class Machine:
    def __init__(self, params: MachineParams | None = None):
        self.p = params or MachineParams()
        self.state = MachineState(temperature_c=self.p.base_temp_c,
                                  vibration=self.p.base_vibration,
                                  motor_current_a=self.p.base_current_a,
                                  cycle_time_s=self.p.nominal_cycle_s)

    def step(self, load: float = 1.0, maintenance: bool = False) -> MachineState:
        load = max(0.0, min(1.5, float(load)))
        s = self.state
        if maintenance:
            s.health = min(1.0, s.health + 0.08)
        else:
            s.health = max(0.0, s.health - self.p.wear_rate_per_cycle * (0.6 + load))
        degradation = 1.0 - s.health
        target_temp = self.p.base_temp_c + 18.0 * load + 26.0 * degradation
        s.temperature_c += self.p.cooling_rate * (target_temp - s.temperature_c)
        s.vibration = self.p.base_vibration + 0.18 * load + 1.55 * degradation
        s.motor_current_a = self.p.base_current_a + 3.2 * load + 5.5 * degradation
        s.cycle_time_s = self.p.nominal_cycle_s * (1.0 + 0.08 * load + 0.55 * degradation)
        s.produced += 1
        return MachineState(**s.__dict__)

    @staticmethod
    def expected_quality(state: MachineState) -> float:
        penalty = 0.55 * (1-state.health) + 0.018 * max(0, state.temperature_c-55) + 0.14 * max(0, state.vibration-0.6)
        return max(0.0, min(1.0, 0.985 - penalty))
