class FreshnessMonitor:
    def __init__(self):
        self.last_seq=None; self.last_time=None
    def score(self, seq: int, timestamp_s: float) -> float:
        stale=0.0
        if self.last_seq is not None and seq <= self.last_seq: stale=max(stale,1.0)
        if self.last_time is not None and timestamp_s <= self.last_time: stale=max(stale,1.0)
        self.last_seq=seq; self.last_time=timestamp_s
        return stale
