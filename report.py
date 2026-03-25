import sqlite3
import pprint

def generate_report():
    conn = sqlite3.connect('agent_local_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM questions')
    total_q = cursor.fetchone()[0]

    query = """
    SELECT e.category, e.name, COUNT(q.id) as q_count
    FROM exams e
    LEFT JOIN subjects s ON e.id = s.exam_id
    LEFT JOIN questions q ON s.id = q.subject_id
    GROUP BY e.id
    ORDER BY e.category, e.name
    """
    
    cursor.execute(query)
    results = cursor.fetchall()

    print(f"## Overall Status\n**Total Questions in Database**: {total_q}\n")
    print("| Category | Exam Name | Question Count |")
    print("|---|---|---|")
    for category, exam, count in results:
        print(f"| {category} | {exam} | {count} |")

    conn.close()

if __name__ == "__main__":
    generate_report()
