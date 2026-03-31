
import os
import sqlite3
from sqlalchemy import create_engine, MetaData, Table, select, insert
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Path: scripts/migrate_to_postgres.py

def migrate():
    load_dotenv()
    
    # Sources
    SQLITE_DB = 'past_questions_v2.db'
    POSTGRES_URL = os.getenv("DATABASE_URL")
    
    if not POSTGRES_URL or 'postgresql' not in POSTGRES_URL:
        print("DATABASE_URL not set to a Postgres connection string. Skipping migration.")
        return

    print(f"Connecting to source: {SQLITE_DB}")
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    sqlite_conn.row_factory = sqlite3.Row
    sq = sqlite_conn.cursor()

    print(f"Connecting to destination: {POSTGRES_URL}")
    pg_engine = create_engine(POSTGRES_URL)
    pg_metadata = MetaData()
    pg_metadata.reflect(bind=pg_engine)
    
    # Table Order (To respect Foreign Keys)
    # 1. exams, 2. subjects, 3. question_papers, 4. question_contexts, 5. questions, 6. choices
    tables = ['exams', 'subjects', 'question_papers', 'question_contexts', 'questions', 'choices', 'users', 'subscriptions']
    
    for table_name in tables:
        if table_name not in pg_metadata.tables:
            print(f"Table {table_name} missing in Postgres. Ensure backend has run to create tables.")
            continue
            
        pg_table = pg_metadata.tables[table_name]
        
        # Clear existing data in Postgres (Optional)
        # with pg_engine.connect() as conn:
        #    conn.execute(pg_table.delete())
        #    conn.commit()

        # Fetch from SQLite
        sq.execute(f"SELECT * FROM {table_name}")
        rows = sq.fetchall()
        print(f"Migrating {len(rows)} rows for {table_name}...")
        
        if not rows: continue

        # Prepare for bulk insert
        data = [dict(row) for row in rows]
        
        # Handle Enum columns or specific types if needed
        # In this app, most are strings/ints
        
        with pg_engine.connect() as conn:
            try:
                # We use insert().values() for bulk
                conn.execute(insert(pg_table), data)
                conn.commit()
                print(f"  Successfully migrated {table_name}")
            except Exception as e:
                print(f"  Error migrating {table_name}: {e}")
                conn.rollback()

    sqlite_conn.close()
    print("\n[DONE] Database migration complete.")

if __name__ == "__main__":
    migrate()
