"""Tests for AnomalyDetector."""
import pytest
from predictkit.anomaly import AnomalyDetector

def test_zscore_normal_value():
    d = AnomalyDetector(model="zscore", threshold=80)
    d.fit([68, 70, 71, 72, 70, 71, 69, 72, 71, 70, 68, 73])
    assert d.predict(71.0) < 50

def test_zscore_anomalous_value():
    d = AnomalyDetector(model="zscore", threshold=80)
    d.fit([68, 70, 71, 72, 70, 71, 69, 72, 71, 70, 68, 73] * 8)
    assert d.predict(150.0) > 80

def test_pro_model_raises():
    with pytest.raises(ImportError, match="Pro"):
        AnomalyDetector(model="isolation_forest")

def test_neutral_before_fit():
    d = AnomalyDetector(model="zscore")
    assert d.predict(100.0) == 50.0
