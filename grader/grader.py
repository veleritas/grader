# last updated 2014-12-12 toby

import os

import util
import debug
from preprocess import convert
from preprocess.parse_morbidmap import parse_morbidmap
from preprocess.get_all_geneIDs import get_all_geneIDs

#-----------------------GLOBAL VARIABLES----------------------------------------

# genes[dMIM] = all the geneMIMs associated with a dMIM
# some diseases have no MIMs
genes = parse_morbidmap()

# gmim_to_geneID[gmim] = geneID of this gmim
gmim_to_geneID = get_all_geneIDs()

#-----------------------END GLOBAL VARIABLES------------------------------------

def evaluate(cui, ranking, true_hits):
	outloc = "/home/toby/grader/data/roc/"
	with open(outloc + cui + ".txt", "w") as out:
		out.write("class,score\n")
		for geneID, score in ranking:
			if geneID in true_hits:
				out.write("1,")
			else:
				out.write("0,")

			out.write(score + "\n")

#-------------------------------------------------------------------------------

def preprocess():
	rocloc = "/home/toby/grader/data/roc/"
	if not os.path.exists(rocloc):
		os.makedirs(rocloc)

	debug.print_genes(genes)
	debug.print_IDs(gmim_to_geneID)

def can_grade(cui):
	dmims = convert.cui_to_dmim(cui)
	for dmim in dmims:
		if dmim in genes:
			return dmims

	return []

def get_gene_ranking(cui):
	ranking = []
	place = "/home/toby/grader/data/input/"
	with open(place + cui + ".txt") as source:
		for line in source:
			line = line.rstrip('\n')
			gid, score = line.split()
			ranking.append([gid, score])

	return ranking

def prepare(cui, dmims):
	ranking = get_gene_ranking(cui)

	true_hits = []
	for dmim in dmims:
		if dmim in genes:
			true_hits += [gmim_to_geneID[gmim] for gmim in genes[dmim] if gmim in gmim_to_geneID]

	evaluate(cui, ranking, true_hits)

def main():
	place = "/home/toby/grader/data/input/"
	for filename in os.listdir(place):
		cui = filename[:-4]
		dmims = can_grade(cui)
		if util.is_cui(cui) and dmims:
			print "Graded", cui
			prepare(cui, dmims)
		else:
			print "ERROR: cannot grade " + cui

if __name__ == "__main__":
	preprocess()
	main()
