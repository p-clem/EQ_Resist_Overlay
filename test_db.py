import sqlite3

conn = sqlite3.connect('dist/npc_data.db')
cursor = conn.cursor()

# Search for Eom
cursor.execute("SELECT name FROM npcs WHERE name LIKE ? LIMIT 10", ('%Eom%',))
rows = cursor.fetchall()
print("NPCs with 'Eom' in name:")
for row in rows:
    print(f"  {row[0]}")

# Search specifically for underscores vs spaces
cursor.execute("SELECT name FROM npcs WHERE name LIKE ? LIMIT 5", ('%Eom_Senshali%',))
rows = cursor.fetchall()
print("\nNPCs with 'Eom_Senshali' (underscore):")
for row in rows:
    print(f"  {row[0]}")

cursor.execute("SELECT name FROM npcs WHERE name LIKE ? LIMIT 5", ('%Eom Senshali%',))
rows = cursor.fetchall()
print("\nNPCs with 'Eom Senshali' (space):")
for row in rows:
    print(f"  {row[0]}")

conn.close()
