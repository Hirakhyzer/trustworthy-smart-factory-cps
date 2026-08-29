from factorycps.simulation import SimulationConfig,run_simulation
from factorycps.cyber.attacks import AttackConfig
from factorycps.cyber.network import NetworkConfig

def test_normal_simulation_runs():
    r,s=run_simulation(SimulationConfig(steps=80,attack=AttackConfig(kind='none',start_step=999,end_step=1000),network=NetworkConfig(loss_probability=0,latency_steps=0,jitter_steps=0))); assert len(r)==80 and s['samples']==80

def test_obvious_temperature_attack_detected():
    _,s=run_simulation(SimulationConfig(steps=160,attack=AttackConfig(kind='temperature_bias',start_step=40,end_step=120,magnitude=10),network=NetworkConfig(loss_probability=0,latency_steps=0,jitter_steps=0))); assert s['recall'] > 0.8
