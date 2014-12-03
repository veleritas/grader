# first version 2014-12-03 toby
# last updated  2014-12-03 toby

# sanitizes the output of disgennet

import utilities
import os
import sys
import shutil

rawsource = "/home/toby/grader/disgenet/raw/"
outloc = "/home/toby/grader/disgenet/good/"

def cleanup(cui):
	curline = 0
	prevscore = 10000.0
	out = open("good" + cui + ".txt", "w")

	with open(rawsource + cui + ".txt") as thefile:
		for line in thefile:
			line = line.rstrip('\n')
			
			if curline == 0:
				curline = 1
				continue

			values = line.split('\t')

			if len(values) != 30:
				print "ERROR: not 30 columns in the file!!!"

			score = float(values[18])
			if score > prevscore:
				print "ERROR: not strictly decreasing"
			else:
				prevscore = score
				
			out.write(values[8] + " " + values[18] + "\n")
			curline += 1

	out.close()

	if curline == 1:
		print "the disease", cui, "did not have any data returned by disgenent"

	shutil.move("good" + cui + ".txt", outloc)

def main():
	if not os.path.exists(rawsource):
		print "ERROR: can't process disgenet data because directory doesn't exist"
		return


	if not os.path.exists(outloc):
		os.makedirs(outloc)

	with open("testset.txt") as testset:
		for cui in testset:
			cui = cui.rstrip('\n')
			cleanup(cui)

	print "Done"

main()
