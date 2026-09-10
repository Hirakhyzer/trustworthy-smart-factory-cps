from factorycps.simulation import SimulationConfig,run_simulation
from factorycps.cyber.attacks import AttackConfig
from factorycps.cyber.network import NetworkConfig

def test_normal_simulation_runs():
    r,s=run_simulation(SimulationConfig(steps=80,attack=AttackConfig(kind='none',start_step=999,end_step=1000),network=NetworkConfig(loss_probability=0,latency_steps=0,jitter_steps=0))); assert len(r)==80 and s['samples']==80

def test_obvious_temperature_attack_detected():
    _,s=run_simulation(SimulationConfig(steps=160,attack=AttackConfig(kind='temperature_bias',start_step=40,end_step=120,magnitude=10),network=NetworkConfig(loss_probability=0,latency_steps=0,jitter_steps=0))); assert s['recall'] > 0.8

def test_network_delivery_metrics_have_explicit_semantics():
    records,summary=run_simulation(SimulationConfig(steps=40,attack=AttackConfig(kind='none',start_step=999,end_step=1000),network=NetworkConfig(loss_probability=0,latency_steps=1,jitter_steps=2,seed=9)))
    delivered=sum(r['delivered_packet_count'] for r in records)
    receive_steps=sum(r['packet_received'] for r in records)
    assert summary['packets_delivered'] == delivered
    assert summary['packet_delivery_fraction'] == delivered/len(records)
    assert summary['step_receive_fraction'] == receive_steps/len(records)
    assert summary['communication_fault_fraction'] == 1.0-summary['step_receive_fraction']

def test_total_packet_loss_is_not_mislabeled_as_cyber_replay():
    records,summary=run_simulation(SimulationConfig(steps=30,attack=AttackConfig(kind='none',start_step=999,end_step=1000),network=NetworkConfig(loss_probability=1.0,latency_steps=0,jitter_steps=0,seed=3)))
    assert summary['communication_fault_fraction'] == 1.0
    assert summary['fp'] == 0
    assert all(r['diagnosis'] == 'NETWORK_FAULT' for r in records)
    assert all(not r['anomaly'] for r in records)
