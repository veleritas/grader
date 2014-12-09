import urllib2
import re
import time

htmllen = []
single = 0
multiple = 0

CUIsofdmim = dict()

def query(dmim):
	req = "http://www.ncbi.nlm.nih.gov/medgen/?term=" + dmim + "%5Bmim%5D"

	print "requesting", dmim

	response = urllib2.urlopen(req)
	html = response.read()

	place = "/home/toby/test/html/"
	with open(place + dmim + ".txt", "w") as out:
		out.write(html)

	return html

def readAllDmims():
	ans = []
	with open("alldmims.txt") as file:
		for dmim in file:
			dmim = dmim.rstrip('\n')
			ans.append(dmim)

	return ans

def findCUIs(html):
	# returns a list of CUIs found in this html file
	htmllen.append(len(html))

	ans = re.findall(r'result_count', html)
	assert len(ans) <= 1, "more than one result count"

	if len(ans) == 1:
		# multiple CUIs associated with this dmim
		print "multiple CUIs"
		global multiple
		multiple += 1

		results = re.findall(r'result_count">Results: \d+<', html)
		assert len(results) == 1

		N = re.findall(r'\d+', results[0])
		N = int(N[0]) # number of CUIs associated with dmim

#		find the CUIs listed as hits
		cuis = re.findall(r'<dd>C\w\d{6}', html)

		assert N == len(cuis)

		ans = []
		for cui in cuis:
			ans.append(cui[4: ])

		return ans
	else:
		res = re.search(r'class="warn icon"', html)
		if res:
			print "doesn't exist"
			return []
		else:
			# len(ans) == 0
			# we got the full report for this dmim
			res = re.findall(r'<div class="MedGenTitleText".*medgenTable', html)
			assert len(res) == 1, "more than one medgentitletext"

			print res

			cui = re.findall(r'C\w\d{6}', res[0])
			print cui

			assert len(cui) == 1

			print "single CUI"
			global single
			single += 1

			return cui
	
def main():
	alldmims = readAllDmims()

	for i, dmim in enumerate(alldmims):
		print "test case #", i
		
		html = query(dmim)
		cuis = findCUIs(html)

		CUIsofdmim[dmim] = cuis

		with open("CUIsofdmim.txt", "a") as out:
			out.write("disease " + dmim + "\n")
			for cui in cuis:
				out.write("\t" + cui + "\n")


		print ""




	print ""
	print ""
	print "size of alldmims", len(alldmims)
	print "tested dmims:", N
	print "single cui", single
	print "multiple cuis", multiple


	print "average # of html chars", sum(htmllen) / len(htmllen)

#	with open("CUIsofdmim.txt", "w") as out:
#		for dmim in CUIsofdmim:
#			out.write("disease " + dmim + "\n")
#			for cui in CUIsofdmim[dmim]:
#				out.write("\t" + cui + "\n")



start_time = time.time()
main()
print "total runtime:", time.time() - start_time, " seconds"
