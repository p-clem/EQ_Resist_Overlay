#!/usr/bin/env python3
import os
import sys
import time
import re
from pathlib import Path

# Test if the log file is being read
log_file = Path("C:/EQ/Quarm EQ/eqlog_Jambedebois_pq.proj.txt")

if not log_file.exists():
    log_file = Path("C:\\EQ\\Quarm EQ\\eqlog_Jambedebois_pq.proj.txt")

print(f"Testing log file: {log_file}")
print(f"Exists: {log_file.exists()}")
print(f"Size: {log_file.stat().st_size if log_file.exists() else 'N/A'}")

if log_file.exists():
    # Show last 5 lines
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        print(f"\nLast 5 lines of log file:")
        for line in lines[-5:]:
            print(f"  {line.strip()}")
    
    # Test the regex
    consider_re = re.compile(
        r'^(?P<target>.*?)\s+(?P<faction>scowls|glar(?:es|es).*?|glowers|is|looks|judges?|kindly|regards).*?(?P<sep>-- )?(?P<diff>.*)?$',
        re.IGNORECASE
    )
    
    print(f"\nTesting consider regex:")
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines()[-5:]:
            clean_line = re.sub(r'^\[.*?\]\s+', '', line.strip())
            match = consider_re.match(clean_line)
            if match:
                print(f"  MATCHED: {clean_line}")
                print(f"    Target: {match.group('target')}")
            else:
                print(f"  No match: {clean_line[:60]}...")
