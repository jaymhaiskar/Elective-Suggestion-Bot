import re
import pdfplumber
import pandas as pd
import sqlite3
from openai import OpenAI

# Global Variable
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

def parse_transcript(pdf_path):
    # Example regex for course: "COMP 101 - Intro to CS A"
    courses = []
# Open and read PDF
    with pdfplumber.open(pdf_path) as pdf:
        # print("Inside with statement")
        for page in pdf.pages:
            # print("Inside first for loop")
            text = page.extract_text()
            # print(text)
            for line in text.splitlines():
                # print(line)
                # Regex for lines with course info, ignores transfer credit
                match = re.match(r"^([A-Z]{2,4}\s\d{3})\s+(.+?)\s+([A-Z]{1,3}[+-]?)\s+(\d\.\d{3})\s+(\d+\.\d{2})$", line)
                # print("match", match)
                if match:
                    course_num = match.group(1)
                    course_name = match.group(2).strip()
                    grade = match.group(3)
                    courses.append((course_num, course_name, grade))
 

    df= pd.DataFrame(courses, columns=["course_code", "course_name", "letter_grade"])

    df["gpa_points"] = df["letter_grade"].map(grade_scale)
    return df

df = parse_transcript("capilano_unofficial_transcript.pdf")

student_json = df.to_json(orient="records", indent=2)
with open("student_courses.json", "w") as f:
    f.write(student_json)


client = OpenAI(api_key="")

# Upload both files
course_file = client.files.create(file=open("final.txt", "rb"), purpose="assistants")
student_file = client.files.create(file=open("student_courses.json", "rb"), purpose="assistants")

print("Files uploaded:", course_file.id, student_file.id)

response = client.chat.completions.create(
    model="gpt-5",  # or gpt-4-turbo if you’re using that
    messages=[
        {"role": "system", "content": "You are an AI academic advisor that recommends electives based on completed coursework and course catalog information."},
        {"role": "user", "content": (
            f"I’ve uploaded two files:\n"
            f"- {course_file}: contains all available course info.\n"
            f"- {student_file}: contains the student’s completed courses.\n\n"
            f"I grant you access to open these files, if uou still don't have it tell me what you need me to do to get the access"
            f"Based on this data, which electives would you recommend for the student? "
            f"Consider both academic performance and alignment with interest areas."
        )}
    ]
)

print(response.choices[0].message.content)


# import re
# from PyPDF2 import PdfReader

# courses = []

# # Open and read PDF
# reader = PdfReader("capilano_transcript.pdf")

# for page in reader.pages:
#     text = page.extract_text()
#     print(text)
#     if not text:
#         continue
#     for line in text.splitlines():
#         # Regex for: BIOL 301, Cell Biology, 3.70, A-
#         pattern = r"([A-Z]{2,4}\s?\d{3}),\s*([^,]+),\s*(\d\.\d{2}),\s*([A-F][+-]?)"
#         match = re.match(pattern, line)
#         if match:
#             course_code = match.group(1)
#             course_name = match.group(2).strip()
#             gpa = match.group(3)
#             grade = match.group(4)
#             courses.append((course_code, course_name, gpa, grade))

# # Print results
# for c in courses:
#     print(c)



#------------------------- Insert course code and description from final.txt into courses table -------------------
# df = pd.read_csv('final.txt', sep='\t', header=None, names=['course_code', 'course_description', 'recommended_gpa', 'NA'])

# df = df.drop(columns=['NA']) 
# print(df)

# conn = sqlite3.connect('students.db')
# df.to_sql('courses', conn, if_exists='replace', index=False)
# conn.close()






