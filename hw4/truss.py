import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse
import scipy.sparse.linalg
import warnings
warnings.filterwarnings('error')

class Truss:
    '''
    A truss object is initialized by a joints file and a beams file respectively.
    The initialization method will process the data from both files. The string
    representation method will give the result of beam forces from computation.
    The PlotGeometry() method can plot the geometry of all beams.
    '''

    def __init__(self, joints_file, beams_file):
        '''
        The input joints file and the beams file are processed to calculate the beam
        force of each beam.
        '''

        self.handle_joints(joints_file)
        self.handle_beams(beams_file)
        self.generate_matrix()
        self.calculate_forces()


    def handle_joints(self, joints_file):
        '''
        Process data in the joints file. Id of each joint is recorded in a list, and 
        coordinates and external forces of each joint are stored in dicts mapping from 
        each joint id. Joints with zero displacement are also stored in another list.
        '''

        # initialize each data structure
        self.joint_ids = []
        self.joint_coords = {}
        self.joint_fxys = {}
        self.joint_zerodisps = []

        with open(joints_file, 'r') as f:
            # skip the first comment line
            f.readline()
            for line in f.readlines():
                # take each line as a list and store data in each data structure
                joint = line.strip().split()
                id, x, y, fx, fy, zerodisp = joint[0], joint[1], joint[2], joint[3], joint[4], joint[5]
                self.joint_ids.append(id)
                self.joint_coords[id] = (float(x), float(y))
                self.joint_fxys[id] = (float(fx), float(fy))
                # only take joint with zero displacement into the list
                if zerodisp == '1':
                    self.joint_zerodisps.append(id)
        
        # sort joint ids just in case
        self.joint_ids.sort()
        self.joint_zerodisps.sort()
        self.n_joints = len(self.joint_ids)
        self.n_zerodisps = len(self.joint_zerodisps)
    

    def handle_beams(self, beams_file):
        '''
        Process data in the beams file. Id of each beam is recorded in a list, and 
        two joints connected by each beam are stored in a dict mapping from each 
        beam id. For each joint, map it to a list of its connecting beams and the other 
        joint connected by each beam.
        '''

        # initialize each data structure
        self.beam_ids = []
        self.beam_joints = {}
        self.joints_beams_other = {}
        for j in self.joint_ids:
            self.joints_beams_other[j] = {}
        
        with open(beams_file, 'r') as f:
            f.readline()
            for line in f.readlines():
                # take each line as a list and store data in each data structure
                beam = line.strip().split()
                id, j1, j2 = beam[0], beam[1], beam[2]
                self.beam_ids.append(id)
                self.beam_joints[id] = (j1, j2)
                self.joints_beams_other[j1][id] = j2
                self.joints_beams_other[j2][id] = j1
        
        # sort beam ids just in case
        self.beam_ids.sort()
        self.n_beams = len(self.beam_ids)


    def generate_matrix(self):
        '''
        Generate matrix in the matrix equation from linear equation groups in the
        truss analysis.
        '''

        # check if proposed matrix is square
        if self.n_beams + self.n_zerodisps * 2 != self.n_joints * 2:
            raise RuntimeError('Truss geometry not suitable for static equilibrium analysis!')

        # initialize components of CSR format of the matrix 
        matrix_row = []
        matrix_col = []
        matrix_val = []

        # process data of each joint and generate terms for beam forces
        for j_index, j in enumerate(self.joint_ids):
            j_coord = self.joint_coords[j]
            # process each connecting beam of the current joint
            for b, other in self.joints_beams_other[j].items():
                b_index = self.beam_ids.index(b)
                # find the coordinates of the other joint and calculate the beam length
                other_coord = self.joint_coords[other]
                dis = ((j_coord[0] - other_coord[0]) ** 2 + (j_coord[1] - other_coord[1]) ** 2) ** 0.5
                # each beam of the current joint will take two terms
                # term positions in the matrix can be determined by the joint and beam indexes
                matrix_row.append(j_index * 2)
                matrix_col.append(b_index)
                matrix_val.append((j_coord[0] - other_coord[0]) / dis)
                matrix_row.append(j_index * 2 + 1)
                matrix_col.append(b_index)
                matrix_val.append((j_coord[1] - other_coord[1]) / dis)
        
        # generate terms for reaction forces at the supports
        for zerodisp_index, j in enumerate(self.joint_zerodisps):
            # find the joint indexes and determine the term position in the matrix
            j_index = self.joint_ids.index(j)
            matrix_row.append(j_index * 2)
            matrix_col.append(self.n_beams + zerodisp_index * 2)
            matrix_val.append(1.)
            matrix_row.append(j_index * 2 + 1)
            matrix_col.append(self.n_beams + zerodisp_index * 2 + 1)
            matrix_val.append(1.)

        # generate the matrix in CSR format by components
        self.matrix = scipy.sparse.csr_matrix((matrix_val, (matrix_row, matrix_col)))


    def calculate_forces(self):
        '''
        Generate the vector on the right hand side of the matrix equation and solve
        the matrix equation to get beam forces.
        '''

        # generate the vector b by taking the opposite number of each external force
        vector_b = np.zeros(self.n_joints * 2)
        for j_index, j in enumerate(self.joint_ids):
            vector_b[j_index * 2] = self.joint_fxys[j][0] * -1
            vector_b[j_index * 2 + 1] = self.joint_fxys[j][1] * -1

        # try to solve the matrix equation and raise error if the equation is singular
        try:
            solution = scipy.sparse.linalg.spsolve(self.matrix, vector_b)
        except scipy.sparse.linalg.dsolve.linsolve.MatrixRankWarning:
            raise RuntimeError('Cannot solve the linear system, unstable truss?')

        # only take beam forces as result and disgard reaction forces at supports
        self.forces = solution[:self.n_beams]

    def PlotGeometry(self, plot_file):
        '''
        Plot beam geometry and save it to the input path.
        '''

        plt.figure()
        for b in self.beam_ids:
            # plot a blue line between coordinates of joints connected by each beam
            j1, j2 = self.beam_joints[b]
            j1_coord = self.joint_coords[j1]
            j2_coord = self.joint_coords[j2]
            plt.plot([j1_coord[0], j2_coord[0]], [j1_coord[1], j2_coord[1]], 'b-')

        # modify the scales and margins and save the figure
        plt.axis('equal')
        plt.gca().margins(0.05,0.05)
        plt.savefig(plot_file)

    def __repr__(self):
        '''
        Return the beam forces with ids in order.
        '''
        res = ' Beam       Force\n'
        res += '-----------------\n'
        for i in range(self.n_beams):
            res += '{:5.0f}  '.format(int(self.beam_ids[i]))
            res += '{:10.3f}\n'.format(self.forces[i])
        return res
