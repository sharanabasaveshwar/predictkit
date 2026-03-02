"""DataNormalizer — Unified sensor schema from any brand/format."""
from __future__ import annotations
import re
from typing import Any, Dict, Optional

class DataNormalizer:
    """Normalize multi-brand sensor data into a unified schema.

    Example::

        normalizer = DataNormalizer(schema={
            "temperature": {"field": ["temp_C", "TEMP_CEL", "temperature"], "unit": "celsius"},
        })
        normalized = normalizer.transform({"temp_C": 75.3})
        # → {"temperature": 75.3}
    """

    UNIT_CONVERSIONS = {
        ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
        ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
        ("psi", "bar"):             lambda v: v * 0.0689476,
        ("bar", "psi"):             lambda v: v * 14.5038,
    }

    def __init__(self, schema: Dict[str, Dict], config: Optional[str] = None):
        if config:
            import yaml
            with open(config) as f:
                schema = yaml.safe_load(f)
        self.schema = schema

    def _find_field(self, data: dict, field_spec) -> Optional[str]:
        candidates = field_spec if isinstance(field_spec, list) else [field_spec]
        for name in candidates:
            if name in data:
                return name
            for key in data:
                if re.fullmatch(name, key, re.IGNORECASE):
                    return key
        return None

    def _coerce(self, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                pass
        return value

    def _convert_unit(self, value: float, src: Optional[str], dst: Optional[str]) -> float:
        if not src or not dst or src == dst:
            return value
        key = (src.lower(), dst.lower())
        return self.UNIT_CONVERSIONS.get(key, lambda v: v)(value)

    def transform(self, data: dict) -> dict:
        result = {}
        for output_field, spec in self.schema.items():
            src_field = self._find_field(data, spec.get("field", output_field))
            if src_field is None:
                result[output_field] = spec.get("default", None)
                continue
            value = self._coerce(data[src_field])
            if isinstance(value, (int, float)):
                value = self._convert_unit(value, spec.get("src_unit"), spec.get("unit"))
            result[output_field] = value
        return result
