#!/usr/bin/env python3
"""Regression test: initialize zone from existing log tail.

When the overlay starts after EQ has already been running, there may be no new
"You have entered ..." line emitted. The watcher should backscan the recent
log tail to set the current zone before watching for new considers.

Run:
  python tests/test_zone_init_from_tail.py
"""

from __future__ import annotations

import os
import sqlite3
import tempfile
import threading
import time
from pathlib import Path

try:
    from ._bootstrap import REPO_ROOT  # type: ignore
except ImportError:
    from _bootstrap import REPO_ROOT  # type: ignore

import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from database import EQResistDatabase
from log_watcher import EQLogWatcher


class _FakeConfig:
    def __init__(self, p: Path):
        self._p = str(p)

    def get_eq_log_path(self):
        return self._p


def main() -> int:
    # The watcher runs in a daemon thread and holds an open SQLite connection.
    # On Windows, that can prevent immediate deletion of the temp DB file.
    # We tolerate cleanup failures for this regression test.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:
        # Use an on-disk DB so the watcher thread (which opens a new connection)
        # sees the same data.
        db_path = str(Path(td) / "test_npc_data.db")
        db = EQResistDatabase(db_path)
        cur = db.conn.cursor()

        # Minimal zone data
        cur.execute(
            "INSERT INTO zones (short_name, long_name, long_name_lower) VALUES (?, ?, ?)",
            ("karnor", "Karnor's Castle", "karnor's castle"),
        )

        # Two NPCs share name_lower but are in different zones.
        cur.execute(
            "INSERT INTO npcs (id, name, name_lower, level, maxlevel, hp, mana, mindmg, maxdmg, ac, mr, cr, dr, fr, pr, special_abilities) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (111, "a_skeleton", "a_skeleton", 10, 10, 500, 0, 5, 15, 50, 10, 10, 10, 10, 10, ""),
        )
        cur.execute(
            "INSERT INTO npcs (id, name, name_lower, level, maxlevel, hp, mana, mindmg, maxdmg, ac, mr, cr, dr, fr, pr, special_abilities) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (222, "a_skeleton", "a_skeleton", 55, 55, 50000, 0, 100, 200, 400, 200, 200, 200, 200, 200, ""),
        )
        cur.execute("INSERT INTO npc_zones (npc_id, zone_short_name) VALUES (?, ?)", (111, "wakening"))
        cur.execute("INSERT INTO npc_zones (npc_id, zone_short_name) VALUES (?, ?)", (222, "karnor"))
        db.conn.commit()

        # Create a temporary log that already contains a zone-enter line.
        log_path = Path(td) / "eqlog_test.txt"
        log_path.write_text(
            "[Sun Feb 08 12:00:00 2026] You have entered Karnor's Castle.\n"
            "[Sun Feb 08 12:00:05 2026] some other line\n",
            encoding="utf-8",
        )

        callback_calls: list[dict] = []

        def cb(payload: dict):
            callback_calls.append(payload)

        watcher = EQLogWatcher(db=db, callback=cb, config=_FakeConfig(log_path))

        # Run watcher in background; it should initialize zone from tail quickly.
        t = threading.Thread(target=watcher.watch, daemon=True)
        t.start()

        # Give it a moment to attach and scan.
        deadline = time.time() + 3.0
        while time.time() < deadline and watcher.current_zone_short is None:
            time.sleep(0.05)

        assert watcher.current_zone_long == "Karnor's Castle", watcher.current_zone_long
        assert watcher.current_zone_short == "karnor", watcher.current_zone_short

        # Ensure it will use that zone for lookups by appending a consider.
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(
                "[Sun Feb 08 12:00:10 2026] a skeleton scowls at you, ready to attack -- what would you like your tombstone to say?\n"
            )

        deadline = time.time() + 3.0
        while time.time() < deadline and not callback_calls:
            time.sleep(0.05)

        assert callback_calls, "Expected a DB callback from consider"
        got = callback_calls[-1]
        assert got.get("current_zone_short") == "karnor", got
        assert got.get("npc_id") == 222, got

    print("OK: watcher initializes zone from existing log tail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
