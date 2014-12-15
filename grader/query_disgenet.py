# last updated  2014-12-12 toby

# this program takes a list of CUIs
# checks that they have the correct format
# querys disgenet for the genes associated with that CUI
# and outputs the result into a text file

import os
import sys
import urllib2

from util import is_cui
from util import move_and_replace

directory = "/home/toby/grader/data/rawdisgenet/"

def make_query(CUI):
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

#---don't touch anything above this line!---------------------------------------

	with open(CUI + ".txt", "w") as out:
		out.write(res.read())

	move_and_replace(CUI + ".txt", directory)

def main():
	if not os.path.exists(directory):
		os.makedirs(directory)

	assert len(sys.argv) == 2, "did not pass a file name to grabber"
	fname = sys.argv[1]
	place = "/home/toby/grader/data/"
	with open(place + fname) as testset:
		for cui in testset:
			cui = cui.rstrip('\n')
			assert is_cui(cui), "CUI was incorrectly formatted"
			print "Querying " + cui
			make_query(cui)

	print "Done"

main()
