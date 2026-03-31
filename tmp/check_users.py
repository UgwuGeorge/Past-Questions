import sqlite3

def check_users():
    conn = sqlite3.connect('past_questions_v2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, is_admin FROM users')
    users = cursor.fetchall()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"ID: {u[0]}, Username: {u[1]}, Email: {u[2]}, IsAdmin: {u[3]}")
    conn.close()

if __name__ == "__main__":
    check_users()
