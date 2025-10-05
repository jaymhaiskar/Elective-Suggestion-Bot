"# Elective-Suggestion-Bot" 

Reccomendations: Download your unofficial transcript from your MyCapU acc and upload it here, if you have a scanned copy of a transcript from your previous uni/seconday school, please make sure the text is "grabable". For ex, open the pdf in Adobe Acrobat, then try to grab the text, if you can't this bot won't work. If you can grab the text, copy and paste it into a notepad to ensure the text can be reforamtted.


Journey mapping:
- started w/ Lake Washington High School Trasncript.
- then uploaded official capilano transcript, didn't work because the scanned pdf had a png inside, therefore no text extraction form pdf.
- downloaded unofficial CapU transcript and text was grabable. 
- regex doesn't take into account transfer credit due to different formatting
ex) Transferred: Subject, Course Title, Grade, Credit Hours, Quality Points (CMNS 152 Business Communications Basics TC+ 3.000 0.00)
    Non Transferred: Subject, Course, Level, Title, Grade  (BIOL 109 01 Introductory Biology B-)


List of course codes for extract_courses.sh :
ACTR, ASAS, BBIO, BCHM, BCMP, BENG, BFPS, BENF, BMAF, BGEO, BHST, BMTH, BPHY, BPSY, BSCI, BSOC, ADVR, ANIM, ANAR, ANTH, ABA, AHIS, AEM, ASTR, BPAC, BECP, BIOL, BADM, BCPT, BUES, BFIN, BMKT, BTEC, CSFF, CAPS, CACC, CACE, CACL, CACF, CACM, CACO, CACS, CACT, CDCO, CDEN, CDMA, CECP, CHEM, CHIN, CINE, CMNS, CLSC, COMP, COND, COST, CRIM, DSGN, DIGI, DEP, DOCS, EDUC, ECON, EDCP, EA, EEA, APSC, ENGL, EAL, ESL, EAP, EAS, ENSM, ELCT, ENSO, FDSC, FINS, FILM, FNST, FNLG, FYS, FREN, GATE, GEOG, GLBS, GRDF, HCA, HIST, HKIN, IDF, IDST, IBUS, IXD, INTS, INMA, IVPA, JAPN, ENSJ, JAZZ, KINE, SDS, LGST, LAW, LBST, ELDF, LING, PADM, MATH, MOPA, MUS, MT, MUTH, NABU, REC, PHIL, PHYS, POL, PPMI, PMIP, PMI, PMTI, PSYC, RADP, RMCP, SCI, SOSC, SOC, SPAN, STAT, SAAB, SABA, SACM, SAEC, SAHU, SAID, SAJS, SALS, SALA, SAMP, SASS, SATO, TECT, TXTL, THTR, INST, TOUR, UOF, USSD, USS, VISN, IDES, VFX, WLP, WGST, WMPI


Structure for students database:
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gpa REAL
);

MAKE EDIT TO TABLE
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    recommended_gpa REAL,
);


Questions for Jason

in the save_to_db function I get the error: c.execute("INSERT INTO students (id, name, gpa) VALUES (?,?)", (student_id, student_name, gpa))
sqlite3.OperationalError: 2 values for 3 columns

discuss table structure w/ Jason
- students
- courses

data cleaning for course code and course description extracted"
&rsquo; &#8208; &quot; &reg; &ndash; &eacute; &amp; &mdash; s&#601;&#787;lil&#787;w&#601;t/  &iacute; 
&uacute; &aacute; &egrave; &lsquo; &ograve; &rdquo; &ldquo;

Asked AI to give recommended gpa for each course
Course codes starting with 1 (e.g., actr-100, asas-110) → very low GPAs like 1.8–2.1. 
Course codes starting with 2 (e.g., actr-200, asas-210) → still low, but slightly higher, 2.0–2.3. 
Course codes starting with 3 → 2.4–2.7. 
Course codes starting with 4 → 2.5–3.0. 
Course codes starting with 5+ → 2.8–3.5.

