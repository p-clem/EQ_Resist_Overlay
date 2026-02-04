import sqlite3
import re

conn = sqlite3.connect('dist/npc_data.db')
cursor = conn.cursor()

# Test the lookup with the name from the log
test_name = "Eom_Senshali_Xakra"

# Try exact match (case-insensitive)
cursor.execute('''
    SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
''', (test_name.lower(),))

result = cursor.fetchone()

if result:
    print(f"Found: {result[0]}")
    print(f"MR: {result[1]}, CR: {result[2]}, DR: {result[3]}, FR: {result[4]}, PR: {result[5]}")
else:
    print(f"Not found with exact match: {test_name.lower()}")
    
    # Try with spaces instead of underscores
    test_with_spaces = test_name.replace('_', ' ')
    cursor.execute('''
        SELECT name, mr, cr, dr, fr, pr FROM npcs WHERE name_lower = ?
    ''', (test_with_spaces.lower(),))
    result = cursor.fetchone()
    
    if result:
        print(f"Found with spaces: {result[0]}")
        print(f"MR: {result[1]}, CR: {result[2]}, DR: {result[3]}, FR: {result[4]}, PR: {result[5]}")
    else:
        print(f"Not found with spaces either")

conn.close()
