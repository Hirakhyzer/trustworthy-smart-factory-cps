from dataclasses import dataclass

@dataclass
class ConveyorState:
    speed_m_s: float = 0.5
    queue: int = 0
    jammed: bool = False

class Conveyor:
    def __init__(self):
        self.state = ConveyorState()
    def step(self, arrivals: int = 1, released: int = 1, jammed: bool = False) -> ConveyorState:
        self.state.jammed = jammed
        self.state.queue = max(0, self.state.queue + arrivals - (0 if jammed else released))
        self.state.speed_m_s = 0.0 if jammed else max(0.2, 0.5 - 0.02*self.state.queue)
        return ConveyorState(**self.state.__dict__)
