import sys
import truss

# check command line parameters
if len(sys.argv) < 3:
    print('Usage:')
    print('    python3 main.py [joints file] [beams file] [optional plot output file]')
    sys.exit(0)

joints = sys.argv[1]
beams = sys.argv[2]

# try to initialize truss object
try:
    t = truss.Truss(joints, beams)
except RuntimeError as e:
    print('ERROR: {}'.format(e))
    sys.exit(2)

# plot geometry if optional plot output file is given
if len(sys.argv) >= 4:
    t.PlotGeometry(sys.argv[3])

# print truss object representation
print(t)
