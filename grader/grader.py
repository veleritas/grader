# last updated 2014-12-03 toby

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





mimsofgid = dict()
mimsofcui = dict()
	
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

	shutil.copy("genes.txt", debugdir)

def printIDs():
	# print the geneID of each MIM
	out = open("geneID.txt", "w")
	for mim in geneID:
		out.write("mim " + mim + " geneID " + geneID[mim] + "\n")
	out.close()

	shutil.copy("geneID.txt", debugdir)

	# print the cui of each mim
	out = open("cui.txt", "w")
	for mim in CUI:
		out.write("mim " + mim + " cui " + CUI[mim] + "\n")
	out.close()

	shutil.copy("cui.txt", debugdir)

#-------------------------------------------------------------------------------

def parseMorbidmap():
	badDiseases = []
	with open("morbidmap") as morbidmap:
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
				
				# get the name with no mim
				result = re.search(r'.*, \d{6}', disease)
				if result == None:
					print "ERROR: bad formatting for the MIM number", mim
				else:
					name = result.group()
					name = name[:-8] # removes the ", mim" at the end
					
					# this gets overwritten a bunch!
					diseaseName[dmim] = name



def parseMIM2gene():
	nulls = [] # list of MIMs that are NULL
	with open("mim2gene_medgen") as mimfile:
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



def loadGeneRanking():
	# load the gene ranking into memory
	# ranking should already be in decreasing order of relevance
	with open("ranking.txt") as source:
		for line in source:
			line = line.rstrip('\n')
			gid, score = line.split()
			ranking.append([gid, float(score)])


def judgeScore(bestdisease):
	out = open("result.txt", "w")

	print "best disease", bestdisease

	gMIM = invert_dict(geneID) # gMIM[geneID] = the mim of geneID

	TP = 0
	TN = 0
	FP = 0
	FN = 0


	roc = open("roc.txt", "w")
	roc.write("FPR,TPR\n")

	threshold = 1.0
	precision = 0.001
	while threshold > 0:
		TP = 0
		TN = 0
		FP = 0
		FN = 0
		for curgeneID, score in ranking:
			if curgeneID in gMIM:
				val = gMIM[curgeneID]

				if score > threshold:
					if val in genes[bestdisease]:
						TP += 1
					else:
						FP += 1
				else:
					if val in genes[bestdisease]:
						FN += 1
					else:
						TN += 1
			else:
				# if this gene not even listed with a mim, it can't be associated with the disease at all
				# thus if we guess true, then is false positive, otherwise we guess false and it's a true negative
				if score > threshold:
					FP += 1
				else:
					TN += 1

		out.write("threshold " + str(threshold) + "\n")
		out.write("\tTP " + str(TP) + "\n")
		out.write("\tTN " + str(TN) + "\n")
		out.write("\tFP " + str(FP) + "\n")
		out.write("\tFN " + str(FN) + "\n")


		TPR = TP / (TP + FN)
		FPR = FP / (FP + TN)

		out.write("\tTPR, FPR " + str(TPR) + " " + str(FPR) + "\n")
		roc.write(str(FPR) + "," + str(TPR) + "\n")


		threshold -= precision


	roc.write("1,1\n")

	out.close()
	roc.close()

def preprocess():
	# where all the debug text files are stored
	if not os.path.exists(debugdir):
		os.makedirs(debugdir)

	parseMorbidmap()
	parseMIM2gene()

	printGenes()
#	printIDs()



	return





	
	
	global CUItoMIM
	CUItoMIM = invert_dict(CUI)
	
#	out = open("lol.txt", "w")	
#	for cui in CUItoMIM:
#		out.write(cui + " " + str(len(CUItoMIM[cui])) + "\n")
#	out.close()
	
	out = open("lol2.txt", "w")	
	for mim in CUI:
		out.write(mim + " " + str(len(CUI[mim])) + "\n")
	out.close()
	
	
	print "gene id length", len(geneID)
	lol = invert_dict(geneID)
	lol2 = invert_dict_nonunique(geneID)
	
	print "lol length", len(lol)
	print "lol2 length", len(lol2)
	
	
	
	
	
	print "len", len(CUItoMIM)
	print len(CUI)

def work():
	loadGeneRanking()

	# find the disease with the most genes involved
	biggest = -1
	bestdisease = ""
	for disease in genes:
		size = len(genes[disease])
		if size > biggest:
			biggest = size
			bestdisease = disease

	# should be mim 125853, insulin resistance
	print "the disease with the most genes is", bestdisease
	judgeScore(bestdisease)

def grade(cui):
	# takes one disease cui and outputs the TRP and FPR
	
	# check that this cui exists in morbidmap
	if not (cui in CUItoMIM):
		return False
	
	
	
	return True


def main():
	preprocess()
	return
	
	place = "/home/toby/grader/disgenet/testset.txt"
	with open(place) as testset:
		for line in testset:
			line = line.rstrip('\n')
			
			if grade(line):
				print "graded"
			else:
				print "ERROR unable to grade"

main()
