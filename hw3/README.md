# CME 211 Homework 3

### Author: Zherui Lin

- An Airfoil object is fully declared by the files in the directory of the given pathname with abstraction. 
- It has 9 attributes: file_xy, alphas, file_pres, coords, chord, pres_coeffs, cls, stag_pts, stag_coeffs. It has 8 methods: \_\_init__(pathname), handle_input(pathname), handle_xy(), handle_pres(), process_data(), cal_cl(alpha), find_stag_pt(alpha) and \_\_repr__(). 
- Each method has its own task of assignments to attributes or returning some results, and its implementation will not affect other methods, which include decomposition and encapsulation. The initialization method will call other methods except the string representation method and all attributes will be assigned during this execution.
- The class implementation can handle several types of errors:
    1. The input argument is not a pathname of a valid directory.
    2. The directory does not include a xy.dat file or at least one alpha\<value>.dat file.
    3. Any alpha\<value>.dat file does not have a matched length with that of the xy.dat file.
    4. Errors caught when reading any file.
