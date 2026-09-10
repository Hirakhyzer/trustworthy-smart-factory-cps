from dataclasses import dataclass
from typing import Any

@dataclass
class TelemetryPacket:
    seq: int
    timestamp_s: float
    source: str
    values: dict[str, Any]
    # Simulation-only evaluation provenance. The detector and controller do not
    # consume this field; it keeps labels attached to the exact delayed packet.
    simulation_attack_label: bool = False
