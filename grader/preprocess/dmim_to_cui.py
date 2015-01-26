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

def read_file(fname):
	with open(fname) as file:
		lines = [line.rstrip('\n') for line in file]

	return lines

def uniq_cui_of_dmim(dmim):
	print "dmim", dmim
	uids = dmim_to_uid(dmim)
	cuis = uid_to_cui(uids)
	return [cui for cui in cuis if re.match(r'^C\d{7}$', cui)]

def main():
	fname = "semmed.txt"
	dmims = read_file(fname)
	ans = map(uniq_cui_of_dmim, dmims)

#	uniq = []
#	for vals in ans:
#		for val in vals:
#			if val not in uniq:
#				uniq.append(val)
#
#	print "uniq", len(uniq)
#	total = 0
#	for vals in ans:
#		total += len(vals)
#	print "total", total

	print len(ans)
	print len(dmims)

	with open("out.txt", "w") as out:
		for dmim, cuis in zip(dmims, ans):
			out.write(dmim)
			for cui in cuis:
				out.write("|" + cui)
			out.write("\n")

#	debugdir = "/home/toby/grader/debug/"
#
#	ans = []
#	with open(debugdir + "tograde.txt") as file:
#		for dmim in file:
#			dmim = dmim.rstrip('\n')
#
#			print "dmim", dmim
#			uids = dmim_to_uid(dmim)
#			cuis = uid_to_cui(uids)
#			print "cuis", cuis
#
#			for cui in cuis:
#				if re.match(r'^C\d{7}$', cui):
#					if not (cui in ans):
#						ans.append(cui)
#
#	print "size", len(ans)
#	place = "/home/toby/grader/data/"
#	with open(place + "testset.txt", "w") as out:
#		for cui in ans:
#			out.write(cui + "\n")

if __name__ == "__main__":
	main()
