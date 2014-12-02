#!/bin/bash

# 2014-12-02 toby
# this program grabs a file from the omim server
# and puts it into the grader directory

file="morbidmap"

echo "Starting to update $file"

./ftpOMIM.exp $file

if [ -e "$file" ]; then
	echo "Successfully got $file"
	mv $file ~/grader/data
else
	echo "Could not get $file from OMIM server"
fi

echo "Finished"
