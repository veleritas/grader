from __future__ import division
import re
import six

diseases = dict() # a list of all the diseases associated with a certain geneMIM
genes = dict() # a list of all the genes associated with a certain diseaseMIM (some diseases don't have MIMs)
diseaseName = dict() # the name of each disease
geneID = dict() # geneID[mim] is the geneID associated with mim
CUI = dict() # CUI[mim] is the medgen concept unique identifier associated with mim



ranking = [] # the ranking of genes in descending order

def invert_dict(d):
    return dict([(v, k) for k, v in d.iteritems()])

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

# print all diseases associated with a gene
def printDiseases():
	out = open("diseases.txt", "w")
	for mim in diseases:
		out.write("gene id " + mim + "\n")
		for val in diseases[mim]:
			out.write("\t" + val + "\n")
		out.write("\n")
	out.close()

def printIDs():
	# print the geneID of each MIM
	out = open("geneID.txt", "w")
	for mim in geneID:
		out.write("mim " + mim + " geneID " + geneID[mim] + "\n")
	out.close()

	# print the cui of each mim
	out = open("cui.txt", "w")
	for mim in CUI:
		out.write("mim " + mim + " cui " + CUI[mim] + "\n")
	out.close()


def parseMorbidmap():
	numnone = 0
	with open("morbidmap") as morbidmap:
		for line in morbidmap:
			line = line.rstrip('\n')

			disease, gene, geneMIM, locus = line.split("|")

			# for each unique mim, have a list of all the diseases it is associated with
			if not (geneMIM in diseases):
				diseases[geneMIM] = []
			diseases[geneMIM].append(disease)

			# check if this disease has a MIM number
			result = re.search(r'\d{6}', disease)
			if result == None:
				numnone += 1
			else:
				mim = result.group()
				if not (mim in genes):
					genes[mim] = []
				genes[mim].append(geneMIM)
				
				# get the name with no mim
				result = re.search(r'.*, \d{6}', disease)
				if result == None:
					# some of the entries ~10 have bad formatting (they are missing the comma)
					print "ERROR: bad formatting for the MIM number", mim
				else:
					name = result.group()
					name = name[:-8] # removes the ", mim" at the end (thus only disease name)
					
					
					diseaseName[mim] = name # the name of this disease
					# this will name it to the last instance of the disease
					# omim has multiple names for the same thing, so not sure how to choose



# generate the geneIDs and CUIs associated with a MIM
def parseMIM2gene():
	# if it's a gene, should have geneID (but some don't)
	# if it's a phenotype, then has C# and maybe geneID (could be CN#)
	numNulls = 0
	
	#MIM number	GeneID	type	Source	MedGenCUI
	with open("mim2gene_medgen") as mimfile:
		for line in mimfile:
			line = line.rstrip('\n')
			
			result = re.search(r'^\d{6}', line)
			if result:
				mim = result.group()
			else:
				print "ERROR: this line had no MIM"
			
			result = re.search(r'gene', line)
			if result:
				temp = re.search(r'\t\d+', line)
				if temp:
					gid = temp.group()
					gid = gid.strip('\t')
					geneID[mim] = gid
				else:
					print "ERROR: can't find geneID for mim #", mim # some weird case
			else:
				result = re.search(r'phenotype', line)
				if result:
					temp = re.search(r'C\w{7}', line)					
					if temp:
						cui = temp.group()
						CUI[mim] = cui
					else:
						print "ERROR: no MedGen Concept ID for phenotype", mim
				else:
					# the NULL field... not sure what to do here
					numNulls += 1


def loadGeneRanking():
	# load the gene ranking into memory
	# ranking should already be in decreasing order of relevance
	with open("ranking.txt") as source:
		for line in source:
			line = line.rstrip('\n')
			gid, score = line.split()
			ranking.append([gid, float(score)])

	# are the dicts built with strings or integers? can you use integers if the indexes are strings?

def isstring(s):
	if isinstance(s, six.string_types):
		return True
	else:
		return False

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
	parseMorbidmap()
	parseMIM2gene()
	
	loadGeneRanking()
	
	printGenes()
	printDiseases()
	printIDs()


def work():
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

def main():
	preprocess()
	work()

main()
