# Baseline Findings

These results are from the deterministic synthetic v0.1 scenario suite and are not measurements from an operational factory. The current baseline was regenerated in GitHub Actions from commit `93dee37bab7edf7a86b2bdab9a933be2fd5993a3` after correcting communication-gap handling, packet-delivery accounting, timestamp-aligned twin comparison, and packet-aligned cyber ground truth.

## Corrected benchmark summary

| Scenario | Delivered-observation recall | Precision | End-to-end attack recall | Packet delivery | Main interpretation |
|---|---:|---:|---:|---:|---|
| Normal | n/a | n/a | n/a | 100% | No cyber alarms in ideal-network baseline |
| Temperature bias | 98.97% | 100% | 96.0% | 98.25% | Strongly detected; 3/100 attack packets lost by network |
| Vibration spoof | 98.97% | 100% | 96.0% | 98.25% | Strongly detected; same network realization as temperature case |
| Quality falsification | 0% | n/a | 0% | 98.25% | Major detector blind spot |
| Replay | 98.97% | 100% | 96.0% | 98.25% | Stale metadata remains strong evidence |
| Rewritten replay | 0% | n/a | 0% | 98.25% | Major stealthy temporal gap |
| Sensor freeze | 0% | n/a | 0% | 98.25% | Frozen values remain plausible after metadata rewriting in this baseline |
| Lossy network | n/a | n/a | n/a | 76.0% | No cyber false alarms; 59.5% of steps receive at least one packet |
| Accelerated degradation | n/a | n/a | n/a | 98.25% | Physical degradation generates many anomaly alarms; not a cyber-attack case |
| Attack during degradation | 100% | 33.1% | 99.17% | 98.25% | Attack detected, but physical degradation creates substantial root-cause ambiguity |

For attack scenarios, `delivered-observation recall` is computed only over attack-labeled telemetry packets actually delivered to the detector. `end-to-end attack recall` divides detected attack packets by all generated attack-window packets, so network loss remains visible instead of disappearing from the cyber score.

## Communication semantics correction

Earlier versions re-evaluated the same held telemetry packet whenever no new packet arrived. Repeated sequence/timestamp values therefore looked like replay evidence, which could turn ordinary latency or loss into false cyber alarms.

The simulator now treats **no newly delivered telemetry** as a communication condition (`NETWORK_FAULT`) rather than a replay observation. Freshness and cyber residuals are evaluated only when a new packet arrives. In the corrected lossy-network scenario, packet delivery is 76.0%, only 59.5% of simulation steps receive at least one packet, and the cyber detector produces zero false alarms.

The simulator reports separate communication quantities:

- `packet_delivery_fraction`: number of delivered packets divided by generated packets;
- `step_receive_fraction`: fraction of simulation steps with at least one newly delivered packet;
- `communication_fault_fraction`: fraction of steps with no newly delivered telemetry;
- `mean_telemetry_age_s`: age of the controller-facing held observation.

These quantities are intentionally different under delay and jitter because multiple queued packets may arrive in one step.

## Packet-aligned cyber evaluation correction

Previously, the attack label for the current simulation step was paired with whatever anomaly decision happened at that step, even when the detector was processing telemetry generated earlier and delivered later. That can shift TP/FN counts under latency and jitter.

Each synthetic telemetry packet now carries a **simulation-only ground-truth attack label** through the network queue. The detector and controller never consume that label. Every delivered packet is evaluated individually against the digital-twin reference associated with the packet timestamp, and the resulting alarm is scored against that packet's own ground truth.

This correction changes the interpretation of several baseline results. Temperature and vibration manipulation remain strong. Ordinary replay remains strong because stale metadata is explicit. By contrast, quality falsification, metadata-rewritten replay, and the current rewritten-metadata sensor-freeze scenario all produce 0% recall and should be treated as genuine v0.1 research gaps rather than hidden by step-level metric alignment.

## Physical degradation versus cyberattack

Accelerated equipment degradation produces a large number of anomaly alarms even though there is no cyberattack. Under a binary cyber-only confusion matrix those alarms appear as false positives, but scientifically they are **real physical anomalies**, not arbitrary detector mistakes. The benchmark therefore should not use the raw binary `fp` count alone to judge diagnosis quality in degradation scenarios.

When a cyberattack is introduced during degradation, delivered-observation recall reaches 100% but precision falls to about 33.1% because the physical fault already creates large residuals. This supports the central research problem: distinguish `CYBERATTACK`, `EQUIPMENT_DEGRADATION`, `SENSOR_FAULT`, `QUALITY_ANOMALY`, communication faults, and model mismatch rather than forcing every abnormal condition into a binary cyber label.

## v0.2 priorities

1. Temporal and trajectory-consistency evidence for metadata-rewritten replay and freeze.
2. Stronger quality-process invariants and causal evidence for quality-result falsification.
3. Latent health estimation that does not rely on simulation-only true health.
4. Multi-label cyber/fault diagnosis and mode-aware metrics instead of one binary cyber confusion matrix.
5. Detection delay, source-isolation accuracy, reconstruction error, service impact, and uncertainty-aware communication metrics.
