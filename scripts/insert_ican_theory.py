
import sqlite3, os

DB = 'past_questions_v2.db'

THEORY_DATA = {
    "Financial Accounting": [
        {"t": "Explain the concept of 'Going Concern' and its significance in the preparation of financial statements.", "tp": "Accounting Concepts"},
        {"t": "The following is a list of balances extracted from the books of Reharz Ventures as at 31 December 2023... Required: Prepare the Statement of Profit or Loss and Statement of Financial Position.", "tp": "Financial Statements Preparation"}
    ],
    "Taxation": [
        {"t": "Enumerate five (5) items of income that are specifically exempted from tax under the Personal Income Tax Act (PITA).", "tp": "Exempt Income"},
        {"t": "Calculate the Capital Gains Tax (CGT) payable by a company that disposed of a building for N50,000,000, which was originally purchased for N30,000,000. Professional fees for the sale were N2,000,000.", "tp": "CGT Computation"}
    ],
    "Business Law": [
        {"t": "Define a 'Contract' and explain the four essential elements required for a contract to be legally binding.", "tp": "Contract Law"},
        {"t": "Distinguish between a 'Private Company' and a 'Public Company' under the Companies and Allied Matters Act (CAMA) 2020.", "tp": "Company Law"}
    ]
}

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total = 0

    for subj_name, questions in THEORY_DATA.items():
        # Find subject ID
        c.execute("SELECT id FROM subjects WHERE name=?", (subj_name,))
        r = c.fetchone()
        if not r:
            print(f"Subject {subj_name} not found. Skipping.")
            continue
        sid = r[0]

        for q in questions:
            # Insert Theory question (No choices)
            c.execute("INSERT INTO questions (subject_id, text, difficulty, year, is_ai_generated, section, topic) VALUES (?,?,?,?,?,?,?)",
                      (sid, q["t"], "MEDIUM", 2024, False, "Section B: Theory", q["tp"]))
            total += 1
            print(f"  Inserted Theory Q for {subj_name}")

    conn.commit()
    conn.close()
    print(f"\n[DONE] {total} ICAN Theory questions inserted.")

if __name__ == "__main__":
    main()
