def parse_genes():
	name_to_geneID = dict()
	place = "/home/toby/grader/data/mim2gene.txt"
	with open(place) as file:
		for line in file:
			line = line.rstrip('\n')
			vals = line.split('\t')
			assert len(vals) == 4

			if vals[1] in ["gene", "gene/phenotype"]:
				if vals[2] != "-" and vals[3] != "-": # has name and geneID
					if not (vals[3] in name_to_geneID):
						name_to_geneID[vals[3]] = vals[2]
					else:
						assert vals[2] == name_to_geneID[vals[3]]

	return name_to_geneID

