# last updated 2014-12-08 toby

from __future__ import division
import re
import six
import os
import sys
import shutil

#-------------------------------------------------------------------------------

# genes[dMIM] = all the geneMIMs associated with a dMIM
# some diseases have no MIMs
genes = dict()

# diseaseName[MIM] = name of the disease given by MIM
diseaseName = dict()

geneID = dict() # geneID[mim] = the geneID associated with mim

CUI = dict() # CUI[mim] is the medgen concept unique identifier of mim
CUItoMIM = dict() # CUItoMIM[CUI] = the MIM associated with this CUI

debugdir = "/home/toby/grader/debug/"

mimsofgid = dict() # mimsofgid[gid] = list of mims that gid is known by
mimsofcui = dict() # mimsofcui[cui] = list of mims that cui is known by

#-------------------------------------------------------------------------------

def invert_dict(d):
    return dict([(v, k) for k, v in d.iteritems()])
    
def moveAndReplace(file, dest):
	if os.path.exists(dest + file):
		os.remove(dest + file)

	shutil.move(file, dest)

#-------------------------------------------------------------------------------

# print all genes associated with a disease
def printGenes():
	with open("genes.txt", "w") as out:
		for disease in genes:
			out.write("disease mim " + disease + "\n")
			out.write("name of disease " + diseaseName[disease] + "\n")
			for gmim in genes[disease]:
				out.write("\t" + gmim + "\n")
			out.write("\n")

	moveAndReplace("genes.txt", debugdir)

def printIDs():
	# print the geneID of each MIM
	with open("geneID.txt", "w") as out:
		for gmim in geneID:
			out.write("gmim " + gmim + " geneID " + geneID[gmim] + "\n")

	moveAndReplace("geneID.txt", debugdir)

	# print the cui of each mim
	with open("cui.txt", "w") as out:
		for mim in CUI:
			out.write("mim " + mim + "\n")
			out.write("\t" + CUI[mim] + "\n")


	moveAndReplace("cui.txt", debugdir)

#-------------------------------------------------------------------------------

def parseMorbidmap():
	badDiseases = []
	place = "/home/toby/grader/data/morbidmap.txt"
	with open(place) as morbidmap:
		for line in morbidmap:
			line = line.rstrip('\n')

			disease, gene, geneMIM, locus = line.split("|")

			result = re.search(r'\d{6}', disease) # disease has MIM?
			if result == None:
				badDiseases.append(disease)
			else:
				dmim = result.group()
				if not (dmim in genes):
					genes[dmim] = []
					
				genes[dmim].append(geneMIM)
				
				# verbatim what morbidmap says the disease name is
				# includes the mim too
				diseaseName[dmim] = disease
				

def parseMIM2gene():
	nulls = [] # list of MIMs that are NULL
	place = "/home/toby/grader/data/mim2gene_medgen.txt"
	with open(place) as mimfile:
		for line in mimfile:
			line = line.rstrip('\n')
			
			# mim, geneID, gene/pheno, <ignore>, CUI
			vals = line.split('\t')
			
			assert len(vals) == 5, "mim2gene has too many columns"

			if vals[2] == "gene":
				if vals[1] != "-":
					geneID[vals[0]] = vals[1] # one to one
					
					if not (vals[1] in mimsofgid):
						mimsofgid[vals[1]] = []
						
					mimsofgid[vals[1]].append(vals[0])
				else:
					print "ERROR: no geneID for MIM #" + vals[0]
			elif vals[2] == "phenotype":
				if vals[4] != "-":
					# should be one unique CUI for each disease MIM				
					if not (vals[0] in CUI):
						CUI[vals[0]] = vals[4]
					else:
						assert CUI[vals[0]] == vals[4], "different CUIs!"
				
					if not (vals[4] in mimsofcui):
						mimsofcui[vals[4]] = []
					
					if not (vals[0] in mimsofcui[vals[4]]):
						mimsofcui[vals[4]].append(vals[0])
				else:
					print "ERROR: no MedGen Concept ID for", vals[0]
			else:
				nulls.append(vals[0])

#-------------------------------------------------------------------------------

def evaluate(cui, ranking, trueHits):
	outloc = "/home/toby/grader/roc/"
	with open(outloc + cui + ".txt", "w") as ans:
		ans.write("class,score\n")

		gMIM = invert_dict(geneID)
		for curgeneID, score in ranking:
			if (curgeneID in gMIM) and (gMIM[curgeneID] in trueHits):
				ans.write("1,")
			else:
				ans.write("0,")

			ans.write(score + "\n")

#-------------------------------------------------------------------------------

def preprocess():
	# where all the debug text files are stored
	if not os.path.exists(debugdir):
		os.makedirs(debugdir)

	rocloc = "/home/toby/grader/roc/"
	if not os.path.exists(rocloc):
		os.makedirs(rocloc)

	parseMorbidmap()

	with open("alldmims.txt", "w") as out:
		for dmim in genes:
			out.write(dmim + "\n")




	parseMIM2gene()

	printGenes()
	printIDs()

def canGrade(cui):
	if not (cui in mimsofcui):
		return False

	for dmim in mimsofcui[cui]:
		if dmim in genes:
			return True

	# cui is indexed by mim2gene_medgen, but the mims are not in morbidmap
	return False

def getGeneRanking(cui):
	ranking = []
	place = "/home/toby/grader/data/input/"
	with open(place + cui + ".txt") as source:
		for line in source:
			line = line.rstrip('\n')
			gid, score = line.split()
			ranking.append([gid, score])

	return ranking

def grade(cui):
	ranking = getGeneRanking(cui)
#	combine all the genes associated with all the dmims together into one big list
	trueHits = []
	for dmim in mimsofcui[cui]:
		if dmim in genes:
			trueHits += genes[dmim]
			
	evaluate(cui, ranking, trueHits)

def main():
	preprocess()

	place = "/home/toby/grader/data/input/"
	for filename in os.listdir(place):
		cui = filename[:-4]

		if canGrade(cui):
			print "Graded", cui
			grade(cui)
		else:
			print "ERROR: cannot grade " + cui

main()
