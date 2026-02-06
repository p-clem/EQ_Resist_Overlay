#!/usr/bin/env python3
"""Quick log parsing sanity check (reads the last few lines).

Run:
  python tests/test_log_parsing.py
"""

from __future__ import annotations

import re
from pathlib import Path

try:
    from ._bootstrap import REPO_ROOT  # noqa: F401
except ImportError:
    from _bootstrap import REPO_ROOT  # type: ignore  # noqa: F401


log_file = Path("C:/EQ/Quarm EQ/eqlog_Jambedebois_pq.proj.txt")
if not log_file.exists():
    log_file = Path("C:\\EQ\\Quarm EQ\\eqlog_Jambedebois_pq.proj.txt")

print(f"Testing log file: {log_file}")
print(f"Exists: {log_file.exists()}")
print(f"Size: {log_file.stat().st_size if log_file.exists() else 'N/A'}")

if log_file.exists():
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        print("\nLast 5 lines of log file:")
        for line in lines[-5:]:
            print(f"  {line.strip()}")

    consider_re = re.compile(
        r"^(?P<target>.*?)\s+(?P<faction>scowls|glar(?:es|es).*?|glowers|is|looks|judges?|kindly|regards).*?(?P<sep>-- )?(?P<diff>.*)?$",
        re.IGNORECASE,
    )

    print("\nTesting consider regex:")
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f.readlines()[-5:]:
            clean_line = re.sub(r"^\[.*?\]\s+", "", line.strip())
            match = consider_re.match(clean_line)
            if match:
                print(f"  MATCHED: {clean_line}")
                print(f"    Target: {match.group('target')}")
            else:
                print(f"  No match: {clean_line[:60]}...")
