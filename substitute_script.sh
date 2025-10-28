#!/bin/bash

sorted_list=$(awk -F'|' -v OFS="|" '{print $1, $3, $4}' final.txt)




echo "$sorted_list" >> final.txt