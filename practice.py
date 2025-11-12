import re
import pdfplumber

courses = []

# Open and read PDF
with pdfplumber.open("capilano_unofficial_transcript.pdf") as pdf:
    print("Inside with statement")
    for page in pdf.pages:
        print("Inside first for loop")
        text = page.extract_text()
        # print(text)
        for line in text.splitlines():
            # print("Inside second for loop")
            # Regex for lines with course info
            # Regex ignores transfer credit
            match = re.match(r"^([A-Z]{2,4}\s\d{3})\s+(.+?)\s+([A-Z]{1,3}[+-]?)\s+(\d\.\d{3})\s+(\d+\.\d{2})$", line)
            print("match", match)
            if match:
                course_num = match.group(1)
                course_name = match.group(2).strip()
                grade = match.group(3)
                courses.append((course_num, course_name, grade))

for c in courses:
    print(c)



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

