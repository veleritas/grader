#!/bin/bash

# last updated 2014-12-04 toby

file="mim2gene_medgen"

echo "Starting to update $file"

./ftpGENE.exp $file

#./ftpGENE.exp $file

if [ -e "$file" ]; then
	echo "Successfully got $file"

	newname=$file
	newname+=".txt"

	mv $file $newname
	mv $newname ~/grader/data
else
	echo "Could not get $file from GENE server"
fi

echo "Finished"
