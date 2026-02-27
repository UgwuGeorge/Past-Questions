import os
import sys

# Ensure 'server' package is discoverable
sys.path.append(os.getcwd())

try:
    from server.models import main_models
    print("Successfully imported server.models.main_models")
    
    from server.database import Base, engine
    print("Successfully imported Base and engine from server.database")
    
    # Check if models are registered with Base
    print(f"Tables in Base.metadata: {list(Base.metadata.tables.keys())}")
    
    print("Verification successful!")
except Exception as e:
    print(f"Verification failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
