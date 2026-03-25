import sqlite3

def get_db_info():
    conn = sqlite3.connect('agent_local_data.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table_name, schema in tables:
        print(f"--- Table: {table_name} ---")
        print(schema)
        print("\n")
        
    conn.close()

if __name__ == "__main__":
    get_db_info()
