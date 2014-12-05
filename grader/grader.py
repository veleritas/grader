# last updated 2014-12-04 toby

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

ranking = [] # the ranking of genes in descending order

debugdir = "/home/toby/grader/debug/"

mimsofgid = dict() # mimsofgid[gid] = list of mims that gid is known by
mimsofcui = dict() # mimsofcui[cui] = list of mims that cui is known by

#-------------------------------------------------------------------------------

def invert_dict(d):
    return dict([(v, k) for k, v in d.iteritems()])
    
def moveAndReplace(file, dest):
	# if file exists at destination, deletes file
	# then moves file to destination
	if os.path.exists(dest + file):
		os.remove(dest + file)

	shutil.move(file, dest)

#-------------------------------------------------------------------------------

# print all genes associated with a disease
def printGenes():
	out = open("genes.txt", "w")
	for disease in genes:
		out.write("disease id " + disease + "\n")
		out.write("name of disease " + diseaseName[disease] + "\n")
		for mim in genes[disease]:
			out.write("\t" + mim + "\n")
		out.write("\n")
	out.close()

	moveAndReplace("genes.txt", debugdir)

def printIDs():
	# print the geneID of each MIM
	out = open("geneID.txt", "w")
	for mim in geneID:
		out.write("mim " + mim + " geneID " + geneID[mim] + "\n")
	out.close()

	moveAndReplace("geneID.txt", debugdir)

	# print the cui of each mim
	out = open("cui.txt", "w")
	for mim in CUI:
		out.write("mim " + mim + "\n")
		for cui in CUI[mim]:
			out.write("\t" + cui + "\n")
	out.close()

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
					if not (vals[0] in CUI):
						CUI[vals[0]] = []
					
					CUI[vals[0]].append(vals[4])
				
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
	
	ans = open(outloc + cui + ".txt", "w") # the list for R to process
	ans.write("FPR,TPR\n")
	
	gMIM = invert_dict(geneID) # gMIM[geneID] = the mim of geneID
	
	threshold = 1.0
	precision = 0.001
	lastTPR = -1.0
	lastFPR = -1.0
	
	while threshold > 0:
		TP = 0
		TN = 0
		FP = 0
		FN = 0
		
		for curgeneID, score in ranking:
			if curgeneID in gMIM:
				curgmim = gMIM[curgeneID]
				
				if curgmim in trueHits:
					if score > threshold:
						TP += 1
					else:
						FN += 1
				else:
					if score > threshold:
						FP += 1
					else:
						TN += 1
					
			else:
				# can't check if in morbidmap or not
				if score > threshold:
					FP += 1
				else:
					TN += 1
					
		TPR = TP / (TP + FN)
		FPR = FP / (FP + TN)
		
		if (TPR != lastTPR) or (FPR != lastFPR):
			ans.write(str(FPR) + "," + str(TPR) + "\n")
			
		lastTPR = TPR
		lastFPR = FPR
	
		threshold -= precision
		
	ans.write("1,1\n")
	ans.close()

#-------------------------------------------------------------------------------

def preprocess():
	# where all the debug text files are stored
	if not os.path.exists(debugdir):
		os.makedirs(debugdir)


	rocloc = "/home/toby/grader/roc/"
	if not os.path.exists(rocloc):
		os.makedirs(rocloc)

	parseMorbidmap()
	parseMIM2gene()

	printGenes()
	printIDs()

def canGrade(cui):
	with open("check.txt", "a") as out:
		out.write("cui " + cui + "\n")

		if not (cui in mimsofcui):
			out.write("\tnot in mim2gene_medgen\n")
			return False

		out.write("dmims associated with cui:\n")
		for dmim in mimsofcui[cui]:
			out.write("\t" + dmim + "\n")

		for dmim in mimsofcui[cui]:
			if dmim in genes:
				return True

		# cui is indexed by mim2gene_medgen, but the mims are not in morbidmap
		out.write("\tcan't find mims in morbidmap\n")
		return False

def getGeneRanking(cui):
	ranking = []
	place = "/home/toby/grader/data/input/"
	with open(place + cui + ".txt") as source:
		for line in source:
			line = line.rstrip('\n')
			gid, score = line.split()
			ranking.append([gid, float(score)])

	return ranking

def grade(cui):
	# takes one disease cui and outputs the TRP and FPR

	ranking = getGeneRanking(cui)
#	combine all the genes associated with all the dmims together into one big list
	trueHits = []
	for dmim in mimsofcui[cui]:
		if dmim in genes:
			trueHits += genes[dmim]
			
	evaluate(cui, ranking, trueHits)

def main():
	preprocess()

	if os.path.exists("/home/toby/grader/check.txt"):
		os.remove("/home/toby/grader/check.txt")

	place = "/home/toby/grader/disgenet/testset.txt"
	with open(place) as testset:
		for line in testset:
			line = line.rstrip('\n')
			
			if canGrade(line):
				grade(line)
			else:
				print "ERROR: cannot grade " + line

main()
