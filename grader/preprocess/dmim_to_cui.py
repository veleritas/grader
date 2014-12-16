# last updated 2014-12-16 toby
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

def main():
	debugdir = "/home/toby/grader/debug/"

	ans = []
	with open(debugdir + "tograde.txt") as file:
		for dmim in file:
			dmim = dmim.rstrip('\n')

			print "dmim", dmim
			uids = dmim_to_uid(dmim)
			cuis = uid_to_cui(uids)
			print "cuis", cuis

			for cui in cuis:
				if re.match(r'^C\d{7}$', cui):
					if not (cui in ans):
						ans.append(cui)

	print "size", len(ans)
	place = "/home/toby/grader/data/"
	with open(place + "testset.txt", "w") as out:
		for cui in ans:
			out.write(cui + "\n")

if __name__ == "__main__":
	main()
