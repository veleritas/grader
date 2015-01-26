# last updated 2015-01-26 toby
import re

import sys
sys.path.append("/home/toby/useful_util/")
import util

from collections import defaultdict

def parse_morbidmap():
#	returns genes[dmim] = set(gmim, gmim, gmim...) to ensure uniqueness
#	gives the list of gene mim numbers known to cause each disease mim number

	genes = defaultdict(set) # all unique gmims assosicated with dmim

	mm_loc = "/home/toby/grader/data/"
	for line in util.read_file(mm_loc, "morbidmap.txt"):
		disease, gene, gmim, locus = line.split("|")
		result = re.search(r'\d{6}', disease)

#		some diseases are bad and have no disease mim identifier
		if result is not None:
			dmim = result.group()
			genes[dmim].add(gmim)

	return genes

#-------------------------------------------------------------------------------

def main():
	debugdir = "/home/toby/grader/debug/"
	util.make_dir(debugdir)

#	print sorted morbidmap
	genes = parse_morbidmap()
	dmims = sorted(list(genes))
	place = debugdir + "sorted_morbidmap.txt"
	with open(place, "w") as out:
		for dmim in dmims:
			out.write("#" + dmim)
			for gmim in genes[dmim]:
				out.write("|" + gmim)
			out.write("\n")

	names = defaultdict(set)
	for dmim, gmims in genes.items():
		names[len(gmims)].add(dmim)

	for i, dmims in names.items():
		print "i {0} len() {1}".format(i, len(dmims))

if __name__ == "__main__":
	main()
