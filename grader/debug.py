# last updated 2015-01-09 toby
import os
from util import move_and_replace

debugdir = "/home/toby/grader/debug/"

def print_IDs(gmim_to_geneID):
	# print the geneID of each gmim
	with open("gmim_to_geneID.txt", "w") as out:
		for gmim, geneID in gmim_to_geneID.items():
			out.write("gmim " + gmim + " geneID " + geneID + "\n")

	move_and_replace("gmim_to_geneID.txt", debugdir)

if not os.path.exists(debugdir):
	os.makedirs(debugdir)
