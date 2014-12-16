# first version 2014-12-03 toby
# last updated  2014-12-15 toby

# sanitizes the output of disgenet

import os
import sys

rawsource = "/home/toby/grader/data/raw/disgenet/"
outloc = "/home/toby/grader/data/input/disgenet/"

def parse_ranking(cui):
	lines = 0
	prevscore = 10000.0
	with open(outloc + cui + ".txt", "w") as out:
		with open(rawsource + cui + ".txt") as file:
			for line in file:
				if lines == 0:
					lines = 1
					continue

				vals = line.split('\t')
				assert len(vals) == 30, "too many columns"

				score = float(vals[18])
				assert score <= prevscore, "not descending order"
				prevscore = score

				out.write(vals[8] + " " + vals[18] + "\n")


def main():
	if not os.path.exists(rawsource):
		raise Exception("input directory does not exist")

	if not os.path.exists(outloc):
		os.makedirs(outloc)

	# process each file in the directory, not from the text file
	files = os.listdir(rawsource)
	for fname in files:
		parse_ranking(fname[:-4])

	print "Done"

main()
