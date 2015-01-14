#!/bin/bash
# last updated 2015-01-13 toby

files=('morbidmap' 'mim2gene.txt')

echo "Updating: ${files[@]}"

./ftpOMIM.exp ${files[@]}

for fname in "${files[@]}"; do
	newname=$fname
	if [[ $fname != *".txt" ]]; then
		newname+=".txt"
	fi

	if [ -e "$fname" ]; then
		echo "Successfully got $fname"
		mv $fname ~/grader/data/$newname
	else
		echo "Could not get $fname from OMIM server."
	fi
done

echo "Done."
