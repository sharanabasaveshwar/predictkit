"""Tests for EdgeCache."""
import sqlite3, json
from predictkit.cache import EdgeCache

def test_store_and_retrieve(tmp_path):
    cache = EdgeCache(storage=f"sqlite:///{tmp_path}/test.db")
    rid = cache.store({"machine_id": "M001", "temperature": 72})
    assert isinstance(rid, int)
    with sqlite3.connect(f"{tmp_path}/test.db") as conn:
        row = conn.execute("SELECT data FROM sensor_data WHERE id=?", (rid,)).fetchone()
    assert json.loads(row[0])["temperature"] == 72

def test_store_multiple(tmp_path):
    cache = EdgeCache(storage=f"sqlite:///{tmp_path}/test2.db")
    ids = [cache.store({"val": i}) for i in range(10)]
    assert len(set(ids)) == 10
