import pandas as pd
import pdfplumber
import re
import sqlite3
from openai import OpenAI

# ---------- GLOBALS ----------
grade_scale = {
    "A+": 4.33, "A": 4.0, "A-": 3.67,
    "B+": 3.33, "B": 3.0, "B-": 2.67,
    "C+": 2.33, "C": 2.0, "C-": 1.67,
    "D": 1.0, "F": 0.0, "W": 0.0,
    "TA+": 4.33, "TA": 4.0, "TA-": 3.67,
    "TB+": 3.33, "TB": 3.0, "TB-": 2.67,
    "TC+": 2.33, "TC": 2.0, "TC-": 1.67,
    "TD": 1.0, "TF": 0.0, "TW": 0.0
}

# client = OpenAI()

# Map student preference keywords to subject prefixes
subject_map = {
    "science": ["BIOL", "CHEM", "PHYS"],
    "math": ["MATH", "STAT"],
    "computing": ["COMP", "INFO", "DATA"],
    "business": ["BUSN", "ECON"],
    "arts": ["ARTS", "ENGL", "HIST"]
}

# ---------- STEP 1: Parse transcript ----------
def parse_transcript(pdf_path):
    """Extract course codes, names, and grades from transcript PDF."""
    courses = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.splitlines():
                match = re.match(r"^([A-Z]{2,4}\s\d{3})\s+(.+?)\s+([A-Z]{1,3}[+-]?)\s+(\d\.\d{3})\s+(\d+\.\d{2})$", line)
                if match:
                    course_num = match.group(1).strip()
                    course_name = match.group(2).strip()
                    grade = match.group(3).strip()
                    courses.append((course_num, course_name, grade))
    df = pd.DataFrame(courses, columns=["course_code", "course_name", "letter_grade"])
    df["gpa_points"] = df["letter_grade"].map(grade_scale)
    df["subject"] = df["course_code"].str.extract(r"^([A-Z]{2,4})")
    print(df)
    return df

# ---------- STEP 2: Get courses from DB ----------
def get_courses_from_db():
    """Read all courses from the database (no category column)."""
    conn = sqlite3.connect("students.db")
    df_catalog = pd.read_sql_query("SELECT course_code, course_name, prerequisites FROM courses", conn)
    conn.close()
    return df_catalog

# # ---------- STEP 3: Filter catalog by preference ----------
# def filter_catalog_by_preference(df_catalog, preference):
#     """Filter courses whose subject prefix matches the student's chosen preference."""
#     subjects = subject_map.get(preference.lower(), [])
#     df_catalog["subject"] = df_catalog["course_code"].str.extract(r"^([A-Z]{2,4})")
#     return df_catalog[df_catalog["subject"].isin(subjects)]

# # ---------- STEP 4: Determine eligible courses ----------
# def find_eligible_courses(catalog_df, transcript_df):
#     """Find all preferred courses for which prerequisites have been satisfied."""
#     completed = set(transcript_df["course_code"].str.strip())
#     eligible = []

#     for _, row in catalog_df.iterrows():
#         prereqs = str(row["prerequisites"]).split(",")
#         prereqs = [p.strip() for p in prereqs if p.strip()]
#         if not prereqs or all(p in completed for p in prereqs):
#             eligible.append(row)

#     return pd.DataFrame(eligible)

# # ---------- STEP 5: Get AI recommendations ----------
# def get_ai_recommendations(preference, transcript_df, eligible_df):
#     """Ask ChatGPT for course suggestions given eligible courses."""
#     input_text = f"""
#     The student is interested in: {preference}

#     Completed transcript:
#     {transcript_df.to_string(index=False)}

#     Eligible preferred courses (based on prerequisites):
#     {eligible_df.to_string(index=False)}

#     Please recommend 5 elective courses the student can take next.
#     - Mention cases where previous courses unlock new ones.
#     - Example: "Since you've completed BIOL 101, you're now eligible for BIOL 210."
#     - Respond in a clear, numbered list.
#     """

#     response = client.responses.create(
#         model="gpt-4.5-turbo",
#         input=[{"role": "user", "content": input_text}]
#     )
#     return response.output_text

# ---------- MAIN ----------
if __name__ == "__main__":
    pdf_path = "capilano_unofficial_transcript.pdf"
    preference = input("What is your academic interest (e.g., science, math, computing, arts)? ")

    # Parse student transcript
    df_transcript = parse_transcript(pdf_path)

    # # Get full catalog from DB
    # df_catalog = get_courses_from_db()

    # # Filter by chosen preference
    # df_pref = filter_catalog_by_preference(df_catalog, preference)

    # # Determine which courses student is eligible for
    # df_eligible = find_eligible_courses(df_pref, df_transcript)

    # print("\n✅ Based on your transcript, you are eligible for these preferred courses:")
    # print(df_eligible[["course_code", "course_name", "prerequisites"]])

    # print("\n🤖 Contacting ChatGPT for elective recommendations...\n")
    # recommendations = get_ai_recommendations(preference, df_transcript, df_eligible)
    # print(recommendations)
