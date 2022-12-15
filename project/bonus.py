import glob
import matplotlib
matplotlib.use('Agg')
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import sys

# check command line parameters
if len(sys.argv) < 3:
    print('Usage:')
    print('    python3 bonus.py <input file> <solution prefix>')
    sys.exit(0)

# extract command line parameters
input_file = sys.argv[1]
soln_prefix = sys.argv[2]

# read input variables
with open(input_file, 'r') as f:
    l, w, h = (float(s) for s in f.readline().strip().split())
    tc, th = (float(s) for s in f.readline().strip().split())

# generate grid coordinates and meshgrids
nrows = int(w / h) + 1
ncols = int(l / h) + 1
x = np.arange(0., l + h, h)
y = np.arange(w, 0 - h, -h)
X, Y = np.meshgrid(x, y)

# look up valid solution files with given prefix and sort them
soln_files = glob.glob(soln_prefix + '*')
soln_files = list(filter(lambda s: s[len(soln_prefix):-4].isnumeric() and s[-4:] == ".txt", soln_files))
soln_files.sort()

# generate pseudocolor plots and animation
fig = plt.figure()
plots = []
for soln_file in soln_files:
    temp = np.loadtxt(soln_file, dtype=np.float64).reshape(nrows, ncols)
    plots.append((plt.pcolor(X, Y, temp, vmin=tc, vmax=th),))
anm = animation.ArtistAnimation(fig, plots, interval=300, repeat_delay=1000, blit=True)

# modify colorbar and scales, and save animation as gif
plt.colorbar()
plt.axis('equal')
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
anm.save("{}.gif".format(soln_prefix))

# print out input file info to indicate success
print("Input file processed: {}".format(input_file))
