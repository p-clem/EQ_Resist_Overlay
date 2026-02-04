#!/usr/bin/env python3
import sqlite3
import os

sql_file = "npc_types.sql"
db_path = "npc_data.db"

if not os.path.exists(sql_file):
    print(f"SQL file not found: {sql_file}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS npcs (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL,
        name_lower TEXT UNIQUE NOT NULL,
        mr INTEGER DEFAULT 0,
        cr INTEGER DEFAULT 0,
        dr INTEGER DEFAULT 0,
        fr INTEGER DEFAULT 0,
        pr INTEGER DEFAULT 0
    )
''')
conn.commit()

print(f"Loading {sql_file} into {db_path}...")
count = 0

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        if line.startswith('(') and not line.startswith('PRIMARY'):
            try:
                # Parse CSV line
                line = line.strip()[1:-2]  # Remove ( and ),
                
                values = []
                in_quotes = False
                current = ''
                
                for i, char in enumerate(line):
                    if char == "'" and (i == 0 or line[i-1] != '\\'):
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        values.append(current.strip().strip("'"))
                        current = ''
                        continue
                    current += char
                
                if current:
                    values.append(current.strip().strip("'"))
                
                if len(values) >= 50 and values[1]:
                    name = values[1]
                    name_lower = name.lstrip('#').replace(' ', '_').lower()
                    mr = int(values[43]) if values[43] else 0
                    cr = int(values[44]) if values[44] else 0
                    dr = int(values[45]) if values[45] else 0
                    fr = int(values[46]) if values[46] else 0
                    pr = int(values[47]) if values[47] else 0
                    
                    try:
                        cursor.execute('''
                            INSERT INTO npcs (id, name, name_lower, mr, cr, dr, fr, pr)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (values[0], name, name_lower, mr, cr, dr, fr, pr))
                        count += 1
                    except sqlite3.IntegrityError:
                        pass
            except Exception as e:
                pass

conn.commit()
cursor.execute("SELECT COUNT(*) FROM npcs")
final_count = cursor.fetchone()[0]
print(f"Loaded {final_count} NPCs total")
conn.close()
