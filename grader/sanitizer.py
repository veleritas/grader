# sanitizes the stupid redundant output of disgennet
def main():
	lines = 0

	previous = 10000.2

	out = open("ranking.txt", "w")
	with open("diabetesGenes.txt") as file:
		for line in file:
			line = line.rstrip('\n')

			if lines == 0:
				lines = 1
				continue

			values = line.split('\t')
			# spit out the geneID and score only

			b = float(values[18])


			if b > previous:
				print "ERROR: not strictly decreasing"
				print b - previous
			else:
				previous = b


			out.write(values[8] + " " + values[18] + "\n")
			lines += 1

	print "num lines", lines
	out.close()

main()
