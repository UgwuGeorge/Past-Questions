"""
Migration: Add required_tier + price to exams; create subscriptions table.
Safe to run multiple times.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent_local_data.db")
print(f"Connecting to: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- 1. Add 'required_tier' column to exams if missing ---
cursor.execute("PRAGMA table_info(exams)")
existing_cols = {row[1] for row in cursor.fetchall()}
print(f"Existing exams columns: {existing_cols}")

if "required_tier" not in existing_cols:
    print("Adding 'required_tier' column to exams...")
    cursor.execute("ALTER TABLE exams ADD COLUMN required_tier VARCHAR DEFAULT 'FREE'")
    print("  [OK] required_tier added")
else:
    print("  [OK] required_tier already exists")

if "price" not in existing_cols:
    print("Adding 'price' column to exams...")
    cursor.execute("ALTER TABLE exams ADD COLUMN price FLOAT DEFAULT 0.0")
    print("  [OK] price added")
else:
    print("  [OK] price already exists")

# --- 2. Create subscriptions table if missing ---
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id),
        tier VARCHAR DEFAULT 'FREE',
        start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        expiry_date DATETIME,
        is_active BOOLEAN DEFAULT 1,
        transaction_id VARCHAR UNIQUE
    )
""")
print("  [OK] subscriptions table ready")

# --- 3. Set all existing exams to FREE tier (safe default) ---
cursor.execute("UPDATE exams SET required_tier = 'FREE' WHERE required_tier IS NULL")
updated = cursor.rowcount
print(f"  [OK] Set {updated} exams to FREE tier")

conn.commit()
conn.close()
print("\n[DONE] Migration complete! Restart the backend for changes to take effect.")
