"""
IELTS Full Exam Insert — Mock IELTS questions for Academic and General Training tracks.
Focus on Reading and Listening (MCQ) for CBT simulation, plus Writing for AI Grading.
"""
import sqlite3, os, json

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'past_questions_v2.db')

# Academic Reading Sample Questions
AR = [
    {"t":"According to recent research, the primary advantage of renewable energy over fossil fuels is:","c":[["Lower initial infrastructure costs",0],["Greater availability in arid regions",0],["Minimal environmental impact throughout the lifecycle",1],["Consistency in power generation regardless of weather",0]],"e":"Renewable energy sources like solar and wind have a much smaller carbon footprint and less pollution compared to fossil fuels.","tp":"Renewable Energy","y":2024},
    {"t":"What led to the sudden decline of the Mayan civilization according to the 'climate change theory'?","c":[["Continuous volcanic eruptions over two centuries",0],["Severe and prolonged drought periods during the 9th century",1],["Sudden rise in sea levels across the coastal plains",0],["Massive tectonic shifts that disrupted water supplies",0]],"e":"Research suggests a series of severe droughts significantly impacted Mayan agriculture and social stability.","tp":"History & Archeology","y":2023},
    {"t":"In the context of the passage, the term 'neural plasticity' refers to:","c":[["The brain's ability to remain unchanged over decades",0],["The physical stiffness of brain tissues in older age",0],["The capacity of the nervous system to adapt its structure and function",1],["The chemical resistance of neurons to external toxins",0]],"e":"Neural plasticity describes how the brain reorganizes itself by forming new neural connections throughout life.","tp":"Science & Biology","y":2024},
    {"t":"The 'Hawthorne Effect' suggests that productivity increases when:","c":[["Employees receive higher financial compensation",0],["Workers are aware they are being observed in a study",1],["Artificial lighting is improved in technical workshops",0],["Break times are extended significantly",0]],"e":"The Hawthorne Effect is a type of reactivity in which individuals modify an aspect of their behavior in response to ihrer awareness of being observed.","tp":"Social Science","y":2023},
    {"t":"What is the main challenge mentioned regarding the colonization of Mars?","c":[["The lack of a breathable atmosphere and high radiation levels",1],["The absence of any water ice beneath the surface",0],["The excessive gravitational pull compared to Earth",0],["The extreme heat during the daytime hours",0]],"e":"Mars has a very thin atmosphere and lacks a global magnetic field, exposing the surface to dangerous solar radiation.","tp":"Astronomy & Space","y":2024}
]

# Academic Listening Sample Questions (Scripted content)
AL = [
    {"t":"What time does the university library close on Saturdays?","c":[["6:00 PM",0],["8:00 PM",1],["10:00 PM",0],["Midnight",0]],"e":"The audio script mentions that while it closes at midnight on weekdays, it closes earlier at 8:00 PM on Saturdays.","tp":"Campus Life","y":2024},
    {"t":"Where should students go to collect their new ID cards?","c":[["The Registrar's Office",0],["The Student Union Building",1],["The Main Hall Reception",0],["The Campus Security Hub",0]],"e":"The speaker instructs students to visit the second floor of the Student Union Building for ID collection.","tp":"Orientation","y":2024},
    {"t":"What is the primary theme of the upcoming guest lecture by Dr. Aris?","c":[["Marine biodiversity in the Atlantic",0],["Ethical implications of genetic engineering",1],["History of the Industrial Revolution",0],["Future of global economic trade",0]],"e":"Dr. Aris will be presenting his new research on the ethics surrounding gene-editing technologies.","tp":"Academic Lectures","y":2024},
    {"t":"What item is NOT allowed in the examinations according to the briefing?","c":[["Clear plastic water bottles",0],["Programmable calculators",1],["Blue or black ink pens",0],["Analogue wristwatches",0]],"e":"The briefing explicitly states that only non-programmable calculators are permitted.","tp":"Exam Regulations","y":2023},
    {"t":"Why was the field trip to the botanical gardens postponed?","c":[["The gardens were closed for maintenance",0],["The transport company cancelled the bus",0],["Adverse weather conditions were forecast",1],["The professor had a medical emergency",0]],"e":"The audio indicates the trip was moved to next Tuesday due to a 90% chance of heavy rain.","tp":"Logistics","y":2024}
]

# General Training Reading (Everyday contexts)
GR = [
    {"t":"According to the notice, what must an employee do if they lose their locker key?","c":[["Buy a new lock from a local store",0],["Inform the Human Resources department immediately",1],["Ask a colleague to share their locker",0],["Wait for the janitor to open it at night",0]],"e":"The staff handbook states HR manages the replacement of lost keys for a small fee.","tp":"Workplace Rules","y":2024},
    {"t":"The flyer states that the discount code 'SUMMER20' can only be used for:","c":[["Items already on sale",0],["Bulk orders over 100 units",0],["Full-priced clothing and accessories",1],["Electronic items purchased in-store",0]],"e":"The fine print specifies the code applies to full-priced stock only.","tp":"Commercial Notices","y":2024},
    {"t":"What is the recommended procedure for reporting a fire in the apartment complex?","c":[["Call the landlord after leaving the building",0],["Trigger the nearest fire alarm and then call 999",1],["Try to extinguish the fire before alerting others",0],["Email the management company with a photo of the fire",0]],"e":"The safety manual emphasizes alerting others via the alarm first, then contacting emergency services.","tp":"Public Safety","y":2023}
]

# Writing Tasks (Sample prompts stored for AI context)
AW = [
    {"t":"Writing Task 2: Some people believe that the best way to reduce local crime is to increase the length of prison sentences. Others, however, believe there are better ways to help reduce crime. Discuss both views and give your opinion.","c":[],"e":"","tp":"Social Issues","y":2024},
    {"t":"Writing Task 1: The graph below shows the consumption of fish and different kinds of meat in a European country between 1979 and 2004. Describe the main features and make comparisons where relevant.","c":[],"e":"","tp":"Data Interpretation","y":2024}
]

ALL_DATA = {
    "Reading": AR + GR, 
    "Listening": AL,
    "Writing": AW,
    "Speaking": [{"t":"Part 2: Describe a major city you would like to visit in the future. You should say: Where it is, What you know about it, What you would do there, and explain why you want to visit it.","c":[],"e":"","tp":"Travel","y":2024}]
}

MODES = {
    "Academic": ["Reading", "Listening", "Writing", "Speaking"],
    "General Training": ["Reading", "Listening", "Writing", "Speaking"],
}

def fmt(raw):
    labels = "ABCD"
    return [{"text": raw[i][0], "is_correct": bool(raw[i][1]), "label": labels[i]} for i in range(len(raw))]

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    total = 0

    for mode, subjects in MODES.items():
        exam_name = f"IELTS {mode}"
        c.execute("SELECT id FROM exams WHERE name=?", (exam_name,))
        r = c.fetchone()
        if r:
            eid = r[0]
        else:
            c.execute("INSERT INTO exams (name,category,description,sub_category) VALUES (?,?,?,?)",
                      (exam_name, "Standardized", f"International English Language Testing System - {mode}", mode))
            eid = c.lastrowid

        for subj in subjects:
            c.execute("SELECT id FROM subjects WHERE name=? AND exam_id=?", (subj, eid))
            r = c.fetchone()
            if r:
                sid = r[0]
                c.execute("DELETE FROM choices WHERE question_id IN (SELECT id FROM questions WHERE subject_id=?)", (sid,))
                c.execute("DELETE FROM questions WHERE subject_id=?", (sid,))
            else:
                c.execute("INSERT INTO subjects (name,exam_id) VALUES (?,?)", (subj, eid))
                sid = c.lastrowid

            qs = ALL_DATA.get(subj, [])
            for q in qs:
                # Some subjects like Writing don't have multiple choices
                has_choices = len(q["c"]) > 0
                section = "Section A" if has_choices else "Essay/Short Answer"
                
                c.execute("INSERT INTO questions (subject_id,text,explanation,difficulty,year,is_ai_generated,section,topic) VALUES (?,?,?,?,?,?,?,?)",
                          (sid, q["t"], q.get("e",""), "MEDIUM", q.get("y",2024), False, section, q.get("tp","")))
                qid = c.lastrowid
                
                if has_choices:
                    for ch in fmt(q["c"]):
                        c.execute("INSERT INTO choices (question_id,text,is_correct,label) VALUES (?,?,?,?)",
                                  (qid, ch["text"], ch["is_correct"], ch["label"]))
                total += 1
            print(f"  [{mode}] {subj}: {len(qs)} questions (sid={sid})")

    conn.commit()
    conn.close()
    print(f"\n[DONE] {total} IELTS questions inserted across both modes.")

if __name__ == "__main__":
    main()
