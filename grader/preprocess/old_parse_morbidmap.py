# last updated 2015-01-15 toby
import os
import re

def parse_morbidmap():
#	returns genes[dmim] = [gmim, gmim, gmim...]
#	gives the list of gene mim numbers known to cause each disease mim number

	bad_diseases = [] # diseases without a dmim
	genes = dict() # all unique gmims assosicated with dmim

	morbidmap_location = "/home/toby/grader/data/morbidmap.txt"
	with open(morbidmap_location) as morbidmap:
		for line in morbidmap:
			line = line.rstrip('\n')

			disease, gene, gmim, locus = line.split("|")

			result = re.search(r'\d{6}', disease) # disease has MIM?
			if result is None:
				bad_diseases.append(disease)
			else:
				dmim = result.group()
				if not (dmim in genes):
					genes[dmim] = []

				if not (gmim in genes[dmim]):
					genes[dmim].append(gmim)

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
