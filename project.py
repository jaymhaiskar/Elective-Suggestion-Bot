import os
import re
import pdfplumber
import pandas as pd
from openai import OpenAI

# ---------- Global Variables ----------
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

# Mapping of interest areas to course code prefixes
#EXPAND to fit all courses
INTEREST_MAPPING = {
    "science": ["BIOL", "CHEM", "ASTR", "PHYS", "SCI", "ENSO"],
    "math": ["MATH", "STAT"],
    "technology": ["COMP", "APSC", "BCPT", "IXD", "DIGI", "VFX"],
    "business": ["BADM", "BFIN", "BMKT", "IBUS", "NABU", "BTEC", "TOUR", "PADM"],
    "arts": ["AHIS", "DSGN", "IDES", "COST", "TXTL"],
    "film & media": ["MOPA", "DOCS", "IDF", "FILM", "ANIM", "ANAR", "CINE"],
    "music": ["JAZZ", "MUS", "ENSM", "ENSJ", "MUTH", "MT", "COND", "PMIP", "PPMI", "PMTI", "WMPI"],
    "theatre & performance": ["THTR", "ACTR", "ASAS", "MUTH", "TECT", "BPAC"],
    "communications": ["CMNS", "ADVR", "BMKT"],
    "humanities": ["ENGL", "HIST", "PHIL", "LING", "FREN", "SPAN", "CHIN", "JAPN", "FNST", "FNLG"],
    "social sciences": ["PSYC", "SOC", "ANTH", "POL", "GEOG", "WGST", "CRIM", "GLBS"],
    "education": ["EDUC", "EA", "KINE"],
    "health & wellness": ["KINE", "BIOL", "HCA", "RADP", "ABA", "MT"],
    "law & legal studies": ["LAW", "LGST", "CRIM"],
    "outdoor recreation": ["REC", "WLP", "TOUR"],
    "environment & sustainability": ["ENSO", "GEOG", "BIOL", "REC", "TOUR"],
    "indigenous studies": ["FNST", "FNLG", "IDST", "IDF", "ENSO"],
    "interdisciplinary": ["INTS", "LBST", "CAPS", "FYS", "IVPA", "SOSC"]
}

COURSE_CATALOG_PATH = "course_catalog.csv"
# ---------- STEP 1: Parse transcript ----------
def parse_transcript(pdf_path):
    """Extracts course info from transcript PDF using regex."""
    courses = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.splitlines():
                # Example line: COMP 101 Intro to CS A 3.000 4.00
                match = re.match(
                    r"^([A-Z]{2,4}\s\d{3})\s+(.+?)\s+([A-Z]{1,3}[+-]?)\s+\d\.\d{3}\s+\d+\.\d{2}$", 
                    line
                )
                if match:
                    course_code = match.group(1).strip()
                    course_name = match.group(2).strip()
                    grade = match.group(3).strip()
                    courses.append((course_code, course_name, grade))

    df = pd.DataFrame(courses, columns=["course_code", "course_name", "letter_grade"])
    df["gpa_points"] = df["letter_grade"].map(grade_scale)
    return df

def get_student_interests():
    """Prompt student to enter their interests"""
    print("\nAvailable interest areas:")
    for i, interest in enumerate(INTEREST_MAPPING.keys(), 1):
        print(f"{i}. {interest.title()}")
    
    print("\nEnter your interests (comma-separated numbers or names):")
    print("Example: 1,3 or science,arts")
    user_input = input("> ").strip()
    
    # Parse input
    selected_interests = []
    for item in user_input.split(','):
        item = item.strip().lower()
        # Check if it's a number
        if item.isdigit():
            idx = int(item) - 1
            if 0 <= idx < len(INTEREST_MAPPING):
                selected_interests.append(list(INTEREST_MAPPING.keys())[idx])
        # Check if it's a valid interest name
        elif item in INTEREST_MAPPING:
            selected_interests.append(item)
    
    return selected_interests

def filter_courses_by_interest(interests):
    """Filter courses from final2.txt based on student interests and return as DataFrame"""
    # Get all relevant course codes
    relevant_codes = []
    for interest in interests:
        relevant_codes.extend(INTEREST_MAPPING.get(interest, []))
    
    # Remove duplicates
    relevant_codes = list(set(relevant_codes))
    
    # Read course catalog and parse into DataFrame
    # Assuming format: COURSE_CODE\tCOURSE_DESCRIPTION\tRECOMMENDED_GPA\t...
    df = pd.read_csv(COURSE_CATALOG_PATH, sep=',', header=0, 
                     names=["course_code", "course_name", "prerequisites"])
    
    # Filter rows where course_code starts with any relevant code
    filtered_df = df[df['course_code'].str.startswith(tuple(relevant_codes))]
    
    return filtered_df
    print("inside function", filtered_df)


# ---------- STEP 3: AI Recommendations ----------
def get_ai_recommendations(student_df, filtered_df):
    """Passes transcript + filtered courses to OpenAI for elective recommendations."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment.")
    client = OpenAI(api_key=api_key)

    student_json = student_df.to_json(orient="records", indent=2)
    filtered_json = filtered_df.to_json(orient="records", indent=2)

    prompt = f"""
    You are an AI academic advisor specializing in course recommendations..

    Their completed transcript:
    {student_json}

    The available courses that match their interest:
    {filtered_json}

    Please recommend 5 courses they should take next, factoring in:
    1. Which courses they’ve already completed.
    2. Any courses where prerequisites are satisfied.
    3. Focus on courses that are newly unlocked because of prerequisites.
    4. Then recommend other advanced or related electives from the list.

    For each recommendation, explain briefly *why* it fits (e.g., "You’ve completed BIOL 101, so BIOL 210 is now available.").
    """

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are an AI academic advisor helping students pick electives."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


# ---------- MAIN EXECUTION ----------
if __name__ == "__main__":
    pdf_path = "transcript.pdf"

    # Step 1: Ask student for their interest
    # interest = input("What area are you most interested in (e.g., science, math, computing, arts, business)? ")

    # Step 2: Parse transcript and save student data
    df_student = parse_transcript(pdf_path)
    print("\n✅ Transcript parsed successfully.")
    print(df_student.head())

    # Step 3: Filter catalog by interest
    interests = get_student_interests()
    print(f"\nYou selected: {', '.join([i.title() for i in interests])}")
    
    # Filter courses based on interests
    print("\nFiltering courses based on your interests...")
    filtered_courses = filter_courses_by_interest(interests)
    
    # Save filtered courses
    with open("filtered_courses.txt", "w") as f:
        f.write("\n".join(filtered_courses))
    
    print(f"Found {len(filtered_courses)} courses matching your interests.")

    # Step 4: Get AI recommendations
    print("\n🤖 Generating personalized elective recommendations...\n")
    recommendations = get_ai_recommendations(df_student, filtered_courses)
    print(recommendations)
