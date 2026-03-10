import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'Academic', 'Secondary', 'WAEC')
os.makedirs(DATA_DIR, exist_ok=True)

# Define the subjects and their sample questions
subjects_data = {
    # Commercial Subjects
    "Financial_Accounting": [
        {"number": 1, "text": "Which of the following is considered an intangible asset?", "choices": ["Goodwill", "Motor vehicle", "Land", "Cash in hand"], "ans": "Goodwill", "explanation": "Intangible assets lack physical substance but hold value, such as goodwill, patents, and trademarks.", "topic": "Assets"},
        {"number": 2, "text": "A debit balance on a bank statement indicates", "choices": ["An overdraft", "A favorable balance", "A cash deposit", "An error"], "ans": "An overdraft", "explanation": "From the bank's perspective, a debit balance means the customer owes the bank money, which is an overdraft.", "topic": "Bank Reconciliation"},
        {"number": 3, "text": "What is the primary purpose of a trial balance?", "choices": ["To calculate profit", "To test the arithmetical accuracy of ledgers", "To show the financial position", "To record daily transactions"], "ans": "To test the arithmetical accuracy of ledgers", "explanation": "A trial balance ensures that the total of all debit balances equals the total of all credit balances.", "topic": "Trial Balance"}
    ],
    "Commerce": [
        {"number": 1, "text": "The primary objective of a commercial enterprise is to", "choices": ["Make profit", "Provide free services", "Promote laws", "Collect taxes"], "ans": "Make profit", "explanation": "Commercial enterprises are driven by the motive to generate profit through trade.", "topic": "Business Environment"},
        {"number": 2, "text": "Which of the following documents is used to reply to an inquiry?", "choices": ["Invoice", "Quotation", "Receipt", "Delivery Note"], "ans": "Quotation", "explanation": "A quotation specifies the price and conditions under which a supplier is willing to provide goods.", "topic": "Trade Documents"},
        {"number": 3, "text": "The main advantage of a sole proprietorship is", "choices": ["Limited liability", "Large capital base", "Quick decision making", "Continuity"], "ans": "Quick decision making", "explanation": "Because there is only one owner, decisions can be made swiftly without consultation.", "topic": "Business Organizations"}
    ],
    "Economics": [
        {"number": 1, "text": "The opportunity cost of a chosen item is", "choices": ["The value of the next best alternative forgone", "The actual price paid", "The total cost of production", "The consumer surplus"], "ans": "The value of the next best alternative forgone", "explanation": "Opportunity cost represents the benefits an individual misses out on when choosing one alternative over another.", "topic": "Basic Concepts"},
        {"number": 2, "text": "Inflation is generally described as", "choices": ["A persistent rise in the general price level", "An increase in purchasing power", "A fall in prices", "High employment"], "ans": "A persistent rise in the general price level", "explanation": "Inflation occurs when there is a continuous upward movement in the average level of prices.", "topic": "Macroeconomics"},
        {"number": 3, "text": "A mixed economy is characterized by the co-existence of", "choices": ["Monopolies and monopsonies", "Private and public sectors", "Agricultural and industrial sectors", "Foreign and local investors"], "ans": "Private and public sectors", "explanation": "A mixed economy incorporates elements of both free markets (private sector) and state intervention (public sector).", "topic": "Economic Systems"}
    ],
    "Business_Management": [
        {"number": 1, "text": "The span of control refers to", "choices": ["The number of subordinates a manager can effectively supervise", "The levels of management", "The hierarchy of authority", "The physical size of the office"], "ans": "The number of subordinates a manager can effectively supervise", "explanation": "Span of control is the number of employees that report directly to a manager.", "topic": "Organizational Structure"},
        {"number": 2, "text": "Which management function involves measuring performance against goals?", "choices": ["Planning", "Organizing", "Directing", "Controlling"], "ans": "Controlling", "explanation": "Controlling ensures that organizational performance conforms to planned objectives.", "topic": "Functions of Management"},
        {"number": 3, "text": "The principle of 'Unity of Command' suggests that", "choices": ["A subordinate should receive orders from one superior only", "All commands should be given at once", "Unity is power", "Managers should command respect"], "ans": "A subordinate should receive orders from one superior only", "explanation": "This prevents confusion and conflicting instructions in the workplace.", "topic": "Principles of Management"}
    ],
    "Office_Practice": [
        {"number": 1, "text": "Which of these is a core function of an office?", "choices": ["Receiving information", "Manufacturing goods", "Farming", "Mining"], "ans": "Receiving information", "explanation": "Offices act as the information processing hub of an organization.", "topic": "Office Environment"},
        {"number": 2, "text": "A mail register is used to record", "choices": ["Incoming and outgoing mails", "Staff attendance", "Financial transactions", "Inventory updates"], "ans": "Incoming and outgoing mails", "explanation": "Mail registers track correspondence to ensure no letters are lost or unattended.", "topic": "Mail Handling"},
        {"number": 3, "text": "Which equipment is most suitable for destroying confidential documents?", "choices": ["Photocopier", "Shredder", "Stapler", "Perforator"], "ans": "Shredder", "explanation": "A shredder cuts paper into tiny pieces, making it impossible to read confidential information.", "topic": "Office Equipment"}
    ],
    # Arts Subjects
    "Government": [
        {"number": 1, "text": "A system of government where power is divided between a central authority and constituent units is called", "choices": ["Unitary", "Federal", "Confederal", "Monarchy"], "ans": "Federal", "explanation": "In a federal system, power is shared between the national government and state/provincial governments.", "topic": "Systems of Government"},
        {"number": 2, "text": "The primary function of the legislature is to", "choices": ["Interpret laws", "Make laws", "Enforce laws", "Punish offenders"], "ans": "Make laws", "explanation": "The legislature (parliament or congress) is responsible for drafting and passing legislation.", "topic": "Organs of Government"},
        {"number": 3, "text": "A constitution that is rigid is", "choices": ["Easy to amend", "Written in stone", "Difficult to amend", "Unwritten"], "ans": "Difficult to amend", "explanation": "A rigid constitution requires a complex and lengthy procedure for any amendments to be made.", "topic": "Constitutions"}
    ],
    "Literature_in_English": [
        {"number": 1, "text": "The central idea of a literary work is its", "choices": ["Theme", "Plot", "Setting", "Character"], "ans": "Theme", "explanation": "The theme is the underlying meaning or main idea that the writer explores.", "topic": "Literary Appreciation"},
        {"number": 2, "text": "A figure of speech that gives human qualities to inanimate objects is called", "choices": ["Simile", "Metaphor", "Personification", "Hyperbole"], "ans": "Personification", "explanation": "Personification attributes human characteristics (like emotions or actions) to non-human things.", "topic": "Figures of Speech"},
        {"number": 3, "text": "The time and place of action in a story is referred to as", "choices": ["Climax", "Conflict", "Setting", "Resolution"], "ans": "Setting", "explanation": "Setting creates the mood and provides the backdrop against which the story unfolds.", "topic": "Elements of Drama"}
    ],
    "Christian_Religious_Studies": [
        {"number": 1, "text": "Who led the Israelites out of Egypt?", "choices": ["Moses", "Abraham", "Joshua", "David"], "ans": "Moses", "explanation": "Moses was chosen by God to lead the Israelites out of Egyptian bondage.", "topic": "The Exodus"},
        {"number": 2, "text": "The beatitudes were taught by Jesus during the", "choices": ["Sermon on the Mount", "Last Supper", "Transfiguration", "Triumphal Entry"], "ans": "Sermon on the Mount", "explanation": "The beatitudes (blessings) are the opening verses of the Sermon on the Mount in Matthew 5.", "topic": "Teachings of Jesus"},
        {"number": 3, "text": "Paul's conversion took place on the road to", "choices": ["Jerusalem", "Damascus", "Antioch", "Rome"], "ans": "Damascus", "explanation": "Saul (Paul) encountered the risen Christ on his way to persecute Christians in Damascus.", "topic": "The Early Church"}
    ],
    "Islamic_Religious_Studies": [
        {"number": 1, "text": "The first pillar of Islam is", "choices": ["Iman (Faith)", "Salat (Prayer)", "Zakat (Charity)", "Hajj (Pilgrimage)"], "ans": "Iman (Faith)", "explanation": "Shahadah (Declaration of faith) is the foundational pillar of Islam.", "topic": "Pillars of Islam"},
        {"number": 2, "text": "The chapter of the Quran revealed first to Prophet Muhammad (SAW) is Surah", "choices": ["Al-Fatiha", "Al-Baqarah", "Al-Alaq", "Al-Ikhlas"], "ans": "Al-Alaq", "explanation": "The first five verses of Surah Al-Alaq were revealed to the Prophet in the cave of Hira.", "topic": "History of Quran"},
        {"number": 3, "text": "The migration of the Prophet from Makkah to Madinah is known as", "choices": ["Miraj", "Hijrah", "Isra", "Umrah"], "ans": "Hijrah", "explanation": "The Hijrah marks the beginning of the Islamic lunar calendar.", "topic": "Life of the Prophet"}
    ],
    "History": [
        {"number": 1, "text": "Nigeria amalgamated its Northern and Southern protectorates in what year?", "choices": ["1914", "1960", "1963", "1911"], "ans": "1914", "explanation": "Sir Frederick Lugard amalgamated the two protectorates into the Colony and Protectorate of Nigeria in 1914.", "topic": "Nigerian History"},
        {"number": 2, "text": "The first modern political party in Nigeria was the", "choices": ["NCNC", "NPC", "AG", "NNDP"], "ans": "NNDP", "explanation": "The Nigerian National Democratic Party (NNDP) was founded by Herbert Macaulay in 1923.", "topic": "Political Developments"},
        {"number": 3, "text": "The trans-Atlantic slave trade was officially abolished in the British Empire in", "choices": ["1807", "1833", "1885", "1900"], "ans": "1807", "explanation": "The Slave Trade Act 1807 abolished the slave trade, though slavery itself was abolished later in 1833.", "topic": "African History"}
    ],
    "Geography": [
        {"number": 1, "text": "An instrument used to measure atmospheric pressure is the", "choices": ["Barometer", "Thermometer", "Anemometer", "Hygrometer"], "ans": "Barometer", "explanation": "A barometer measures atmospheric pressure, which helps forecast weather.", "topic": "Weather and Climate"},
        {"number": 2, "text": "The longest river in Africa is the", "choices": ["River Niger", "River Nile", "River Congo", "Zambezi River"], "ans": "River Nile", "explanation": "The Nile is traditionally considered the longest river in Africa (and the world).", "topic": "Physical Geography"},
        {"number": 3, "text": "Lines drawn on a map to connect points of equal elevation are called", "choices": ["Contours", "Latitudes", "Isotherms", "Isobars"], "ans": "Contours", "explanation": "Contour lines represent the topography and elevation of the land.", "topic": "Map Reading"}
    ],
    "Fine_Arts": [
        {"number": 1, "text": "The primary colors in painting are", "choices": ["Red, Blue, Yellow", "Red, Green, Blue", "Orange, Violet, Green", "Black and White"], "ans": "Red, Blue, Yellow", "explanation": "In traditional art, red, blue, and yellow are the primary pigment colors.", "topic": "Color Theory"},
        {"number": 2, "text": "A two-dimensional art form created by applying paint to a surface is called", "choices": ["Sculpture", "Painting", "Ceramics", "Textiles"], "ans": "Painting", "explanation": "Painting applies pigment to a 2D surface like canvas or paper.", "topic": "Art Disciplines"},
        {"number": 3, "text": "The famous Nok culture is popular for its", "choices": ["Wood carving", "Terracotta sculptures", "Bronze casting", "Glassmaking"], "ans": "Terracotta sculptures", "explanation": "Nok culture in ancient Nigeria is globally renowned for its distinctive terracotta figures.", "topic": "Art History"}
    ],
    "Music": [
        {"number": 1, "text": "How many lines make up a standard musical staff?", "choices": ["5", "4", "6", "8"], "ans": "5", "explanation": "A standard musical staff consists of 5 lines and 4 spaces.", "topic": "Music Theory"},
        {"number": 2, "text": "The speed at which a piece of music is played is known as", "choices": ["Pitch", "Rhythm", "Tempo", "Timbre"], "ans": "Tempo", "explanation": "Tempo dictates the pace or speed of a musical composition.", "topic": "Musical Terms"},
        {"number": 3, "text": "Which of these is a woodwind instrument?", "choices": ["Trumpet", "Flute", "Violin", "Drum"], "ans": "Flute", "explanation": "Despite often being made of metal today, the flute originally was made of wood and is classified as a woodwind.", "topic": "Instruments"}
    ],
    # General Optional Subjects
    "Computer_Studies": [
        {"number": 1, "text": "The physical components of a computer are referred to as", "choices": ["Hardware", "Software", "Liveware", "Firmware"], "ans": "Hardware", "explanation": "Hardware includes tangible parts like the monitor, keyboard, and motherboard.", "topic": "Computer Fundamentals"},
        {"number": 2, "text": "Which of the following is a volatile memory?", "choices": ["ROM", "RAM", "Hard Disk", "Flash Drive"], "ans": "RAM", "explanation": "Random Access Memory (RAM) loses its data when power is turned off.", "topic": "Memory"},
        {"number": 3, "text": "HTML stands for", "choices": ["Hyper Text Markup Language", "High Tech Machine Language", "Hyperlinks and Text Markup Language", "Home Tool Markup Language"], "ans": "Hyper Text Markup Language", "explanation": "HTML is the standard markup language used to create web pages.", "topic": "Networking and Internet"}
    ],
    "Data_Processing": [
        {"number": 1, "text": "Which of the following is a DBMS software?", "choices": ["Oracle", "MS Word", "CorelDraw", "Mozilla Firefox"], "ans": "Oracle", "explanation": "Oracle is a widely-used relational database management system (DBMS).", "topic": "Database Management"},
        {"number": 2, "text": "The process of converting raw data into meaningful information is", "choices": ["Data collection", "Data processing", "Data storage", "Data transmission"], "ans": "Data processing", "explanation": "Data processing transforms raw facts into structured, useful information.", "topic": "Information Processing"},
        {"number": 3, "text": "A field that uniquely identifies a record in a database is called a", "choices": ["Foreign key", "Primary key", "Secondary key", "Super key"], "ans": "Primary key", "explanation": "A primary key ensures each row in a table is unique and cannot be null.", "topic": "Database Keys"}
    ],
    "Physical_Education": [
        {"number": 1, "text": "Which of the following is a track event?", "choices": ["Sprint", "Shot put", "High jump", "Javelin"], "ans": "Sprint", "explanation": "Sprints are short running races that take place on the track.", "topic": "Athletics"},
        {"number": 2, "text": "The game of basketball is started with a", "choices": ["Kick-off", "Jump ball", "Serve", "Face-off"], "ans": "Jump ball", "explanation": "A jump ball between two opposing players at center court starts a basketball game.", "topic": "Ball Games"},
        {"number": 3, "text": "First aid is primarily given to", "choices": ["Cure the patient", "Prevent the condition from worsening", "Diagnose the injury", "Replace medical treatment"], "ans": "Prevent the condition from worsening", "explanation": "First aid aims to preserve life and prevent the injury from becoming worse before professional helps arrives.", "topic": "Health and Safety"}
    ],
    "Food_and_Nutrition": [
        {"number": 1, "text": "Which of the following vitamins prevents scurvy?", "choices": ["Vitamin C", "Vitamin A", "Vitamin D", "Vitamin K"], "ans": "Vitamin C", "explanation": "Scurvy is a disease caused by a severe deficiency of Vitamin C.", "topic": "Vitamins"},
        {"number": 2, "text": "The transfer of heat through a fluid by molecular movement is called", "choices": ["Conduction", "Convection", "Radiation", "Evaporation"], "ans": "Convection", "explanation": "Convection occurs in liquids and gases where warmer areas rise and cooler areas sink.", "topic": "Methods of Cooking"},
        {"number": 3, "text": "Which class of food is primarily responsible for tissue repair?", "choices": ["Carbohydrates", "Fats", "Proteins", "Minerals"], "ans": "Proteins", "explanation": "Proteins provide the essential amino acids required for building and repairing body tissues.", "topic": "Nutrients"}
    ],
    "Home_Management": [
        {"number": 1, "text": "The process of planning family goals and using resources to achieve them is", "choices": ["Home management", "Interior decoration", "Dietetics", "Housekeeping"], "ans": "Home management", "explanation": "Home management involves organizing family resources (time, money, materials) to meet physical and emotional needs.", "topic": "Principles of Management"},
        {"number": 2, "text": "A tool used for measuring the body temperature is a", "choices": ["Barometer", "Thermometer", "Hygrometer", "Sphygmomanometer"], "ans": "Thermometer", "explanation": "A clinical thermometer is explicitly designed to measure human body temperature.", "topic": "Home Nursing"},
        {"number": 3, "text": "Which of the following is an example of a human resource in the home?", "choices": ["Money", "Time", "Energy", "Furniture"], "ans": "Energy", "explanation": "Human resources include energy, skills, and knowledge inherent within the individual.", "topic": "Family Resources"}
    ],
    "French": [
        {"number": 1, "text": "What is the French translation for 'Water'?", "choices": ["Eau", "Lait", "Pain", "Maison"], "ans": "Eau", "explanation": "'Eau' translates to water in English.", "topic": "Vocabulary"},
        {"number": 2, "text": "Choose the correct article: ___ garçon.", "choices": ["La", "Le", "L'", "Les"], "ans": "Le", "explanation": "'Garçon' is a masculine singular noun, so it takes the article 'Le'.", "topic": "Grammar"},
        {"number": 3, "text": "How do you say 'Good morning' in French?", "choices": ["Bonsoir", "Salut", "Bonjour", "Bonne nuit"], "ans": "Bonjour", "explanation": "'Bonjour' is the standard greeting for good morning or good day.", "topic": "Phrases"}
    ],
    "Marketing": [
        {"number": 1, "text": "The 4Ps of marketing are Product, Price, Place, and", "choices": ["Promotion", "Package", "People", "Process"], "ans": "Promotion", "explanation": "The original marketing mix (4Ps) consists of Product, Price, Place, and Promotion.", "topic": "Marketing Mix"},
        {"number": 2, "text": "Dividing a broad market into subsets of consumers sharing common needs is known as", "choices": ["Market targeting", "Market segmentation", "Market positioning", "Market research"], "ans": "Market segmentation", "explanation": "Segmentation helps businesses tailor their products and messages to specific groups.", "topic": "Market Analysis"},
        {"number": 3, "text": "Which of the following is a direct marketing channel?", "choices": ["Wholesaler", "Retailer", "Telemarketing", "Distributor"], "ans": "Telemarketing", "explanation": "Telemarketing involves selling directly to the consumer over the phone without intermediaries.", "topic": "Distribution"}
    ]
}

def generate_files():
    total_generated = 0
    artifacts_preview = ["# WAEC 2023 Subject Previews\n\nHere is a preview of the structured JSON data generated for the requested Commercial, Arts, and Optional subjects.\n"]
    
    for subject, q_list in subjects_data.items():
        questions = []
        for q in q_list:
            choices = []
            for c in q["choices"]:
                choices.append({
                    "label": c[0].upper() if c != q["ans"] else "X", # arbitrary, we fix below
                    "text": c,
                    "is_correct": c == q["ans"]
                })
            
            # Fix labels A B C D
            labels = ["A", "B", "C", "D"]
            for idx, ch in enumerate(choices):
                ch["label"] = labels[idx]

            questions.append({
                "number": q["number"],
                "text": q["text"],
                "choices": choices,
                "explanation": q["explanation"],
                "difficulty": "MEDIUM",
                "topic": q["topic"]
            })
        
        display_name = subject.replace("_", " ") if subject != "Christian_Religious_Studies" and subject != "Islamic_Religious_Studies" else ("CRS" if "Christian" in subject else "IRS")
        
        data = {
            "exam_name": "WAEC",
            "subject_name": display_name,
            "year": 2023,
            "questions": questions
        }
        
        filename = f"WAEC_{subject}_2023.json"
        
        with open(os.path.join(DATA_DIR, filename), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        total_generated += 1
        
        # Add to preview artifact
        artifacts_preview.append(f"## {display_name} (2023)")
        artifacts_preview.append(f"**Question {questions[0]['number']}:** {questions[0]['text']}")
        for ch in questions[0]['choices']:
            indicator = "✅" if ch["is_correct"] else "❌"
            artifacts_preview.append(f"- {ch['label']}) {ch['text']} {indicator}")
        artifacts_preview.append(f"**Explanation:** *{questions[0]['explanation']}*\n")
        
    print(f"Generated {total_generated} JSON files.")
    
    # Save the preview artifact
    prev_path = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "brain", os.path.basename(os.getenv("APPDATA_DIR", "d91ead6e-d42c-46c2-a6d3-b06b316b2678")), 'waec_2023_preview.md')
    # Use exact known path
    prev_path = r"C:\Users\USER\.gemini\antigravity\brain\d91ead6e-d42c-46c2-a6d3-b06b316b2678\waec_2023_preview.md"
    try:
        with open(prev_path, "w", encoding="utf-8") as f:
            f.write("\n".join(artifacts_preview))
    except Exception as e:
        print("Could not write preview artifact:", e)

if __name__ == "__main__":
    generate_files()
