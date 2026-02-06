#!/usr/bin/env python3
"""DB ad-hoc inspection (dev convenience).

Run:
  python tests/test_db.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

try:
    from ._bootstrap import REPO_ROOT
except ImportError:
    from _bootstrap import REPO_ROOT  # type: ignore


def _pick_db_path() -> Path:
    for p in (REPO_ROOT / "npc_data.db", REPO_ROOT / "dist" / "npc_data.db"):
        if p.exists():
            return p
    return REPO_ROOT / "npc_data.db"


db_path = _pick_db_path()
if not db_path.exists():
    print(f"DB not found: {db_path}")
    raise SystemExit(0)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Search for Eom
cursor.execute("SELECT name FROM npcs WHERE name LIKE ? LIMIT 10", ("%Eom%",))
rows = cursor.fetchall()
print("NPCs with 'Eom' in name:")
for row in rows:
    print(f"  {row[0]}")

# Search specifically for underscores vs spaces
cursor.execute("SELECT name FROM npcs WHERE name LIKE ? LIMIT 5", ("%Eom_Senshali%",))
rows = cursor.fetchall()
print("\nNPCs with 'Eom_Senshali' (underscore):")
for row in rows:
    print(f"  {row[0]}")

cursor.execute("SELECT name FROM npcs WHERE name LIKE ? LIMIT 5", ("%Eom Senshali%",))
rows = cursor.fetchall()
print("\nNPCs with 'Eom Senshali' (space):")
for row in rows:
    print(f"  {row[0]}")

conn.close()
