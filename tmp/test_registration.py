import sys, os
sys.path.append(os.getcwd())
from agent_core.database import SessionLocal
from agent_core.models import main_models
from agent_core.core import auth
from datetime import datetime

def register_test_user():
    db = SessionLocal()
    try:
        username = "testuser_" + str(int(datetime.now().timestamp()))
        email = username + "@example.com"
        password = "testpassword123"
        
        new_user = main_models.User(
            username=username,
            email=email,
            hashed_password=auth.get_password_hash(password),
            is_admin=True # Make test user admin
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Success! Created user: {new_user.username} (ID: {new_user.id})")
    except Exception as e:
        print(f"Failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    register_test_user()
