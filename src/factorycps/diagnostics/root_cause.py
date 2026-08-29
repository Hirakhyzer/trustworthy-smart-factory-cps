def dominant_residual(residuals: dict[str,float]) -> str:
    return max(residuals, key=lambda k: abs(residuals[k])) if residuals else 'unknown'
