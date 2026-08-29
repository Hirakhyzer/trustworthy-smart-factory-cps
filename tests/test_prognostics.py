from factorycps.maintenance.prognostics import cycles_to_threshold

def test_prognostics_positive():
    assert cycles_to_threshold(.9,.001,.6) > 0
