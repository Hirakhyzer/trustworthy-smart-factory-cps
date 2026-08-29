import json
from factorycps.simulation import SimulationConfig, run_simulation
from factorycps.cyber.attacks import AttackConfig
from factorycps.cyber.network import NetworkConfig

scenarios={
'normal': SimulationConfig(attack=AttackConfig(kind='none',start_step=999,end_step=1000),network=NetworkConfig(loss_probability=0.0,latency_steps=0,jitter_steps=0)),
'temperature_bias': SimulationConfig(attack=AttackConfig(kind='temperature_bias',magnitude=8.0)),
'vibration_spoof': SimulationConfig(attack=AttackConfig(kind='vibration_spoof',magnitude=0.42)),
'quality_falsification': SimulationConfig(attack=AttackConfig(kind='quality_falsification',magnitude=0.12)),
'replay': SimulationConfig(attack=AttackConfig(kind='replay')),
'rewritten_replay': SimulationConfig(attack=AttackConfig(kind='replay',rewrite_metadata=True)),
'sensor_freeze': SimulationConfig(attack=AttackConfig(kind='sensor_freeze',rewrite_metadata=True)),
'lossy_network': SimulationConfig(attack=AttackConfig(kind='none',start_step=999,end_step=1000),network=NetworkConfig(loss_probability=0.25,latency_steps=2,jitter_steps=2)),
'accelerated_degradation': SimulationConfig(accelerated_degradation=True,attack=AttackConfig(kind='none',start_step=999,end_step=1000)),
'attack_during_degradation': SimulationConfig(accelerated_degradation=True,attack=AttackConfig(kind='vibration_spoof',magnitude=-0.28,start_step=180,end_step=300)),
}
for name,cfg in scenarios.items():
    _,s=run_simulation(cfg); print(name); print(json.dumps(s,indent=2))
