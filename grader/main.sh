#!/bin/bash

# last updated 2014-12-16 toby

# this puts everything together...

echo "Starting everything..."

echo "Updating OMIM"
cd updater
./updateOMIM.sh
cd ..
echo "Finished updating OMIM"

echo "Querying disgenet"
cd grabbers/disgenet
python query.py testset.txt
python sanitize.py
cd ..
echo "Finished querying disgenet"

echo "Querying biograph"
cd biograph
python query.py testset.txt
python sanitize.py
cd ..
echo "Finished querying biograph"

cd ..

echo "Running grader"
python grader.py
echo "Done grading"

echo "Plotting graphs"
Rscript plotROC.R
echo "Finished plotting ROC curves"

echo "Completely done!"
