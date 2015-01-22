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

def uid_to_cui(uid):
#	converts one uid to one cui
#	there is only one cui for each uid

	req = "esummary.fcgi?db=medgen&id=" + uid
	xml = query_ncbi(req)

	if re.search(r'cannot get document summary', xml) is not None:
		raise Exception("UID {0} does not exist!".format(uid))

	res = re.findall(r'<ConceptId>C\w\d{6}</ConceptId>', xml)
	assert len(res) == 1, "More than one CUI for UID {0}".format(uid)
	return res[0][11:-12]


def cui_to_uid(cui):
	req = "esearch.fcgi?db=medgen&term=" + cui + "[conceptid]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		raise Exception("No UID exists for {0}".format(cui))

	res = re.findall(r'<Id>\d+</Id>', xml)

	assert len(res) == 1, "More than one UID for {0}".format(cui)
#	uids = [uid[4:-5] for uid in res]


	return res[0][4:-5]

#	return uids[0]



#	there should only be one UID for each CUI
	if len(uids) == 1:
		return uids[0]

#	but, some CUIs return multiple UIDs for some reason...
#	eg C0745103 gives UIDs of 152875 and 5688
#	but the CUI of 5688 is C0020445

#	to to get around this we find the UID of each CUI again
#	and see which gives the correct one to one mapping

	cuis = map(uid_to_cui, uids)
	assert cuis.count(cui) == 1, "UID to CUI {0} is not unique!".format(cui)
	return uids[cuis.index(cui)]

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
#		raise Exception("DMIM {0} does not exist in MedGen.".format(dmim))

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

	assert len(cuis) == len(set(cuis)), "repeating cuis for dmim {0}".format(dmim)
	return cuis

def cui_to_dmim(cui):
#	one cui to many dmim
#	gives empty list if cui and uid exist but no dmim exists

	uid = cui_to_uid(cui)
	return uid_to_dmim(uid)

#-------------------------------------------------------------------------------

#error in gene database:
#gmim 603072 gives two results using eutils: geneids: 6790 and 8465

#6790 gives the correct mapping, but searching for 8465 in gene gives nothing
#if you use esummary, then it gives 8465 for id but "currentid" is 6790

#..... stupid database


def gmim_to_geneID(gmim):
#	converts a gene MIM into a gene ID (should be 1 to 1)
	req = "esearch.fcgi?db=gene&term=" + gmim + "[mim]"
	xml = query_ncbi(req)

	if re.search(r'No items found.', xml) is not None:
		print "Gene MIM {0} has no gene ID.".format(gmim)
		return []

#		raise Exception("Gene MIM {0} has no gene ID.".format(gmim))

	res = re.findall(r'<Id>\d+</Id>', xml)
#	assert len(res) == 1, "Gene MIM {0} has multiple gene IDs.".format(gmim)
	return [gene_id[4:-5] for gene_id in res]

#-------------------------------------------------------------------------------

def main():

	print cui_to_uid(sys.argv[1])
	return




	print "hi"
#	print gmim_to_geneID('612374')
	print dmim_to_cui('615962')
#	print gmim_to_geneID(sys.argv[1])

if __name__ == "__main__":
	main()
