# Predictive Maintenance

Machine health is an abstract latent state in `[0,1]`. Degradation increases vibration, temperature, motor current and cycle time. `prognostics.py` provides a simple cycles-to-threshold baseline.

The runtime supervisor does **not** read simulator ground-truth health. It now uses a reduced-order health estimator derived from observable vibration, motor-current and cycle-time signals. The estimator inverts the v0.1 machine relations and uses the median of the three channel estimates so a single corrupted channel cannot directly determine the health signal.

This estimator is still an illustrative model-derived baseline, not a validated prognostic model. A major future problem is distinguishing real degradation from manipulated condition-monitoring telemetry and quantifying uncertainty in the latent-health estimate.
