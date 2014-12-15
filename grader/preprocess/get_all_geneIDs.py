# last updated 2014-12-12 toby
# return a dict of all gmim to geneID mappings
def get_all_geneIDs():
	bad_genes = []
	gmim_to_geneID = dict()
	place = "/home/toby/grader/data/mim2gene.txt"
	with open(place) as file:
		for line in file:
			line = line.rstrip('\n')
			vals = line.split('\t')
			assert len(vals) == 4, "too many columns in mim2gene"

#			five types for vals[1]:
#			predominantly phenotypes, gene, phenotype, gene/phenotype, moved/removed
			if vals[1] in ["gene", "gene/phenotype"]:
				if vals[2] == "-":
					bad_genes.append(vals[0])
				else:
#					each gmim only has one single geneID
					gmim_to_geneID[vals[0]] = vals[2]
#					but a single geneID can have multiple gmims!

	return gmim_to_geneID

if __name__ == "__main__":
	gmim_to_geneID = get_all_geneIDs()
	gmims = sorted(list(gmim_to_geneID))
	place = "/home/toby/grader/debug/gmim_to_geneID.txt"
	with open(place, "w") as out:
		for gmim in gmims:
			out.write("#" + gmim + "|" + gmim_to_geneID[gmim] + "\n")
