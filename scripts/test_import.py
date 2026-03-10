import sys
sys.path.insert(0, '.')
import traceback
from agent_core.database import SessionLocal
from agent_core.scripts.import_data import import_aloc_file

db = SessionLocal()
try:
    print(import_aloc_file('data/aloc_raw/english_2000_aloc.json', db))
except Exception as e:
    print(traceback.format_exc())
