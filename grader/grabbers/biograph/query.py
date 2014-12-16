# last updated 2014-12-16 toby
import os
import re
import sys
import urllib2

# TODO: make this parallel, because biograph servers are too slow...



outloc = "/home/toby/grader/data/raw/biograph/"

token = "cMRF2PHmSsm8sXbPywVX"

def query(url):
	try:
		response = urllib2.urlopen(url)
		html = response.read()
	except urllib2.HTTPError, error:
		html = error.read()

	return html

def rank_genes(cui):
	req = "http://www.biograph.be/concept/tsv/" + cui
	req += "?filter_directness=Known+and+inferred&filter_type=Gene"

	html = query(req)

	with open(outloc + cui + ".txt", "w") as out:
		out.write(html)


def exists(cui):
	req = "http://www.biograph.be/api/info?id=" + cui + "&auth=" + token
	html = query(req)

	with open(cui + ".txt", "w") as out:
		out.write(html)

	return re.search(r'<error>', html) is None

def main(fname):
	if not os.path.exists(outloc):
		os.makedirs(outloc)

	place = "/home/toby/grader/data/"
	with open(place + fname) as testset:
		for cui in testset:
			cui = cui.rstrip('\n')
			print "Querying", cui

			if exists(cui):
				print "cui", cui, "can be graded"
				rank_genes(cui)
			else:
				print "can't grade", cui
				with open(outloc + cui + ".txt", "w") as out:
					out.write("")

if __name__ == "__main__":
	assert len(sys.argv) == 2, "didn't pass a file name"
	fname = sys.argv[1]
	main(fname)
