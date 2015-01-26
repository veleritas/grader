# last updated 2015-01-21 toby

# uses NCBI's eutils to convert
# disease mims to concept unique identifiers (CUIs)
# and the reverse (CUI -> dmim)

# UID stands for MedGen unique identifier
# mim is OMIM identifier
# NCBI = National Center for Biotechnology Information

import re
import urllib2
import sys

def query_ncbi(url):
#	TODO: add error checking
	BASE = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
	response = urllib2.urlopen(BASE + url)
	return response.read()

#-------------------------------------------------------------------------------

def uid_to_cui(uid): # one uid to one cui
	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query_ncbi(req)

	if re.search(r'cannot get document summary', xml) is not None:
		raise Exception("UID {0} does not exist!".format(uid))

	res = re.findall(r'<ConceptId>C\w\d{6}</ConceptId>', xml)
	assert len(res) == 1, "More than one CUI for UID {0}".format(uid)
	return res[0][11:-12]

def cui_to_uid(cui): # one cui to one uid
	req = "esearch.fcgi?db=medgen&term=" + cui + "[conceptid]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		raise Exception("No UID exists for {0}".format(cui))

	res = re.findall(r'<Id>\d+</Id>', xml)
	assert len(res) == 1, "More than one UID for {0}".format(cui)
	return res[0][4:-5]

#-------------------------------------------------------------------------------

def uid_to_dmim(uid):
#	one uid to many dmim

	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query_ncbi(req)

	if re.search(r'cannot get document summary', xml) is not None:
		raise Exception("UID {0} does not exist!".format(uid))

	res = re.findall(r'&lt;MIM&gt;\d{6}&lt;/MIM&gt;', xml)
	return [dmim[11:-12] for dmim in res]

def dmim_to_uid(dmim):
#	one dmim to many uid
	req = "esearch.fcgi?db=medgen&term=" + dmim + "[mim]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		print "DMIM {0} does not exist in MedGen.".format(dmim)
		return []

	res = re.findall(r'<Id>\d+</Id>', xml)
	return [uid[4:-5] for uid in res]

#-------------------------------------------------------------------------------

def dmim_to_cui(dmim):
#	one dmim to many cui
#	returns CUIs starting with CN...

	uids = dmim_to_uid(dmim)
	if not uids:
		return []

	cuis = map(uid_to_cui, uids)
	return list(set(cuis)) # returns unique cuis

def cui_to_dmim(cui):
#	one cui to many dmim
#	gives empty list if cui and uid exist but no dmim exists

	uid = cui_to_uid(cui)
	return uid_to_dmim(uid)

#-------------------------------------------------------------------------------

# some gene ids are deprecated
# eg gmim 603072 gives 6790 and 8465
# but the 8465 is deprecated

def gmim_to_geneID(gmim):
#	converts a gene MIM into a gene ID (should be 1 to 1)
	req = "esearch.fcgi?db=gene&term=" + gmim + "[mim]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		print "Gene MIM {0} has no gene ID.".format(gmim)
		return []

#	TODO:
#	get only the current gene id
	res = re.findall(r'<Id>\d+</Id>', xml)
	return [gene_id[4:-5] for gene_id in res]

#-------------------------------------------------------------------------------

def main():
	print cui_to_dmim(sys.argv[1])

if __name__ == "__main__":
	main()
