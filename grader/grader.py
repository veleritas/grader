# last updated 2015-01-09 toby

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

def evaluate(cui, ranking, true_hits, ofile):
	with open(ofile, "w") as out:
		out.write("class,score\n")
		for geneID, score in ranking:
			if geneID in true_hits:
				out.write("1,")
			else:
				out.write("0,")

			out.write(score + "\n")

#-------------------------------------------------------------------------------

def preprocess():
	debug.print_IDs(gmim_to_geneID)

def can_grade(cui):
	dmims = convert.cui_to_dmim(cui)
	for dmim in dmims:
		if dmim in genes:
			return dmims

	return []

def get_gene_ranking(ifile):
	ranking = []
	with open(ifile) as source:
		for line in source:
			line = line.rstrip('\n')
			gid, score = line.split()
			ranking.append([gid, score])

	return ranking

def prepare(cui, dmims, inloc, ofile):
	ranking = get_gene_ranking(inloc)

	true_hits = []
	for dmim in dmims:
		if dmim in genes:
			true_hits += [gmim_to_geneID[gmim] for gmim in genes[dmim] if gmim in gmim_to_geneID]

	evaluate(cui, ranking, true_hits, ofile)


def main():
	start = "/home/toby/grader/data/input/"
	outloc = "/home/toby/grader/data/roc/"

	subdirs = []
	for root, dirs, files in os.walk(start):
		if root == start:
			subdirs += dirs
			break

	for subdir in subdirs:
		util.make_dir(os.path.join(outloc, subdir))

		files = os.listdir(start + subdir)
		for fname in files:
			inloc = os.path.join(start, subdir, fname)
			ofile = os.path.join(outloc, subdir, fname)

			cui = fname[:-4]
			dmims = can_grade(cui)
			if util.is_cui(cui) and dmims:
				print "Grading", subdir, cui
				prepare(cui, dmims, inloc, ofile)
			else:
				print "Can't grade", subdir, cui

if __name__ == "__main__":
	preprocess()
	main()
