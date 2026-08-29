from dataclasses import dataclass
from .machine import Machine, MachineState
from .conveyor import Conveyor, ConveyorState
from .inspection import InspectionStation, InspectionResult

@dataclass
class FactorySnapshot:
    machine: MachineState
    conveyor: ConveyorState
    inspection: InspectionResult

class FactoryCell:
    def __init__(self):
        self.machine = Machine()
        self.conveyor = Conveyor()
        self.inspection = InspectionStation()
    def step(self, load: float = 1.0, maintenance: bool = False, jammed: bool = False) -> FactorySnapshot:
        ms = self.machine.step(load, maintenance)
        q = self.machine.expected_quality(ms)
        ins = self.inspection.inspect(q)
        cs = self.conveyor.step(arrivals=1, released=1 if ins.passed else 0, jammed=jammed)
        return FactorySnapshot(ms, cs, ins)
