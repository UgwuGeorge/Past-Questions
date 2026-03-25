import sqlite3
import enum

class ExamCategory(enum.Enum):
    ACADEMICS = "ACADEMICS"
    PROFESSIONAL = "PROFESSIONAL"
    SCHOLARSHIPS = "SCHOLARSHIPS"
    Standardized = "Standardized"

class SubscriptionTier(enum.Enum):
    FREE = "FREE"
    PREMIUM = "PREMIUM"
    ELITE = "ELITE"

def update_tiers():
    conn = sqlite3.connect('agent_core/past_questions_v2.db')
    cursor = conn.cursor()
    
    # 1. Update Professional Exams to ELITE
    cursor.execute("UPDATE exams SET required_tier = ? WHERE category = ?", 
                  (SubscriptionTier.ELITE.value, ExamCategory.PROFESSIONAL.value))
    print(f"Updated Professional exams to ELITE")
    
    # 2. Update Standardized to PREMIUM
    cursor.execute("UPDATE exams SET required_tier = ? WHERE category = ?", 
                  (SubscriptionTier.PREMIUM.value, ExamCategory.Standardized.value))
    print(f"Updated Standardized exams to PREMIUM")
    
    # 3. Academics stay FREE for now
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_tiers()
