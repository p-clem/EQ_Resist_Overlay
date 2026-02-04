#!/usr/bin/env python3
import sqlite3

db_path = "npc_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def lookup_npc(name):
    """Simplified lookup - normalize spaces to underscores"""
    name_normalized = name.strip().replace(' ', '_').lstrip('#')
    
    cursor.execute('''
        SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
    ''', (name_normalized.lower(),))
    
    result = cursor.fetchone()
    return result

# Test cases
test_cases = [
    "Eom Senshali Xakra",  # With spaces (EQ log output)
    "Eom_Senshali_Xakra",  # With underscores (manual entry)
    "eom senshali xakra",  # Lowercase with spaces
    "Eom Liako",           # Different NPC with spaces
]

print("Testing NPC lookups with unified logic:")
print("=" * 70)

for test_name in test_cases:
    result = lookup_npc(test_name)
    normalized = test_name.strip().replace(' ', '_').lstrip('#')
    
    if result:
        print(f"✓ '{test_name}'")
        print(f"  Normalized to: '{normalized}'")
        print(f"  Found: {result[0]} | MR:{result[1]} CR:{result[2]} DR:{result[3]} FR:{result[4]} PR:{result[5]}")
    else:
        print(f"✗ '{test_name}'")
        print(f"  Normalized to: '{normalized}' - NOT FOUND")
    print()

conn.close()
