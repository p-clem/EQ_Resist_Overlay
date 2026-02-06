#!/usr/bin/env python3
"""Simple DB lookup smoke test.

Run:
  python tests/test_lookup.py
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

test_name = "Eom_Senshali_Xakra"

cursor.execute(
    """
    SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
    """,
    (test_name.lower(),),
)

result = cursor.fetchone()

if result:
    print(f"Found: {result[0]}")
    print(f"MR: {result[1]}, CR: {result[2]}, DR: {result[3]}, FR: {result[4]}, PR: {result[5]}")
else:
    print(f"Not found with exact match: {test_name.lower()}")

    test_with_spaces = test_name.replace("_", " ")
    cursor.execute(
        """
        SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
        """,
        (test_with_spaces.lower(),),
    )
    result = cursor.fetchone()

    if result:
        print(f"Found with spaces: {result[0]}")
        print(f"MR: {result[1]}, CR: {result[2]}, DR: {result[3]}, FR: {result[4]}, PR: {result[5]}")
    else:
        print("Not found with spaces either")

conn.close()
