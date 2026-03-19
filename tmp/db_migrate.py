import sqlite3
conn = sqlite3.connect('agent_local_data.db')
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
    conn.commit()
    print("Column added successfully.")
except Exception as e:
    print(f"Failed: {e}")
conn.close()
