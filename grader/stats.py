from __future__ import division
import os

inloc = "/home/toby/grader/curves/summary/"

fnames = os.listdir(inloc)

for fname in fnames:
	aucs = []
	with open(inloc + fname) as infile:
		for line in infile:
			line = line.rstrip('\n')

			aucs.append(float(line))

	print fname
	total = sum(aucs)
	print "total", total
	print "average auc", total / len(aucs)



