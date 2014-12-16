# last updated 2014-12-16 toby
import os
import sys

from parse_genes import parse_genes

name_to_geneID = parse_genes()

rawsource = "/home/toby/grader/data/raw/biograph/"
outloc = "/home/toby/grader/data/input/biograph/"

def get_name(raw):
	vals = raw.split(' ')
	if len(vals) == 2 and vals[1] == "gene":
		return vals[0]

	return ""

def sanitize(cui):
	with open(outloc + cui + ".txt", "w") as out:
		with open(rawsource + cui + ".txt") as file:
			for line in file:
				line = line.rstrip('\n')
				vals = line.split('\t')
				assert len(vals) == 6

				name = get_name(vals[2])
				if name and name in name_to_geneID:
					out.write(name_to_geneID[name] + " " + vals[5] + "\n")
				else:
					out.write("-1" + " " + vals[5] + "\n")

def main():
	if not os.path.exists(rawsource):
		raise Exception("no input directory")

	if not os.path.exists(outloc):
		os.makedirs(outloc)

	files = os.listdir(rawsource)
	for fname in files:
		sanitize(fname[:-4])

main()
