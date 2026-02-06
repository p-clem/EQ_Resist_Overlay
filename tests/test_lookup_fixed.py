#!/usr/bin/env python3
"""Lookup test using the same normalization the overlay uses.

Run:
  python tests/test_lookup_fixed.py
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


def lookup_npc(name: str):
    name_normalized = name.strip().replace(" ", "_").lstrip("#")
    cursor.execute(
        """
        SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
        """,
        (name_normalized.lower(),),
    )
    return cursor.fetchone()


test_cases = [
    "Eom Senshali Xakra",
    "Eom_Senshali_Xakra",
    "eom senshali xakra",
    "Eom Liako",
]

print("Testing NPC lookups with unified logic:")
print("=" * 70)

for test_name in test_cases:
    result = lookup_npc(test_name)
    normalized = test_name.strip().replace(" ", "_").lstrip("#")

    if result:
        print(f"✓ '{test_name}'")
        print(f"  Normalized to: '{normalized}'")
        print(
            f"  Found: {result[0]} | MR:{result[1]} CR:{result[2]} DR:{result[3]} FR:{result[4]} PR:{result[5]}"
        )
    else:
        print(f"✗ '{test_name}'")
        print(f"  Normalized to: '{normalized}' - NOT FOUND")
    print()

conn.close()
