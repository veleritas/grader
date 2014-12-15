#!/bin/bash

# last updated 2014-12-12 toby

# grabs files from OMIM and moves it

file1="morbidmap"
file2="mim2gene.txt"

echo "Starting to update $file1 and $file2"

./ftpOMIM.exp $file1 $file2

if [ -e "$file1" ]; then
	echo "Successfully got $file1"

	newname=$file1
	newname+=".txt"

	mv $file1 $newname
	mv $newname ~/grader/data
else
	echo "Could not get $file1 from OMIM server"
fi

if [ -e "$file2" ]; then
	echo "Successfully got $file2"
	mv $file2 ~/grader/data
else
	echo "Could not get $file2 from OMIM server"
fi

echo "Finished"
