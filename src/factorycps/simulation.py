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
    residual_keys=['temperature_c','vibration','motor_current_a','cycle_time_s','quality_score']
    for step in range(c.steps):
        snap=factory.step(load=load)
        measured=sensors.read(snap)
        pkt=TelemetryPacket(step,step*c.dt_s,'machine-1',measured)
        pkt=attack.apply(pkt,step); net.send(pkt); delivered=net.receive()
        delivered_packet_count=len(delivered)
        packet_received=delivered_packet_count > 0
        if delivered:
            last_values=delivered[-1]
        pred=twin.predict(load)
        if packet_received and last_values is not None:
            # Freshness is evaluated only for newly received telemetry. Re-feeding
            # the same held packet during a communication gap would falsely turn
            # loss/latency into replay evidence.
            fscore=freshness.score(last_values.seq,last_values.timestamp_s)
            pvals=pred.__dict__.copy(); pvals['production_count']=step+1
            det=detector.evaluate(last_values.values,pvals,fscore)
            trust=trust_engine.update(det.residuals,fscore)
            dg=diagnose(last_values.values,pvals,det.residuals,fscore,trust)
            values=last_values.values
        else:
            # No new telemetry is a communication condition, not a cyber replay
            # observation. Keep sensor residuals neutral, reduce network trust,
            # and let the supervisor enter WATCH via the explicit diagnosis.
            fscore=1.0
            det=Detection(score=0.0,anomaly=False,residuals={k:0.0 for k in residual_keys})
            trust=trust_engine.update(det.residuals,fscore)
            dg='NETWORK_FAULT'
            values=last_values.values if last_values is not None else measured
        health_estimate=estimate_health(values,load)
        dec=supervisor.decide(dg,det.anomaly,min(trust.values()),health_estimate,snap.inspection.score)
        load=dec.load_command
        active_attack=attack.active(step) and attack.c.kind!='none'
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
    labels=[r['attack_active'] for r in records]; preds=[r['anomaly'] for r in records]
    summary=production_metrics(records); summary.update(classification_metrics(labels,preds))
    delivered_packets=sum(r['delivered_packet_count'] for r in records)
    summary['packets_delivered']=delivered_packets
    summary['packet_delivery_fraction']=delivered_packets/len(records)
    summary['step_receive_fraction']=sum(r['packet_received'] for r in records)/len(records)
    summary['communication_fault_fraction']=sum(r['communication_fault'] for r in records)/len(records)
    summary['mean_telemetry_age_s']=sum(r['telemetry_age_s'] for r in records)/len(records)
    summary['final_estimated_health']=records[-1]['estimated_health']
    return records, summary
