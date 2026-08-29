import argparse, json, csv
from pathlib import Path
import matplotlib.pyplot as plt
from factorycps.simulation import SimulationConfig, run_simulation
from factorycps.cyber.attacks import AttackConfig

p=argparse.ArgumentParser(); p.add_argument('--config',default='configs/baseline.json'); p.add_argument('--out',default='results/demo'); a=p.parse_args()
cfg=json.loads(Path(a.config).read_text())
attack=AttackConfig(**cfg.get('attack',{})); sim=SimulationConfig(**{k:v for k,v in cfg.items() if k!='attack'},attack=attack)
records,summary=run_simulation(sim); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2))
with (out/'timeseries.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=records[0].keys()); w.writeheader(); w.writerows(records)
plt.figure(figsize=(9,4)); plt.plot([r['time_s'] for r in records],[r['true_temperature_c'] for r in records],label='true'); plt.plot([r['time_s'] for r in records],[r['twin_temperature_c'] for r in records],label='twin'); plt.xlabel('time (s)'); plt.ylabel('temperature (C)'); plt.legend(); plt.tight_layout(); plt.savefig(out/'temperature_twin.png'); plt.close()
plt.figure(figsize=(9,4)); plt.plot([r['time_s'] for r in records],[r['anomaly_score'] for r in records],label='anomaly score'); plt.axhline(3.0,linestyle='--'); plt.xlabel('time (s)'); plt.ylabel('score'); plt.tight_layout(); plt.savefig(out/'security_response.png'); plt.close()
print(json.dumps(summary,indent=2))
