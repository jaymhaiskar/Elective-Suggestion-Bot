# #!/bin/bashu

# # List of course codes (add more as needed)
# course_codes=("actr" "asas" "bbio" "bchm" "bcmp" "beng" "bfps" "benf" "bmaf" "bgeo" "bhst" "bmth" "bphy" "bpsy" "bsci" "bsoc" "advr" "anim" "anar" "anth" "aba" "ahis" "aem" "astr" "bpac" "becp" "biol" "badm" "bcpt" "bues" "bfin" "bmkt" "btec" "csff" "caps" "cacc" "cace" "cacl" "cacf" "cacm" "caco" "cacs" "cact" "cdco" "cden" "cdma" "cecp" "chem" "chin" "cine" "cmns" "clsc" "comp" "cond" "cost" "crim" "dsgn" "digi" "dep" "docs" "educ" "econ" "edcp" "ea" "eea" "apsc" "engl" "eal" "esl" "eap" "eas" "ensm" "elct" "enso" "fdsc" "fins" "film" "fnst" "fnlg" "fys" "fren" "gate" "geog" "glbs" "grdf" "hca" "hist" "hkin" "idf" "idst" "ibus" "ixd" "ints" "inma" "ivpa" "japn" "ensj" "jazz" "kine" "sds" "lgst" "law" "lbst" "eldf" "ling" "padm" "math" "mopa" "mus" "mt" "muth" "nabu" "rec" "phil" "phys" "pol" "ppmi" "pmip" "pmi" "pmti" "psyc" "radp" "rmcp" "sci" "sosc" "soc" "span" "stat" "saab" "saba" "sacm" "saec" "sahu" "said" "sajs" "sals" "sala" "samp" "sass" "sato" "tect" "txtl" "thtr" "inst" "tour" "uof" "ussd" "uss" "visn" "ides" "vfx" "wlp" "wgst" "wmpi")

# # Clear output file
# > final.txt

# for course_code in "${course_codes[@]}"; do
#     echo "========== Processing $course_code =========="

#     # Step 1: Fetch all course slugs for this course code
#     CourseFullName=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/" \
#         | grep "$course_code-[0-9][0-9][0-9]" \
#         | awk -F/ '{print $4}')

#     echo "[DEBUG] CourseFullName results for $course_code:"
#     echo "$CourseFullName"

#     # Step 2: Loop through each course page
#     for course in $CourseFullName; do
#         echo "[DEBUG] Checking course slug: $course"

#         course_num=$(echo "$course" | grep -o "$course_code-[0-9][0-9][0-9]")
#         echo "[DEBUG] Extracted course_num: $course_num"

#         description=$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course/" \
#             | grep '<meta name="coursedescription"' \
#             | awk -F'"' '{print $4}')

#         echo "[DEBUG] Extracted description for $course_num: $description"

#         # Append results to file if not empty
#         if [[ -n "$course_num" && -n "$description" ]]; then
#             echo -e "$course_num\t$description" >> final.txt
#         else
#             echo "[WARNING] Missing data for $course"
#         fi
#     done
# done

# echo "========== Script Finished =========="
# echo "Final output in final.txt:"
# cat final.txt


# CourseTitle=$(curl -s "https://www.capilanou.ca/programs--courses/courses/chin-200---intermediate-chinese-language-and-culture-i/" | grep -oP '(?<=-\s).*?(?=</h1>)')
# echo "$CourseTitle"


# Prerequisites=$(curl -s "https://www.capilanou.ca/programs--courses/courses/ensm-200---choir-ensemble-iii/" | grep -oP '(?<=<p><strong>Prerequisites</strong></p><p>).*?(?=</p>)')
# echo "$Prerequisites"



#!/bin/bash

# Add all prefixes you want here
course_codes=("actr" "asas" "bbio" "bchm" "bcmp" "beng" "bfps" "benf" "bmaf" "bgeo" "bhst" "bmth" "bphy" "bpsy" "bsci" "bsoc" "advr" "anim" "anar" "anth" "aba" "ahis" "aem" "astr" "bpac" "becp" "biol" "badm" "bcpt" "bues" "bfin" "bmkt" "btec" "csff" "caps" "cacc" "cace" "cacl" "cacf" "cacm" "caco" "cacs" "cact" "cdco" "cden" "cdma" "cecp" "chem" "chin" "cine" "cmns" "clsc" "comp" "cond" "cost" "crim" "dsgn" "digi" "dep" "docs" "educ" "econ" "edcp" "ea" "eea" "apsc" "engl" "eal" "esl" "eap" "eas" "ensm" "elct" "enso" "fdsc" "fins" "film" "fnst" "fnlg" "fys" "fren" "gate" "geog" "glbs" "grdf" "hca" "hist" "hkin" "idf" "idst" "ibus" "ixd" "ints" "inma" "ivpa" "japn" "ensj" "jazz" "kine" "sds" "lgst" "law" "lbst" "eldf" "ling" "padm" "math" "mopa" "mus" "mt" "muth" "nabu" "rec" "phil" "phys" "pol" "ppmi" "pmip" "pmi" "pmti" "psyc" "radp" "rmcp" "sci" "sosc" "soc" "span" "stat" "saab" "saba" "sacm" "saec" "sahu" "said" "sajs" "sals" "sala" "samp" "sass" "sato" "tect" "txtl" "thtr" "inst" "tour" "uof" "ussd" "uss" "visn" "ides" "vfx" "wlp" "wgst" "wmpi")

output="final.txt"
> "$output"

base_page=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/")

for code in "${course_codes[@]}"; do
    echo "Processing $code..."
    slugs=$(echo "$base_page" | grep "$code-[0-9][0-9][0-9]" | awk -F/ '{print $4}' | sort -u)
    # echo "$slugs"

    for slug in $slugs; do
        url="https://www.capilanou.ca/programs--courses/courses/$slug/"
        echo "$slug"
        html=$(curl -A "Mozilla/5.0" -s "$url")

        # --- Extract course title ---
        CourseTitle=$(echo "$html" | grep -oP '(?<=-\s).*?(?=</h1>)')

        # --- Extract prerequisites ---
        Prerequisites=$(echo "$html" | grep -oP '(?<=<p><strong>Prerequisites</strong></p><p>).*?(?=</p>)')

        # Only write if we found a title
        if [[ -n "$CourseTitle" ]]; then
            echo "${slug^^}|$CourseTitle|$Prerequisites" >> "$output"
        fi

        # Be polite to the server
        sleep 0.3
    done
done

echo "Done. Results saved to $output"