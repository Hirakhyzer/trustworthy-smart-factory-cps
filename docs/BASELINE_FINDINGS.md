# Baseline Findings

The deterministic v0.1 benchmark is intentionally imperfect.

- Normal production with an ideal network produces no alarms in the baseline run.
- Temperature and vibration bias attacks are detected strongly.
- Ordinary replay is detected strongly because stale metadata and physical inconsistency reinforce one another.
- Metadata-rewritten replay and sensor freeze remain challenging as the model adapts and the frozen values may stay temporarily plausible.
- Quality-result falsification is a major blind spot for the residual-only baseline.
- Packet loss/delay can trigger false cyber alarms because stale telemetry resembles replay.
- Real accelerated equipment degradation produces many anomaly alarms, showing that the current detector does not reliably separate physical faults from cyber manipulation.
- A cyberattack during real degradation is detected, but root-cause attribution is poor because the physical fault itself already generates large residuals.

These limitations motivate mode-aware diagnosis, causal cross-sensor reasoning, uncertainty-aware state estimation, temporal statistics, and explicit multi-label cyber-plus-fault inference in later versions.
