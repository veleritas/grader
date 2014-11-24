import re

diseases = dict() # a list of all the diseases associated with a certain geneMIM
genes = dict() # a list of all the genes associated with a certain diseaseMIM (some diseases don't have MIMs)
diseaseName = dict() # the name of each disease

def printthings():
	out = open("out.txt", "w")
	
	for mim in diseases:
		out.write(mim + "\n")
		
		for val in diseases[mim]:
			out.write("\t" + val + "\n")
			
		out.write("\n")
	
	out.close()

def preprocess():
	numnone = 0
	
	lines = 0
	with open("morbidmap") as morbidmap:
		for line in morbidmap:
			# remove the single newline at the end
			line = line.rstrip('\n')

			# always four fields in each line:
			# disease name, gene name, gene MIM number, locus (don't care)
			disease, gene, geneMIM, locus = line.split("|")

			# for each unique mim, have a list of all the diseases it is associated with
			if not (geneMIM in diseases):
				diseases[geneMIM] = []
				
			diseases[geneMIM].append(disease)

			# check if this disease has a MIM number
			result = re.search(r'\d{6}', disease)
			if result == None:
				# nomim.append(disease)
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
					print "we got a problem", mim
					print disease
				else:
					name = result.group()
					name = name[:-8] # removes the ", mim" at the end (thus only disease name)
					

					diseaseName[mim] = name # the name of this disease
				
			
			lines += 1


			
	print("num with no mim for disease", numnone)
	
	# print all the diseases associated with one gene MIM
	printthings()
	
	print("total lines", lines)

	
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
	
		
	
def main():
	print("starting main")
	
	preprocess()
	finprint()
	print("end of main")

main()
