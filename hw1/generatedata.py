#--codequality_0
#--Please make sure you put the imports in lexicographical order :).
#--START
import sys, random
#--END

# check command line arguments
if (len(sys.argv) < 6):
	print("Usage:")
	print("  $ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file")
	sys.exit()

# extract command line arguments
ref_length = int(sys.argv[1])
nreads = int(sys.argv[2])
read_len = int(sys.argv[3])
ref_file = sys.argv[4]
reads_file = sys.argv[5]

# define base options
bases = ("A", "T", "C", "G")

# generate reference
ref = ""
for i in range(int(ref_length * 0.75)):
	ref += bases[random.randint(0,3)]
ref += ref[int(ref_length * 0.5) :] + "\n"

# write reference to file
with open(ref_file, "w") as f:
	f.write(ref)

#--codequality_0
#--Where are the comments here?? :'(
#--Please make sure you add some comments, e.g. before every for, if, elif, else
#--statements, which briefly mention what they do, e.g. mentioning the copying of
#--the reference string. Same in processdata.py!
#--END
# generate reads and count different types
reads = []
n_aligns = [0, 0, 0]
for i in range(nreads):
	rand = random.random()
	if rand < 0.75:
		start = random.randint(0, int(ref_length * 0.5) - 1)
		read = ref[start : start + read_len] + "\n"
		reads.append(read)
		n_aligns[1] += 1
	elif rand < 0.85:
		start = random.randint(int(ref_length * 0.75), int(ref_length - read_len))
		read = ref[start : start + read_len] + "\n"
		reads.append(read)
		n_aligns[2] += 1
	else:
		read = ""
		while ref.find(read) != -1:
			read = ""
			for j in range(read_len):
				read += bases[random.randint(0, 3)]
		read += "\n"
		reads.append(read)
		n_aligns[0] += 1

# write reads to file
with open(reads_file, "w") as f:
	f.writelines(reads)

# print information of reference and reads
print("reference length: {}".format(ref_length))
print("number reads: {}".format(nreads))
print("read length: {}".format(read_len))
for i in range(3):
	print("aligns {}: {:f}".format(i, n_aligns[i] / nreads))
