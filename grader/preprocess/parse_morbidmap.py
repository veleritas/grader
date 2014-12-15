# last updated 2014-12-12 toby
import re

def parse_morbidmap():
	bad_diseases = [] # diseases without a dmim
	genes = dict() # all unique gmims assosicated with dmim
	place = "/home/toby/grader/data/morbidmap.txt"
	with open(place) as morbidmap:
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

if __name__ == "__main__":
	genes = parse_morbidmap()
	dmims = sorted(list(genes))
	place = "/home/toby/grader/debug/sorted_morbidmap.txt"
	with open(place, "w") as out:
		for dmim in dmims:
			out.write("#" + dmim)
			for gmim in genes[dmim]:
				out.write("|" + gmim)
			out.write("\n")


	ans = [0 for x in range(30)]
	for dmim in dmims:
		ans[len(genes[dmim])] += 1

	with open("/home/toby/grader/debug/tograde.txt", "w") as out:
		for dmim in dmims:
			if len(genes[dmim]) >= 5:
				out.write(dmim + "\n")

	print ans
