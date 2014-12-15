#!/bin/bash

# last updated 2014-12-12 toby

# this puts everything together...

echo "Starting everything..."

echo "Updating OMIM"
cd updater
./updateOMIM.sh
cd ..
echo "Finished updating OMIM"

echo "Querying disgenet"
python query_disgenet.py testset.txt
echo "Finished querying disgenet"

echo "Sanitizing disgenet"
python disgenet_sanitizer.py
echo "Done sanitizing disgenet"

echo "Running grader"
python grader.py
echo "Done grading"

echo "Plotting graphs"
Rscript plotROC.R
echo "Finished plotting ROC curves"

echo "Completely done!"
