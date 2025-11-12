# #!/bin/bash

# #Step 1: curl all information from Capilano website

# if [ -z "$1" ]; then
# 	echo "Please enter a course code"

# fi

# course_code="$1"

# echo -n "">final.txt

# #Step 2: Accept course code and grep for that course code ($1) throughout file
# #CourseNumArray=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/" | grep "$course_code-[0-9][0-9][0-9]" | awk -F/ '{print $4}' | awk -F- '{print $1 "-" $2}')

# CourseFullName=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/" | grep "$course_code-[0-9][0-9][0-9]" | awk -F/ '{print $4}')

# #DescriptionArray=()
# #for course_num in $CourseNumArray
# #do
# #echo $course_num
# #done

# # Retrieve all course codes and run this in a loop 


# #Step 3: Retrieve courses description
# for course in $CourseFullName
# do
# 	course_num=$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course" | grep -o "$course_code-[0-9][0-9][0-9]")
# 	description=$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course/" | grep '<meta name="coursedescription"' | awk -F'"' '{print $4}')
# #$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course/" | grep -i "<p>.*</p>" | sed "s/\(<p>\|<\/p>\)//g" | awk -F'<strong>' '{print $1}' | tail +6 | head -n +1 | sed -E "s/\t//g")
# 	(echo -e "$course_num\t $description\n")>>final.txt
# 	#DescriptionArray+=$Placeholder
# done


# cat final.txt
# #echo $DescriptionArray
# #Step 4: Output a tab seperated document with course code and courses description

# #echo $DescriptionArray
# #for c in $DescriptionArray
# #do
# #echo $c
# #done

# #for i in $CourseNumArray
# #do
# #course_name=$(grep -i "$course_code-[0-9][0-9][0-9]")
# #echo "$CourseNumArray[i]: $DescriptionArray[i]"
# #done


#!/bin/bash

# List of course codes (add more as needed)
course_codes=("actr" "asas" "bbio" "bchm" "bcmp" "beng" "bfps" "benf" "bmaf" "bgeo" "bhst" "bmth" "bphy" "bpsy" "bsci" "bsoc" "advr" "anim" "anar" "anth" "aba" "ahis" "aem" "astr" "bpac" "becp" "biol" "badm" "bcpt" "bues" "bfin" "bmkt" "btec" "csff" "caps" "cacc" "cace" "cacl" "cacf" "cacm" "caco" "cacs" "cact" "cdco" "cden" "cdma" "cecp" "chem" "chin" "cine" "cmns" "clsc" "comp" "cond" "cost" "crim" "dsgn" "digi" "dep" "docs" "educ" "econ" "edcp" "ea" "eea" "apsc" "engl" "eal" "esl" "eap" "eas" "ensm" "elct" "enso" "fdsc" "fins" "film" "fnst" "fnlg" "fys" "fren" "gate" "geog" "glbs" "grdf" "hca" "hist" "hkin" "idf" "idst" "ibus" "ixd" "ints" "inma" "ivpa" "japn" "ensj" "jazz" "kine" "sds" "lgst" "law" "lbst" "eldf" "ling" "padm" "math" "mopa" "mus" "mt" "muth" "nabu" "rec" "phil" "phys" "pol" "ppmi" "pmip" "pmi" "pmti" "psyc" "radp" "rmcp" "sci" "sosc" "soc" "span" "stat" "saab" "saba" "sacm" "saec" "sahu" "said" "sajs" "sals" "sala" "samp" "sass" "sato" "tect" "txtl" "thtr" "inst" "tour" "uof" "ussd" "uss" "visn" "ides" "vfx" "wlp" "wgst" "wmpi")

# Clear output file
> final.txt

for course_code in "${course_codes[@]}"; do
    echo "========== Processing $course_code =========="

    # Step 1: Fetch all course slugs for this course code
    CourseFullName=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/" \
        | grep "$course_code-[0-9][0-9][0-9]" \
        | awk -F/ '{print $4}')

    echo "[DEBUG] CourseFullName results for $course_code:"
    echo "$CourseFullName"

    # Step 2: Loop through each course page
    for course in $CourseFullName; do
        echo "[DEBUG] Checking course slug: $course"

        course_num=$(echo "$course" | grep -o "$course_code-[0-9][0-9][0-9]")
        echo "[DEBUG] Extracted course_num: $course_num"

        description=$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course/" \
            | grep '<meta name="coursedescription"' \
            | awk -F'"' '{print $4}')

        echo "[DEBUG] Extracted description for $course_num: $description"

        # Append results to file if not empty
        if [[ -n "$course_num" && -n "$description" ]]; then
            echo -e "$course_num\t$description" >> final.txt
        else
            echo "[WARNING] Missing data for $course"
        fi
    done
done

echo "========== Script Finished =========="
echo "Final output in final.txt:"
cat final.txt

