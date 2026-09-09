# Diagnostic Method

The v0.1 diagnostic stack combines uncertainty-normalized twin residuals, metadata freshness, source trust, and cross-signal rules. Labels include `NORMAL`, `SENSOR_FAULT`, `EQUIPMENT_DEGRADATION`, `QUALITY_ANOMALY`, `NETWORK_FAULT`, `CYBERATTACK`, and `MODEL_MISMATCH`.

Equipment-degradation diagnosis now uses observable/model-derived cross-sensor evidence (for example, elevated vibration and motor current together with cycle-time inconsistency). Simulator ground-truth health is not used by the active diagnosis path. The optional `true_health` argument remains only for backward API compatibility and is intentionally ignored.

The classifier is intentionally interpretable and should be treated as a research baseline rather than a validated diagnostic system.
