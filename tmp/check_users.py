import sqlite3
conn = sqlite3.connect('agent_local_data.db')
cursor = conn.cursor()
cursor.execute("SELECT id, username, is_admin FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
