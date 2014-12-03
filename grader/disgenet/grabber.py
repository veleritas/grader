# first version 2014-12-02 toby
# last updated  2014-12-03 toby

# this program takes a list of CUIs
# checks that they have the correct format
# querys disgenet for the genes associated with that CUI
# and outputs the result into a text file

import urllib2
import re
import os
import sys
import shutil

import utilities

def makeQuery(CUI):
	query="""
DEFINE
	c0='/data/gene_disease_score_onexus',
	c1='/data/diseases',
	c2='/data/genes',
	c3='/data/sources'
ON
	'http://bitbucket.org/janis_pi/disgenet_onexus.git'
SELECT
	c1 (cui, name, cui, name, diseaseClassName, STY, cui, name),
	c2 (geneId, name, geneId, name, uniprotId, description, pathName, pantherName, geneId, name),
	c0 (score, diseaseId, score, geneId, score, diseaseId, geneId, score, diseaseId, geneId, score, pmids)
FROM
	c0
WHERE
	(
		c1 = 'umls:""" + CUI + """'
	AND
		c3 = 'ALL'
	)
ORDER BY
	c0.score DESC"""

	req = urllib2.Request("http://www.disgenet.org/oql")
	res = urllib2.urlopen(req, query)

#----------------------------------------------------------------------
	# don't touch anything above this line!

	out = open(CUI + ".txt", "w")
	out.write(res.read())
	out.close()

	# move it to the raw data directory
	directory = "/home/toby/grader/disgenet/raw/"
	shutil.move(CUI + ".txt", directory) 

def main():
	# where to put the raw disgenet data
	directory = "/home/toby/grader/disgenet/raw/"
	if not os.path.exists(directory):
		os.makedirs(directory)

	with open("testset.txt") as testset:
		for cui in testset:
			cui = cui.rstrip('\n')

			if utilities.isCUI(cui):
				print "Querying " + cui
				makeQuery(cui)
			else:
				print "ERROR: CUI " + cui + " was incorrectly formatted"

	print "Done"	

main()
