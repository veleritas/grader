import re


diseases = dict() # a list of all the diseases associated with a certain geneMIM
genes = dict() # a list of all the genes associated with a certain diseaseMIM (some diseases don't have MIMs)
diseaseName = dict() # the name of each disease
geneID = dict() # geneID[mim] is the geneID associated with mim
CUI = dict() # CUI[mim] is the medgen concept unique identifier associated with mim


def printthings():
	out = open("out.txt", "w")
	
	for mim in diseases:
		out.write(mim + "\n")
		
		for val in diseases[mim]:
			out.write("\t" + val + "\n")
			
		out.write("\n")
	
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


def finprint():
	print("size of diseases", len(diseases))
	print("size of genes", len(genes))
	
	out = open("genes.txt", "w")
	for disease in genes:
		out.write("disease id " + disease + "\n")
		out.write("name of disease " + diseaseName[disease] + "\n")
		for mim in genes[disease]:
			out.write("\t" + mim + "\n")
		out.write("\n")
		
	out.close()


def preprocess():
	parseMorbidmap()
	parseMIM2gene()
	printthings()
	
def main():
	preprocess()
	finprint()

main()
