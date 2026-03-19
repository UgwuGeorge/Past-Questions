import sqlite3
import sys

def promote_to_admin(username):
    conn = sqlite3.connect('past_questions_v2.db')
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"Error: User '{username}' not found.")
        conn.close()
        return

    cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (username,))
    conn.commit()
    print(f"Success: User '{username}' (ID: {user[0]}) has been promoted to Admin.")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python promote_admin.py <username>")
    else:
        promote_to_admin(sys.argv[1])
