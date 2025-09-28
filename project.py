import pandas as pd
import sqlite3
import PyPDF2
import re
import pdfplumber

# Write more on: show example where input -> output 
# hook in to openAI API, upload pdf to openAI return, file format that u want to use if returned
# document both stategies for final paper (regex vs AI)


# ---------- STEP 1: Parse transcript ----------
def parse_transcript(pdf_path):
    # Example regex for course: "COMP 101 - Intro to CS A"
    courses = []
# Open and read PDF
    with pdfplumber.open(pdf_path) as pdf:
        print("Inside with statement")
        for page in pdf.pages:
            print("Inside first for loop")
            text = page.extract_text()
            # print(text)
            for line in text.splitlines():
                # Regex for lines with course info, ignores transfer credit
                match = re.match(r"^([A-Z]{2,4}\s\d{3})\s+(.+?)\s+([A-Z]{1,3}[+-]?)\s+(\d\.\d{3})\s+(\d+\.\d{2})$", line)
                # print("match", match)
                if match:
                    course_num = match.group(1)
                    course_name = match.group(2).strip()
                    grade = match.group(3)
                    courses.append((course_num, course_name, grade))
    
    df= pd.DataFrame(courses, columns=["course_code", "course_name", "letter_grade"])
    return df
    
# ---------- STEP 2: Convert to GPA ----------
grade_scale = {
    "A+": 4.33, "A": 4.0, "A-": 3.67,
    "B+": 3.33, "B": 3.0, "B-": 2.67,
    "C+": 2.33, "C": 2.0, "C-": 1.67,
    "D": 1.0, "F": 0.0, "W": 0.0
}

def compute_gpa(df):
    df["gpa_points"] = df["letter_grade"].map(grade_scale)
    return df["gpa_points"].mean()

# ---------- STEP 3: Store in SQL ----------
def save_to_db(student_name, student_id, df, gpa):
    conn = sqlite3.connect("students.db")
    c = conn.cursor()

    print(student_id, student_name, gpa)
    # need to ask for student name and student id
    c.execute("INSERT INTO students (id, name, gpa) VALUES (?,?)", (student_id, student_name, gpa))

    for _, row in df.iterrows():
        c.execute("INSERT INTO courses (student_id, course_code, course_name, grade, gpa_points) VALUES (?,?,?,?,?)",
                  (student_id, row.course_code, row.course_name, row.grade, row.gpa_points, ))
    conn.commit()
    conn.close()

# ---------- STEP 4: Recommend electives ----------
def recommend_electives(student_id):

# use sci kit learn or pass to ChatGPT API
# talk about the three different types of AI, rule based, gen AI, and machine learning (test)

    conn = sqlite3.connect("students.db")
    df_courses = pd.read_sql_query(f"SELECT * FROM courses WHERE student_id={student_id}", conn)
    df_electives = pd.read_sql_query("SELECT * FROM electives", conn)
    
    # Simple rule: recommend electives in categories where student did well
    avg_gpa = df_courses["gpa_points"].mean()
    recommended = df_electives[df_electives["difficulty_level"] <= avg_gpa + 0.5]
    
    return recommended.sort_values("difficulty_level")

# ---------- STEP 5: Chatbot interaction ----------
# def chatbot(student_id):
#     print("Hello! Ask me about your elective recommendations. Please type 'quit' or 'exit' to end the conversation")
#     while True:
#         q = input("You: ")
#         if "electives" in q.lower():
#             recs = recommend_electives(student_id)
#             print("Bot: Here are electives I think you'd be good at:")
#             print(recs[["elective_code", "elective_name"]].to_string(index=False))
#         elif q.lower() in ["quit", "exit"]:
#             break
#         else:
#             print("Bot: I can help you with elective advice. Try asking me about electives!")

# ---------- DEMO ----------
if __name__ == "__main__":
    # For save to database function
    student_name = input("Please enter your name: ")
    student_id = int(input("Please enter your student id: "))
    # print(text)
    df = parse_transcript("capilano_unofficial_transcript.pdf")
    # print(df)
    gpa = compute_gpa(df)
    print(gpa)
    save_to_db(student_name, student_id, df, gpa)
    
    # chatbot(1)



# make electives table 
# check grade scale
# check for loop in def save_to_db(student_name, df, gpa), does studentid update? where are you getting info for all other variables?
# check logic in recommend_electives(student_id):
# check logic in chatbot
