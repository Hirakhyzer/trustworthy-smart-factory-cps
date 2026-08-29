from factorycps.quality.predictor import predict_quality

def test_quality_falls_with_damage():
    assert predict_quality(70,1.0,.5) < predict_quality(40,.3,.95)
