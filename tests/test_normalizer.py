"""Tests for DataNormalizer."""
import pytest
from predictkit.normalizer import DataNormalizer

SCHEMA = {"temperature": {"field": ["temp_C", "TEMP_CEL", "temperature"], "unit": "celsius"}}

def test_siemens_format():
    n = DataNormalizer(schema=SCHEMA)
    assert n.transform({"temp_C": 75.3})["temperature"] == pytest.approx(75.3)

def test_fanuc_format():
    n = DataNormalizer(schema=SCHEMA)
    assert n.transform({"TEMP_CEL": "75.3"})["temperature"] == pytest.approx(75.3)

def test_missing_field_returns_none():
    n = DataNormalizer(schema=SCHEMA)
    assert n.transform({"humidity": 60})["temperature"] is None

def test_fahrenheit_to_celsius():
    schema = {"temperature": {"field": "temp_F", "src_unit": "fahrenheit", "unit": "celsius"}}
    n = DataNormalizer(schema=schema)
    assert n.transform({"temp_F": 212.0})["temperature"] == pytest.approx(100.0, abs=0.01)
