import re
from convert import query

def dmim_to_uid(dmim):
	req = "esearch.fcgi?db=medgen&term=" + dmim + "[mim]"
	xml = query(req)

	if re.search(r'No items found.', xml) is not None:
		raise Exception("dmim does not exist in medgen")

	res = re.findall(r'<Id>\d+</Id>', xml)
	return [uid[4:-5] for uid in res]

def uid_to_cui(uids):
	req = "esummary.fcgi?db=medgen&id="
	for uid in uids:
		req += uid + ","

	xml = query(req)
	res = re.findall(r'<ConceptId>C\w\d{6}</ConceptId>', xml)
	assert len(res) == len(uids), "different lengths"
	return [cui[11:-12] for cui in res]

if __name__ == "__main__":
	with open("/home/toby/grader/debug/testset.txt", "w") as out:
		with open("/home/toby/grader/debug/tograde.txt") as file:
			for dmim in file:
				dmim = dmim.rstrip('\n')

				print "dmim", dmim
				uids = dmim_to_uid(dmim)
				cuis = uid_to_cui(uids)
				print "cuis", cuis

				for cui in cuis:
					if re.match(r'^C\d{7}$', cui):
						out.write(cui + "\n")
