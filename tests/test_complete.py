#!/usr/bin/env python3
"""Complete end-to-end smoke test of the overlay system.

Run:
  python tests/test_complete.py
  python -m tests.test_complete
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

try:
    from ._bootstrap import REPO_ROOT
except ImportError:
    from _bootstrap import REPO_ROOT  # type: ignore


def _pick_db_path() -> Path:
    candidates = [
        REPO_ROOT / "npc_data.db",
        REPO_ROOT / "dist" / "npc_data.db",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]


print("=" * 60)
print("QUARM NPC OVERLAY - COMPLETE SYSTEM TEST")
print("=" * 60)

# 1. Test database connection and NPC count
print("\n1. DATABASE TEST")
print("-" * 60)

db_path = _pick_db_path()
if not db_path.exists():
    print(f"   ✗ Database not found: {db_path}")
    raise SystemExit(0)

conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM npcs")
count = cursor.fetchone()[0]
print(f"   Database: {db_path}")
print(f"   NPCs loaded: {count}")

# 2. Test NPC lookups with different formats
print("\n2. NPC LOOKUP TEST")
print("-" * 60)

test_cases = [
    "Eom_Senshali_Xakra",
    "Eom Senshali Xakra",
    "eom_senshali_xakra",
    "Eom_Liako",
    "Eom Liako",
]


def lookup_npc(name: str):
    """Test the NPC lookup logic."""
    cursor.execute(
        """
        SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
        """,
        (name.lower(),),
    )
    result = cursor.fetchone()

    if not result:
        name_with_underscores = name.replace(" ", "_")
        cursor.execute(
            """
            SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
            """,
            (name_with_underscores.lower(),),
        )
        result = cursor.fetchone()

    return result


for test_name in test_cases:
    result = lookup_npc(test_name)
    if result:
        print(f"   ✓ {test_name}")
        print(
            f"     Found: {result[0]} | MR:{result[1]} CR:{result[2]} DR:{result[3]} FR:{result[4]} PR:{result[5]}"
        )
    else:
        print(f"   ✗ {test_name} - NOT FOUND")

# 3. Test log file existence (local dev convenience)
print("\n3. LOG FILE TEST")
print("-" * 60)
log_paths = [
    Path("C:/EQ/Quarm EQ/eqlog_Jambedebois_pq.proj.txt"),
    Path("C:\\EQ\\Quarm EQ\\eqlog_Jambedebois_pq.proj.txt"),
]

log_file = None
for path in log_paths:
    if path.exists():
        log_file = path
        print(f"   ✓ Log file found: {path}")
        print(f"     Size: {path.stat().st_size:,} bytes")
        print(f"     Last modified: {path.stat().st_mtime}")
        break

if not log_file:
    print("   ✗ Log file not found!")

# 4. Test regex parsing
print("\n4. REGEX PARSING TEST")
print("-" * 60)
consider_re = re.compile(
    r"^(?P<target>.*?)\s+(?P<faction>scowls|glar(?:es|es).*?|glowers|is|looks|judges?|kindly|regards).*?(?P<sep>-- )?(?P<diff>.*)?$",
    re.IGNORECASE,
)

test_lines = [
    "Eom Senshali Xakra scowls at you, ready to attack -- what would you like your tombstone to say?",
    "Eom_Senshali_Xakra scowls at you, ready to attack -- what would you like your tombstone to say?",
    "Eom Liako glares at you, ready to attack -- what would you like your tombstone to say?",
    "Eom Centien looks at you...",
]

for line in test_lines:
    match = consider_re.match(line)
    if match:
        npc_name = match.group("target").strip()
        print(f"   ✓ MATCHED: {npc_name}")
        result = lookup_npc(npc_name)
        if result:
            print(f"     Found in DB: {result[0]}")
        else:
            print("     WARNING: Not found in database!")
    else:
        print(f"   ✗ NO MATCH: {line[:50]}...")

# 5. Configuration test (packaged builds usually keep it in dist/)
print("\n5. CONFIGURATION TEST")
print("-" * 60)
config_candidates = [
    REPO_ROOT / "config.json",
    REPO_ROOT / "dist" / "config.json",
]
config_file = next((p for p in config_candidates if p.exists()), config_candidates[0])

if config_file.exists():
    with open(config_file, encoding="utf-8") as f:
        config = json.load(f)
    print(f"   ✓ Config file found: {config_file}")
    print(f"     EQ Log Path: {config.get('eq_log_path')}")
else:
    print(f"   ✗ Config file not found: {config_file}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

conn.close()
