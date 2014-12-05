#!/bin/bash

# last updated 2014-12-04 toby

# this puts everything together...
# lets hope it works!

echo "Starting everything..."

echo "Updating mim2gene"
cd updater
./updateGene.sh
echo "Finished updating mim2gene"

echo "Updating OMIM"
./updateOMIM.sh
cd ..
echo "Finished updating OMIM"


echo "Running grabber"
cd disgenet
python grabber.py
echo "Finished grabber"

echo "Running sanitizer"
python sanitizer.py
cd ..
echo "Done sanitizing"


echo "Running grader"
python grader.py
echo "Done grading"

echo "Plotting graphs"
Rscript plotAll.R
echo "Finished plotting ROC curves"

echo "Completely done!"
