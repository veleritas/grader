# last updated 2015-01-26 toby
import os
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
#	genes = parse_morbidmap()
#	ans = []
#	for key, val in genes.items():
#		if len(val) >= 10:
#			ans.append((key, len(val)))
#
#	ans = sorted(ans, key = lambda x: x[1], reverse = True)
#	with open("max_morbidmap.txt", "w") as out:
#		for dmim, num in ans:
#			out.write(dmim + "\n")
#
#	return


	debugdir = "/home/toby/grader/debug/"
	if not os.path.exists(debugdir):
		os.makedirs(debugdir)

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

#	generate testset
	names = [ [] for x in range(30)]
	for dmim in dmims:
		names[len(genes[dmim])].append(dmim)

	print "length of names"
	print [len(val) for val in names]

	min_genes = 9
	total = 0
	ans = []
	for i, val in enumerate(names):
		print "i", i, "len(val)", len(val)
		if i >= min_genes:
			ans += val

	with open(debugdir + "tograde.txt", "w") as out:
		for dmim in ans:
			out.write(dmim + "\n")

if __name__ == "__main__":
	main()
