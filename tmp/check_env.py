import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.getcwd()), ".env") # This is if run from a subdir
# Actually let's just use what database.py uses
db_dir = os.path.dirname(os.path.abspath("agent_core/database.py"))
root_dir = os.path.dirname(db_dir)
env_file = os.path.join(root_dir, ".env")

print(f"DB Dir: {db_dir}")
print(f"Root Dir: {root_dir}")
print(f"Env File: {env_file}")
print(f"Env File Exists: {os.path.exists(env_file)}")

load_dotenv(env_file)
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL')}")
