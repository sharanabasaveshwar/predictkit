"""EdgeCache — Offline-first local storage with intelligent cloud sync."""
from __future__ import annotations
import sqlite3, json, logging, threading, time
from typing import Optional

logger = logging.getLogger(__name__)

class EdgeCache:
    """Store sensor data locally and sync to cloud when internet is available.

    Example::

        cache = EdgeCache(
            storage="sqlite:///data/local_cache.db",
            sync_url="https://api.yourcompany.com/data",
            sync_interval=60,
        )
        cache.store({"machine_id": "M003", "temperature": 78, "timestamp": 1709164800})
    """

    def __init__(self, storage: str = "sqlite:///predictkit_cache.db",
                 sync_url: Optional[str] = None, sync_interval: int = 60,
                 batch_size: int = 100):
        self.db_path = storage.replace("sqlite:///", "")
        self.sync_url = sync_url
        self.sync_interval = sync_interval
        self.batch_size = batch_size
        self._init_db()
        if sync_url:
            threading.Thread(target=self._sync_loop, daemon=True).start()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    priority INTEGER DEFAULT 0,
                    synced INTEGER DEFAULT 0,
                    created_at REAL DEFAULT (strftime('%s','now'))
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_synced ON sensor_data(synced)")

    def store(self, record: dict, priority: int = 0) -> int:
        """Store a record locally. Always succeeds even when offline."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("INSERT INTO sensor_data (data, priority) VALUES (?, ?)",
                               (json.dumps(record), priority))
            return cur.lastrowid

    def _sync_loop(self):
        while True:
            time.sleep(self.sync_interval)
            try:
                self._sync()
            except Exception as exc:
                logger.warning("Sync failed: %s", exc)

    def _sync(self):
        try:
            import httpx
        except ImportError:
            raise ImportError("pip install predictkit[http]  —  httpx required for cloud sync")
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, data FROM sensor_data WHERE synced=0 ORDER BY priority DESC, id ASC LIMIT ?",
                (self.batch_size,)).fetchall()
        if not rows:
            return
        ids = [r[0] for r in rows]
        records = [json.loads(r[1]) for r in rows]
        resp = httpx.post(self.sync_url, json={"records": records}, timeout=10)
        resp.raise_for_status()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(f"UPDATE sensor_data SET synced=1 WHERE id IN ({','.join('?'*len(ids))})", ids)
        logger.info("Synced %d records", len(ids))
