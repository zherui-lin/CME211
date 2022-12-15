import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import sys

# check command line parameters
if len(sys.argv) < 3:
    print('Usage:')
    print('    python3 postprocess.py <input file> <solution file>')
    sys.exit(0)

# extract command line parameters
input_file = sys.argv[1]
soln_file = sys.argv[2]

# read input variables
with open(input_file, 'r') as f:
    l, w, h = (float(s) for s in f.readline().strip().split())
    tc, th = (float(s) for s in f.readline().strip().split())
nrows = int(w / h) + 1
ncols = int(l / h) + 1

# read solution file and calculate mean temperature
temp = np.loadtxt(soln_file, dtype=np.float64).reshape(nrows, ncols)
mean = np.mean(temp)

# generate pseuducolor plot
x = np.arange(0., l + h, h)
y = np.arange(w, 0 - h, -h)
X, Y = np.meshgrid(x, y)
plt.pcolor(X, Y, temp, vmin=tc, vmax=th)
plt.colorbar()

# calculate mean temperature isoline by interpolation and plot it
mean_isoline = np.zeros(ncols)
for i in range(ncols):
    mean_isoline[i] = scipy.interpolate.interp1d(temp[:,i], y)(mean)
plt.plot(x, mean_isoline, 'k-')

# modify scales and save plot as png
plt.axis('equal')
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
plt.savefig("{}.png".format(soln_file[:-4]))

# print out input file info and mean temperature to indicate success
print("Input file processed: {}".format(input_file))
print("Mean Temperature: {:.5f}".format(mean))
