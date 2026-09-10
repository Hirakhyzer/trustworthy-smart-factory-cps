from __future__ import annotations
from dataclasses import dataclass
from factorycps.physical.factory import FactoryCell
from factorycps.sensing.sensors import SensorSuite, SensorConfig
from factorycps.cyber.telemetry import TelemetryPacket
from factorycps.cyber.network import NetworkChannel, NetworkConfig
from factorycps.cyber.attacks import AttackEngine, AttackConfig
from factorycps.cyber.freshness import FreshnessMonitor
from factorycps.twin.digital_twin import FactoryDigitalTwin
from factorycps.diagnostics.anomaly import PhysicsAnomalyDetector, Detection
from factorycps.diagnostics.trust import TrustEngine
from factorycps.diagnostics.fault_diagnosis import diagnose
from factorycps.maintenance.degradation import estimate_health
from factorycps.control.supervisor import ResilientSupervisor
from factorycps.metrics.evaluation import classification_metrics, production_metrics

@dataclass
class SimulationConfig:
    steps: int=400
    dt_s: float=1.0
    seed: int=42
    base_load: float=1.0
    accelerated_degradation: bool=False
    attack: AttackConfig | None=None
    network: NetworkConfig | None=None
    model_mismatch: float=0.0


def run_simulation(config: SimulationConfig | None=None):
    c=config or SimulationConfig(); factory=FactoryCell()
    if c.accelerated_degradation: factory.machine.p.wear_rate_per_cycle=0.0022
    sensors=SensorSuite(SensorConfig(seed=c.seed)); net=NetworkChannel(c.network or NetworkConfig(seed=c.seed+1)); attack=AttackEngine(c.attack or AttackConfig())
    freshness=FreshnessMonitor(); twin=FactoryDigitalTwin(c.model_mismatch); detector=PhysicsAnomalyDetector(); trust_engine=TrustEngine(); supervisor=ResilientSupervisor()
    records=[]; last_values=None; load=c.base_load
    detection_labels=[]; detection_preds=[]; attack_packets_dropped=0; prediction_history={}
    residual_keys=['temperature_c','vibration','motor_current_a','cycle_time_s','quality_score']
    for step in range(c.steps):
        snap=factory.step(load=load)
        measured=sensors.read(snap)
        active_attack=attack.active(step) and attack.c.kind!='none'
        pkt=TelemetryPacket(step,step*c.dt_s,'machine-1',measured,simulation_attack_label=active_attack)
        pkt=attack.apply(pkt,step)
        # Replay/freeze may replace the packet with an older clean snapshot. The
        # annotation is restored after manipulation and is never used by detection.
        pkt.simulation_attack_label=active_attack
        if not net.send(pkt) and active_attack:
            attack_packets_dropped += 1
        delivered=net.receive()
        delivered_packet_count=len(delivered)
        packet_received=delivered_packet_count > 0
        if delivered:
            last_values=max(delivered,key=lambda p:(p.timestamp_s,p.seq))
        pred=twin.predict(load)
        pvals=pred.__dict__.copy(); pvals['production_count']=step+1
        prediction_history[step*c.dt_s]=dict(pvals)
        if packet_received:
            step_det=Detection(score=0.0,anomaly=False,residuals={k:0.0 for k in residual_keys})
            step_dg='NORMAL'
            for received_packet in delivered:
                # Evaluate each delivered observation against the twin reference at
                # its own timestamp. This keeps benign latency from becoming a
                # physical residual and keeps attack labels aligned after jitter.
                fscore_i=freshness.score(received_packet.seq,received_packet.timestamp_s)
                expected=prediction_history.get(received_packet.timestamp_s,pvals)
                det_i=detector.evaluate(received_packet.values,expected,fscore_i)
                trust=trust_engine.update(det_i.residuals,fscore_i)
                dg_i=diagnose(received_packet.values,expected,det_i.residuals,fscore_i,trust)
                detection_labels.append(bool(received_packet.simulation_attack_label))
                detection_preds.append(bool(det_i.anomaly))
                if det_i.anomaly and not step_det.anomaly or det_i.score > step_det.score:
                    step_det=det_i; step_dg=dg_i
            det=step_det; dg=step_dg; values=last_values.values
        else:
            # No new telemetry is a communication condition, not a replay event.
            fscore=1.0
            det=Detection(score=0.0,anomaly=False,residuals={k:0.0 for k in residual_keys})
            trust=trust_engine.update(det.residuals,fscore)
            dg='NETWORK_FAULT'
            values=last_values.values if last_values is not None else measured
        health_estimate=estimate_health(values,load)
        dec=supervisor.decide(dg,det.anomaly,min(trust.values()),health_estimate,snap.inspection.score)
        load=dec.load_command
        telemetry_age_s=(step*c.dt_s-last_values.timestamp_s) if last_values is not None else step*c.dt_s
        records.append({
            'step':step,'time_s':step*c.dt_s,'packet_received':packet_received,'delivered_packet_count':delivered_packet_count,'communication_fault':not packet_received,'telemetry_age_s':float(max(0.0,telemetry_age_s)),'attack_active':active_attack,
            'true_health':snap.machine.health,'estimated_health':health_estimate,'true_temperature_c':snap.machine.temperature_c,'true_vibration':snap.machine.vibration,
            'true_current_a':snap.machine.motor_current_a,'true_cycle_time_s':snap.machine.cycle_time_s,'true_quality':snap.inspection.score,
            'measured_temperature_c':float(values['temperature_c']),'measured_vibration':float(values['vibration']),'measured_current_a':float(values['motor_current_a']),
            'measured_quality':float(values['quality_score']),'twin_temperature_c':pred.temperature_c,'twin_vibration':pred.vibration,'twin_current_a':pred.motor_current_a,
            'twin_quality':pred.quality_score,'anomaly_score':float(det.score),'anomaly':bool(det.anomaly),'diagnosis':dg,'min_trust':min(trust.values()),
            'supervisor_state':dec.state,'load_command':dec.load_command,
        })
    summary=production_metrics(records); summary.update(classification_metrics(detection_labels,detection_preds))
    delivered_packets=sum(r['delivered_packet_count'] for r in records)
    attack_generated=sum(r['attack_active'] for r in records); attack_observed=sum(detection_labels)
    summary['packets_delivered']=delivered_packets
    summary['packet_delivery_fraction']=delivered_packets/len(records)
    summary['step_receive_fraction']=sum(r['packet_received'] for r in records)/len(records)
    summary['communication_fault_fraction']=sum(r['communication_fault'] for r in records)/len(records)
    summary['mean_telemetry_age_s']=sum(r['telemetry_age_s'] for r in records)/len(records)
    summary['attack_packets_generated']=attack_generated
    summary['attack_packets_observed']=attack_observed
    summary['attack_packets_dropped']=attack_packets_dropped
    summary['attack_delivery_fraction']=attack_observed/attack_generated if attack_generated else 0.0
    summary['end_to_end_attack_recall']=summary['tp']/attack_generated if attack_generated else 0.0
    summary['final_estimated_health']=records[-1]['estimated_health']
    return records, summary
