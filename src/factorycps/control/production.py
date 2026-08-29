def effective_throughput(load_command: float, cycle_time_s: float) -> float:
    if cycle_time_s <= 0: return 0.0
    return max(0.0,load_command)*3600.0/cycle_time_s
