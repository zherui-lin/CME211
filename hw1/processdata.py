import sys, time

# check command line arguments
if(len(sys.argv) < 4):
	print("Usage:")
	print("  $ python3 processdata.py <ref_file> <reads_file> <align_file>")
	sys.exit()

# extract command line arguments
reference_file = sys.argv[1]
reads_file = sys.argv[2]
align_file = sys.argv[3]

# read reference from file
ref = ""
with open(reference_file, "r") as f:
	ref = f.read().strip()
ref_length = len(ref)

# read reads from file
reads = []
with open(reads_file, "r") as f:
	reads = [line.strip() for line in f.readlines() if line.strip() != ""]
nreads = len(reads)
read_len = len(reads[0])

# record starting time
start_time = time.time()

# perfrom alignment and count different types
aligns = []
n_aligns = [0, 0, 0]
for read in reads:
	start = []
	first = ref.find(read)
	start.append(first)
	if first != -1:
		second = ref.find(read, first + 1)
		if second != -1:
			start.append(second)
			n_aligns[2] += 1
		else:
			n_aligns[1] += 1
	else:
		n_aligns[0] += 1
	for s in start:
		read += " {}".format(s)
	read += "\n"
	aligns.append(read)

# record ending time
end_time = time.time()

# write alignments to file
with open(align_file, "w") as f:
	f.writelines(aligns)

# print information of reference, reads, alignments and elapsed time
print("reference length: {}".format(ref_length))
print("number reads: {}".format(nreads))
for i in range(3):
	print("aligns {}: {:2f}".format(i, n_aligns[i] / nreads))
print("elapsed time: {:6f}".format(end_time - start_time))

#--documentation_0
#--Great design and pretty good code quality. The comments could have been a little
#--more here and there (see previous comment), and ensure they add context, but in general
#--you've done a great job! Keep up the good work!! :))
#--END