# last updated 2014-12-15 toby
import re
import urllib2

def query(url):
#	TODO: add error checking
	BASE = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	response = urllib2.urlopen(BASE + url)
	html = response.read()
	return html

def uid_to_cui(uid):
	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query(req)

	if re.search(r'cannot get document summary', xml) is not None:
		raise Exception("uid not found")

	res = re.findall(r'<ConceptId>C\w\d{6}</ConceptId>', xml)
	assert len(res) == 1, "too many cuis for uid " + uid
	return res[0][11:-12]

def cui_to_uid(cui):
	req = "esearch.fcgi?db=medgen&term=" + cui
	xml = query(req)

	if re.search(r'No items found.', xml) is not None:
		return ""

	res = re.findall(r'<Id>\d+</Id>', xml)
	res = [uid[4:-5] for uid in res]

	if len(res) == 1: # most cases
		return res[0]

#	sometimes the search returns two or more uids for some reason
#	eg C0745103 (gives uids of 152875 and 5688)
#	but only one gives the correct cui when you do a summary
#	so i guess i'll take care of it and then email ncbi..

	truths = 0
	ans = ""
	for uid in res:
		if uid_to_cui(uid) == cui:
			truths += 1
			ans = uid

	assert truths == 1, "too much truth"
	return ans

def uid_to_dmim(uid):
	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query(req)
	res = re.findall(r'&lt;MIM&gt;\d{6}&lt;/MIM&gt;', xml)
	return [dmim[11:-12] for dmim in res]

def cui_to_dmim(cui):
	uid = cui_to_uid(cui)
	if not uid:
		return []

	return uid_to_dmim(uid)

if __name__ == "__main__":
	with open("/home/toby/grader/data/tobytestset.txt") as file:
		for line in file:
			line = line.rstrip('\n')
			print line
			dmim = cui_to_dmim(line)
			print "dmim", dmim
