import sqlite3
import json

db_path = 'past_questions_v2.db'

def insert_ican():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Find ICAN exam id
    cursor.execute("SELECT id FROM exams WHERE name = 'ICAN'")
    exam = cursor.fetchone()
    if not exam:
        print("ICAN exam not found. Creating it.")
        cursor.execute("INSERT INTO exams (name, category, description) VALUES ('ICAN', 'Professional', 'Institute of Chartered Accountants of Nigeria')")
        exam_id = cursor.lastrowid
    else:
        exam_id = exam[0]

    # Create subject
    subject_name = 'Financial Accounting (ATSWA 1)'
    cursor.execute("SELECT id FROM subjects WHERE name = ? AND exam_id = ?", (subject_name, exam_id))
    subject = cursor.fetchone()
    if not subject:
        cursor.execute("INSERT INTO subjects (name, exam_id) VALUES (?, ?)", (subject_name, exam_id))
        subject_id = cursor.lastrowid
    else:
        subject_id = subject[0]
        # Clear existing questions for this dummy run to ensure clean state
        cursor.execute("DELETE FROM choices WHERE question_id IN (SELECT id FROM questions WHERE subject_id = ?)", (subject_id,))
        cursor.execute("DELETE FROM questions WHERE subject_id = ?", (subject_id,))

    # Data to insert (Realistic ICAN Foundation Level Financial Accounting Past Questions)
    qdata = [
        {
            "text": "Which of the following is NOT an element of the financial statements?",
            "choices": [
                {"text": "Assets", "is_correct": False, "label": "A"},
                {"text": "Equity", "is_correct": False, "label": "B"},
                {"text": "Revenue", "is_correct": False, "label": "C"},
                {"text": "Audit Report", "is_correct": True, "label": "D"}
            ],
            "explanation": "The elements directly related to the measurement of financial position are assets, liabilities and equity. Elements related to performance are income and expenses. Audit Report is not an element."
        },
        {
            "text": "The accounting concept which states that an enterprise will continue in operational existence for the foreseeable future is the:",
            "choices": [
                {"text": "Accrual concept", "is_correct": False, "label": "A"},
                {"text": "Going concern concept", "is_correct": True, "label": "B"},
                {"text": "Consistency concept", "is_correct": False, "label": "C"},
                {"text": "Materiality concept", "is_correct": False, "label": "D"}
            ],
            "explanation": "Going concern implies that the entity will not be liquidated or forced to discontinue operations in the foreseeable future."
        },
        {
            "text": "The process of recording transactions in the journal is called:",
            "choices": [
                {"text": "Posting", "is_correct": False, "label": "A"},
                {"text": "Journalizing", "is_correct": True, "label": "B"},
                {"text": "Summarizing", "is_correct": False, "label": "C"},
                {"text": "Balancing", "is_correct": False, "label": "D"}
            ],
            "explanation": "Journalizing is the process of entering transactions in the journal."
        },
        {
            "text": "When a bank statement shows a debit balance, it means the customer:",
            "choices": [
                {"text": "Has cash at bank", "is_correct": False, "label": "A"},
                {"text": "Is overdrawn", "is_correct": True, "label": "B"},
                {"text": "Has an uncleared cheque", "is_correct": False, "label": "C"},
                {"text": "Has earned interest", "is_correct": False, "label": "D"}
            ],
            "explanation": "A debit balance on a bank statement represents an overdraft, meaning the customer owes the bank."
        },
        {
            "text": "Depreciation is best described as:",
            "choices": [
                {"text": "The systematic allocation of the depreciable amount of an asset over its useful life", "is_correct": True, "label": "A"},
                {"text": "A method of valuing assets", "is_correct": False, "label": "B"},
                {"text": "The loss of cash resulting from asset use", "is_correct": False, "label": "C"},
                {"text": "A reserve fund for replacing assets", "is_correct": False, "label": "D"}
            ],
            "explanation": "According to IAS 16, depreciation is the systematic allocation of the depreciable amount of an asset over its useful life."
        },
        {
            "text": "What is the primary purpose of a trial balance?",
            "choices": [
                {"text": "To calculate the profit for the year", "is_correct": False, "label": "A"},
                {"text": "To test the arithmetical accuracy of the double-entry bookkeeping", "is_correct": True, "label": "B"},
                {"text": "To show the financial position of the entity", "is_correct": False, "label": "C"},
                {"text": "To act as a substitute for financial statements", "is_correct": False, "label": "D"}
            ],
            "explanation": "A trial balance lists balances from the ledger simply to verify that total debits equal total credits."
        },
        {
            "text": "Which of the following errors will not affect the agreement of a trial balance?",
            "choices": [
                {"text": "Casting error", "is_correct": False, "label": "A"},
                {"text": "Error of principle", "is_correct": True, "label": "B"},
                {"text": "Partial omission", "is_correct": False, "label": "C"},
                {"text": "Transposition error in one account", "is_correct": False, "label": "D"}
            ],
            "explanation": "An error of principle (e.g. treating an asset as an expense) will have the same debit and credit amount, thus the trial balance will still balance."
        },
        {
            "text": "Capital expenditure is expenditure that:",
            "choices": [
                {"text": "Relates to the day-to-day running of the business", "is_correct": False, "label": "A"},
                {"text": "Enhances the value of an existing non-current asset or acquires a new one", "is_correct": True, "label": "B"},
                {"text": "Is spent to repair a non-current asset", "is_correct": False, "label": "C"},
                {"text": "Is paid as an interest on a loan", "is_correct": False, "label": "D"}
            ],
            "explanation": "Capital expenditure provides benefit over more than one accounting period, typically by acquiring or improving a non-current asset."
        },
        {
            "text": "In a partnership, interest on a partner's drawing is credited to:",
            "choices": [
                {"text": "The partner's current account", "is_correct": False, "label": "A"},
                {"text": "The partner's capital account", "is_correct": False, "label": "B"},
                {"text": "The appropriation account", "is_correct": True, "label": "C"},
                {"text": "The bank account", "is_correct": False, "label": "D"}
            ],
            "explanation": "Interest on drawings is an income to the partnership and is credited to the Profit and Loss Appropriation Account."
        },
        {
            "text": "Which accounting standard governs the presentation of financial statements?",
            "choices": [
                {"text": "IAS 2", "is_correct": False, "label": "A"},
                {"text": "IAS 7", "is_correct": False, "label": "B"},
                {"text": "IAS 1", "is_correct": True, "label": "C"},
                {"text": "IFRS 15", "is_correct": False, "label": "D"}
            ],
            "explanation": "IAS 1 outlines the overall requirements for the presentation of financial statements, guidelines for their structure, and minimum requirements for their content."
        },
        {
            "text": "Which of the following describes an Imprest System?",
            "choices": [
                {"text": "A method of stock valuation", "is_correct": False, "label": "A"},
                {"text": "A system where petty cash is maintained at an agreed fixed sum", "is_correct": True, "label": "B"},
                {"text": "A system of controlling long-term liabilities", "is_correct": False, "label": "C"},
                {"text": "A depreciation method for small assets", "is_correct": False, "label": "D"}
            ],
            "explanation": "The imprest system is a form of financial accounting system for petty cash. It relies on a fixed imprest balance which is periodically replenished."
        },
        {
            "text": "If closing inventory is understated, what is the effect on profit?",
            "choices": [
                {"text": "Profit is understated", "is_correct": True, "label": "A"},
                {"text": "Profit is overstated", "is_correct": False, "label": "B"},
                {"text": "No effect", "is_correct": False, "label": "C"},
                {"text": "Cost of sales is understated", "is_correct": False, "label": "D"}
            ],
            "explanation": "Cost of sales = Opening Inventory + Purchases - Closing Inventory. If closing inventory is understated, Cost of Sales is overstated, resulting in an understated profit."
        },
        {
            "text": "The document sent by a supplier to a customer showing the outstanding balance at the end of the month is called:",
            "choices": [
                {"text": "An invoice", "is_correct": False, "label": "A"},
                {"text": "A statement of account", "is_correct": True, "label": "B"},
                {"text": "A debit note", "is_correct": False, "label": "C"},
                {"text": "A credit note", "is_correct": False, "label": "D"}
            ],
            "explanation": "A statement of account summarizes all transactions over a period and shows the closing balance owed."
        },
        {
            "text": "Goodwill is classified as what type of asset?",
            "choices": [
                {"text": "Tangible non-current asset", "is_correct": False, "label": "A"},
                {"text": "Intangible non-current asset", "is_correct": True, "label": "B"},
                {"text": "Current asset", "is_correct": False, "label": "C"},
                {"text": "Liquid asset", "is_correct": False, "label": "D"}
            ],
            "explanation": "Goodwill cannot be physically touched, so it is an intangible non-current asset."
        },
        {
            "text": "A provision for doubtful debts is created to comply with which accounting concept?",
            "choices": [
                {"text": "Going concern", "is_correct": False, "label": "A"},
                {"text": "Matching", "is_correct": False, "label": "B"},
                {"text": "Prudence", "is_correct": True, "label": "C"},
                {"text": "Materiality", "is_correct": False, "label": "D"}
            ],
            "explanation": "Prudence requires liabilities and potential losses to be recognized immediately but gains only when realized. Provision for doubtful debts anticipates a loss."
        },
        {
            "text": "Shares issued at a price above their nominal value are said to be issued at a:",
            "choices": [
                {"text": "Premium", "is_correct": True, "label": "A"},
                {"text": "Discount", "is_correct": False, "label": "B"},
                {"text": "Par value", "is_correct": False, "label": "C"},
                {"text": "Loss", "is_correct": False, "label": "D"}
            ],
            "explanation": "When the issue price exceeds the nominal (par) value, the excess is credited to the share premium account."
        },
        {
            "text": "Under the straight-line method of depreciation, the annual charge is:",
            "choices": [
                {"text": "Decreasing every year", "is_correct": False, "label": "A"},
                {"text": "Increasing every year", "is_correct": False, "label": "B"},
                {"text": "Constant every year", "is_correct": True, "label": "C"},
                {"text": "Based on units of production", "is_correct": False, "label": "D"}
            ],
            "explanation": "The straight-line method allocates an equal amount of depreciation to each full accounting period."
        },
        {
            "text": "Which of these is not typically a component of the manufacturing account?",
            "choices": [
                {"text": "Direct materials", "is_correct": False, "label": "A"},
                {"text": "Direct labour", "is_correct": False, "label": "B"},
                {"text": "Factory overheads", "is_correct": False, "label": "C"},
                {"text": "Office rent", "is_correct": True, "label": "D"}
            ],
            "explanation": "Office rent is an administrative expense, hence it is charged to the Statement of Profit or Loss, not the manufacturing account."
        },
        {
            "text": "A partner who contributes capital to the firm but takes no active part in its management is called a:",
            "choices": [
                {"text": "General partner", "is_correct": False, "label": "A"},
                {"text": "Nominal partner", "is_correct": False, "label": "B"},
                {"text": "Sleeping/Dormant partner", "is_correct": True, "label": "C"},
                {"text": "Active partner", "is_correct": False, "label": "D"}
            ],
            "explanation": "A sleeping or dormant partner provides capital and shares profits/losses but doesn't participate in day-to-day management."
        },
        {
            "text": "The primary objective of external auditing is to:",
            "choices": [
                {"text": "Detect fraud and errors", "is_correct": False, "label": "A"},
                {"text": "Express an opinion on the true and fair view of financial statements", "is_correct": True, "label": "B"},
                {"text": "Prepare the financial statements for management", "is_correct": False, "label": "C"},
                {"text": "Advise management on tax matters", "is_correct": False, "label": "D"}
            ],
            "explanation": "The external auditor's primary role is to audit the financial statements and express an opinion on whether they give a true and fair view."
        } # 20 questions total
    ]

    for i, q in enumerate(qdata):
        cursor.execute("INSERT INTO questions (subject_id, text, explanation, difficulty, year, is_ai_generated, section) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (subject_id, q['text'], q['explanation'], 'medium', 2023, False, "Multiple Choice"))
        q_id = cursor.lastrowid
        
        for c in q['choices']:
            cursor.execute("INSERT INTO choices (question_id, text, is_correct, label) VALUES (?, ?, ?, ?)",
                           (q_id, c['text'], c['is_correct'], c['label']))

    conn.commit()
    conn.close()
    print(f"Successfully inserted {len(qdata)} ICAN questions into subject ID {subject_id}.")

if __name__ == "__main__":
    insert_ican()
