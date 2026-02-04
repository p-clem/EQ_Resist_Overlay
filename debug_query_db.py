import sqlite3

DB_PATH = "npc_data.db"

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    for q in ("%Vulak%", "%Aerr%", "%Herald%"):
        cur.execute("SELECT name, name_lower FROM npcs WHERE name LIKE ? LIMIT 10", (q,))
        rows = cur.fetchall()
        print(q, rows[:10])

    for key in ("the_herald_of_vulak`aerr", "the_herald_of_vulak'aerr"):
        cur.execute("SELECT name, name_lower FROM npcs WHERE name_lower = ?", (key,))
        print("exact", key, cur.fetchone())
