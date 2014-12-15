# first version 2014-12-03 toby
# last updated  2014-12-12 toby

# sanitizes the output of disgennet

import os
import sys
import shutil

from util import move_and_replace

rawsource = "/home/toby/grader/data/rawdisgenet/"
outloc = "/home/toby/grader/data/input/"

def cleanup(cui):
	lines = 0
	prevscore = 10000.0
	with open(cui + ".txt", "w") as out:
		with open(rawsource + cui + ".txt") as thefile:
			for line in thefile:
				line = line.rstrip('\n')
				lines += 1

				if lines == 1:
					continue

				values = line.split('\t')
				assert len(values) == 30, "ERROR: not exactly 30 columns in file"

				score = float(values[18])
				assert score <= prevscore, "ERROR: not strictly decreasing"
				prevscore = score

				out.write(values[8] + " " + values[18] + "\n")

	if lines == 1:
		print "disgenet returned no data for", cui
		os.remove(cui + ".txt")
	else:
		move_and_replace(cui + ".txt", outloc)

def main():
	if not os.path.exists(rawsource):
		raise Exception("input directory does not exist")

	if not os.path.exists(outloc):
		os.makedirs(outloc)

	# process each file in the directory, not from the text file
	files = os.listdir(rawsource)
	for fname in files:
		cleanup(fname[:-4])

	print "Done"

main()
