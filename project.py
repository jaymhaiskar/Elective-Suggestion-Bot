import pandas as pd
import sqlite3
import PyPDF2
import re

# ---------- STEP 1: Upload transcript ----------
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

# ---------- STEP 2: Parse transcript ----------
def parse_transcript(text):
    # Example regex for course: "COMP 101 - Intro to CS A"
    pattern = r'\b([A-Z]{4}\s?[0-9]{4})\s+(.+)'
    #  \b[A-Z]{4}\s?[0-9]{4}\b

    # courses = []
    # with open(text, "r", encoding="utf-8") as f:
    #     for line in f:
    #         line = line.strip()
    #         match = re.match(pattern, line)   
    #         if match:
    #             code = match.group(1)      # course code
    #             name = match.group(2)      # course name
    #             total_credits = match.group(3)   # credits
    #             grade = match.group(4)     # letter grade
    #             gpa_grade = match.group(5)    # GPA points
    #             courses.append((code, name, total_credits, grade, gpa_grade))
    
    course_code = re.findall(pattern, text)
    print("results", course_code)
    #df = pd.DataFrame(courses, columns=["course_code", "course_name", "total credits", "grade", "gpa_grade"])


# ---------- STEP 3: Convert to GPA ----------
grade_scale = {
    "A+": 4.33, "A": 4.0, "A-": 3.67,
    "B+": 3.33, "B": 3.0, "B-": 2.67,
    "C+": 2.33, "C": 2.0, "C-": 1.67,
    "D": 1.0, "F": 0.0
}

def compute_gpa(df):
    df["gpa_points"] = df["grade"].map(grade_scale)
    return df["gpa_points"].mean()

# ---------- STEP 4: Store in SQL ----------
def save_to_db(student_name, df, gpa):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, gpa) VALUES (?,?)", (student_name, gpa))
    student_id = c.lastrowid
    
    for _, row in df.iterrows():
        c.execute("INSERT INTO courses (course_code, course_name, grade, gpa_points, student_id) VALUES (?,?,?,?,?)",
                  (row.course_code, row.course_name, row.grade, row.gpa_points, student_id))
    conn.commit()
    conn.close()

# ---------- STEP 5: Recommend electives ----------
def recommend_electives(student_id):
    conn = sqlite3.connect("students.db")
    df_courses = pd.read_sql_query(f"SELECT * FROM courses WHERE student_id={student_id}", conn)
    df_electives = pd.read_sql_query("SELECT * FROM electives", conn)
    
    # Simple rule: recommend electives in categories where student did well
    avg_gpa = df_courses["gpa_points"].mean()
    recommended = df_electives[df_electives["difficulty_level"] <= avg_gpa + 0.5]
    
    return recommended.sort_values("difficulty_level")

# ---------- STEP 6: Chatbot interaction ----------
def chatbot(student_id):
    print("Hello! Ask me about your elective recommendations. Please type 'quit' or 'exit' to end the conversation")
    while True:
        q = input("You: ")
        if "electives" in q.lower():
            recs = recommend_electives(student_id)
            print("Bot: Here are electives I think you'd be good at:")
            print(recs[["elective_code", "elective_name"]].to_string(index=False))
        elif q.lower() in ["quit", "exit"]:
            break
        else:
            print("Bot: I can help you with elective advice. Try asking me about electives!")

# ---------- DEMO ----------
if __name__ == "__main__":
    text = extract_text_from_pdf("transcript.pdf")
    # print(text)
    df = parse_transcript(text)
    # print(df)
    # gpa = compute_gpa(df)
    # save_to_db("John Doe", df, gpa)
    
    # chatbot(1)

    #currently stuck at parse transcript, nothing being populated in the results list


# make electives table 
# make courses table
# check grade scale
# check for loop in def save_to_db(student_name, df, gpa), does studentid update? where are you getting info for all other variables?
# check logic in recommend_electives(student_id):
# check logic in chatbot
