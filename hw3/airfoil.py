import glob, math, os

class Airfoil:
    ''' 
    An Airfoil object is initialized by a pathname. The initialization method
    will process all data file in that pathname, including the airfoil geometry
    and pressure coefficient data. The string representation method will give the 
    result of the computation.
    '''

    def __init__(self, pathname):
        '''
        Files in the input pathname are processed to calculate cl values.
        '''
        self.handle_input(pathname)
        self.handle_xy()
        self.handle_pres()
        self.process_data()

    def handle_input(self, pathname):
        '''
        In the directory of the input pathname, store the pathname of xy.dat as
        self.file_xy and store all alpha values of pressure coefficient files in a
        sorted list named self.alphas. Use a dictionary named self.file_pres to map 
        from each alpha value to its coresponding file pathname.
        '''
        # check if given pathname is a valid directory
        if not os.path.isdir(pathname):
            raise RuntimeError('{} is not a valid directory'.format(pathname))
        # get all file pathnames in the directory
        if pathname[len(pathname) - 1] != '/':
            pathname = pathname + '/'
        files = glob.glob(pathname + '*')
        self.file_xy = ''
        self.alphas = []
        self.file_pres = {}
        # seperate xy.dat and alpha<value>.dat files in the directory
        for f in files:
            if os.path.basename(f) == 'xy.dat':
                self.file_xy = f
            else:
                # extract alpha values from the file name
                alpha = float(os.path.basename(f)[5:-4])
                self.alphas.append(alpha)
                self.file_pres[alpha] = f
        # check if any of the required data files do not exist in the directory
        if self.file_xy == '':
            raise RuntimeError('xy.dat cannot be found in {}'.format(pathname))
        if len(self.alphas) == 0:
            raise RuntimeError('no pressure coeffient data file found in {}'.format(pathname))
        # sort alpha values to make string representation sorted
        self.alphas.sort()

    def handle_xy(self):
        '''
        Extract coordinate values from self.file_xy file to a list named self.coords
        and also calculate the chord of the airfoil as self.chord.
        '''
        self.coords = []
        try:
            with open(self.file_xy, 'r') as f:
                # extract first line as the airfoil name and other lines as coordinate values
                self.name = f.readline().strip()
                for line in f.readlines():
                    point = line.strip().split()
                    self.coords.append((float(point[0]), float(point[1])))
        except Exception as e:
            raise RuntimeError(e)
        # extract all values and calculate range difference as chord
        x_coords = [coord[0] for coord in self.coords]
        self.chord = max(x_coords) - min(x_coords)

    def handle_pres(self):
        '''
        Extract pressure coefficients from files in the self.pres_coeffs values. 
        Use a dictionary to map from each alpha value to the corresponding list of 
        pressure coefficent data.
        '''
        self.pres_coeffs = {}
        for a in self.alphas:
            try:
                with open(self.file_pres[a], 'r') as f:
                    # discard the first line and take all other lines into a list
                    f.readline()
                    self.pres_coeffs[a] = [float(line.strip()) for line in f.readlines()]
            except Exception as e:
                raise RuntimeError(e)
            # check if length of coordinates and pressure coefficients match
            if len(self.pres_coeffs[a]) != len(self.coords) - 1:
                raise RuntimeError('length of xy.dat and {} mismatch'.format(self.file_pres[a]))

    def process_data(self):
        '''
        Process data in self.pres_coeffs with self.coords and calculate cl and
        stagnation point for each alpha value. The results are stored in dictionaries
        mapping from each alpha value to the corresponding results named self.cls,
        self.stag_pts and self.stag_coeffs.
        '''
        self.cls = {}
        self.stag_pts = {}
        self.stag_coeffs = {}
        for a in self.alphas:
            # calculate cl and stagnation point results by helper methods
            self.cls[a] = self.cal_cl(a)
            self.stag_pts[a], self.stag_coeffs[a] = self.find_stag_pt(a)
    
    def cal_cl(self, alpha):
        '''
        Return the cl result of the pressure coefficient dataset of alpha.
        '''
        pres = self.pres_coeffs[alpha]
        delta_cx = []
        delta_cy = []
        for i, p in enumerate(pres):
            # pres[i] is the value on the panel between self.coords[i] and self.coords[i + 1]
            coord1, coord2 = self.coords[i], self.coords[i + 1]
            delta_cx.append(-p * (coord2[1] - coord1[1]) / self.chord)           
            delta_cy.append(p * (coord2[0] - coord1[0]) / self.chord)
        cx = sum(delta_cx)
        cy = sum(delta_cy)
        # remember to convert degrees to radians first
        return cy * math.cos(math.radians(alpha)) - cx * math.sin(math.radians(alpha))

    def find_stag_pt(self, alpha):
        '''
        Return the result of stagnation point coordinates and its pressure coefficient
        of the pressure coefficient dataset of alpha.
        '''
        pres = self.pres_coeffs[alpha]
        max_pres = 0
        index = 0
        for i, p in enumerate(pres):
            # find the max pressure coefficient which must be the closest to 1
            if p > max_pres:
                index = i
                max_pres = p
        stag_x = (self.coords[index][0] + self.coords[index + 1][0]) / 2
        stag_y = (self.coords[index][1] + self.coords[index + 1][1]) / 2
        return (stag_x, stag_y), max_pres

    def __repr__(self):
        '''
        Return the result data for each alpha value of each pressure coefficient file.
        '''
        res = 'Test case: {}\n\n'.format(self.name)
        res += 'alpha     cl           stagnantion pt\n'
        res += '-----  -------  --------------------------\n'
        for a in self.alphas:
            res += '{:5.2f}  '.format(a)
            res += '{:7.4f}  '.format(self.cls[a])
            res += '({:7.4f}, {:7.4f})  '.format(self.stag_pts[a][0], self.stag_pts[a][1])
            res += '{:6.4f}\n'.format(self.stag_coeffs[a])
        return res