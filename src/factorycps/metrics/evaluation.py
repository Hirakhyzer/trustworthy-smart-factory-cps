def classification_metrics(labels, predictions):
    tp=sum(bool(a and b) for a,b in zip(labels,predictions)); fp=sum(bool((not a) and b) for a,b in zip(labels,predictions)); fn=sum(bool(a and (not b)) for a,b in zip(labels,predictions))
    precision=tp/(tp+fp) if tp+fp else 0.0; recall=tp/(tp+fn) if tp+fn else 0.0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    return {'precision':precision,'recall':recall,'f1':f1,'tp':tp,'fp':fp,'fn':fn}

def production_metrics(records):
    n=len(records)
    return {
        'samples': n,
        'mean_quality': sum(r['true_quality'] for r in records)/n,
        'final_health': records[-1]['true_health'],
        'anomaly_fraction': sum(r['anomaly'] for r in records)/n,
        'quality_hold_fraction': sum(r['supervisor_state']=='QUALITY_HOLD' for r in records)/n,
        'safe_stop_fraction': sum(r['supervisor_state']=='SAFE_STOP' for r in records)/n,
    }
