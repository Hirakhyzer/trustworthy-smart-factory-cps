from factorycps.diagnostics.fault_diagnosis import diagnose


def _trust(value=0.9):
    return {
        'temperature_c': value,
        'vibration': value,
        'motor_current_a': value,
        'cycle_time_s': value,
        'quality_score': value,
    }


def test_true_health_is_not_used_as_oracle():
    measured = {
        'temperature_c': 40.0,
        'vibration': 0.30,
        'motor_current_a': 8.0,
        'cycle_time_s': 12.0,
        'quality_score': 0.95,
    }
    predicted = dict(measured)
    residuals = {k: 0.0 for k in measured}
    assert diagnose(measured, predicted, residuals, 0.0, _trust(), true_health=0.1) == 'NORMAL'


def test_cross_sensor_pattern_can_indicate_equipment_degradation():
    measured = {
        'temperature_c': 54.0,
        'vibration': 0.82,
        'motor_current_a': 12.4,
        'cycle_time_s': 15.0,
        'quality_score': 0.90,
    }
    predicted = {
        'temperature_c': 48.0,
        'vibration': 0.50,
        'motor_current_a': 9.6,
        'cycle_time_s': 12.8,
        'quality_score': 0.92,
    }
    residuals = {
        'temperature_c': 1.0,
        'vibration': 2.0,
        'motor_current_a': 2.0,
        'cycle_time_s': 1.5,
        'quality_score': -0.3,
    }
    assert diagnose(measured, predicted, residuals, 0.0, _trust()) == 'EQUIPMENT_DEGRADATION'
