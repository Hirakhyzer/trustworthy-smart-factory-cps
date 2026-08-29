from dataclasses import dataclass
from typing import Any

@dataclass
class TelemetryPacket:
    seq: int
    timestamp_s: float
    source: str
    values: dict[str, Any]
