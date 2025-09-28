#!/bin/bash

#Step 1: curl all information from Capilano website

if [ -z "$1" ]; then
	echo "Please enter a course code"

fi

course_code="$1"

echo -n "">final.txt

#Step 2: Accept course code and grep for that course code ($1) throughout file
#CourseNumArray=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/" | grep "$course_code-[0-9][0-9][0-9]" | awk -F/ '{print $4}' | awk -F- '{print $1 "-" $2}')

CourseFullName=$(curl -s "https://www.capilanou.ca/programs--courses/search--select/find-a-program-or-course/" | grep "$course_code-[0-9][0-9][0-9]" | awk -F/ '{print $4}')

#DescriptionArray=()
#for course_num in $CourseNumArray
#do
#echo $course_num
#done

# Retrieve all course codes and run this in a loop 


#Step 3: Retrieve courses description
for course in $CourseFullName
do
	course_num=$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course" | grep -o "$course_code-[0-9][0-9][0-9]")
	description=$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course/" | grep '<meta name="coursedescription"' | awk -F'"' '{print $4}')
#$(curl -s "https://www.capilanou.ca/programs--courses/courses/$course/" | grep -i "<p>.*</p>" | sed "s/\(<p>\|<\/p>\)//g" | awk -F'<strong>' '{print $1}' | tail +6 | head -n +1 | sed -E "s/\t//g")
	(echo -e "$course_num\t $description\n")>>final.txt
	#DescriptionArray+=$Placeholder
done


cat final.txt
#echo $DescriptionArray
#Step 4: Output a tab seperated document with course code and courses description

#echo $DescriptionArray
#for c in $DescriptionArray
#do
#echo $c
#done

#for i in $CourseNumArray
#do
#course_name=$(grep -i "$course_code-[0-9][0-9][0-9]")
#echo "$CourseNumArray[i]: $DescriptionArray[i]"
#done