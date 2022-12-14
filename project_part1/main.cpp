#include <fstream>
#include <iostream>
#include <string>

#include "CGSolver.hpp"
#include "COO2CSR.hpp"

int main(int argc, char* argv[]) {

    /* check the command line arguments */
    if (argc < 3) {
        std::cout << "Usage:" << std::endl;
        std::cout << "  " << argv[0] << " <input matrix file name> <output solution file name>" << std::endl;
        return 0;
    }

    /* extract command line arguments */
    std::string input = argv[1];
    std::string output = argv[2];

    /* declare data structures and read matrix in COO form from input file to them */
    std::vector<double> val;
    std::vector<int> row;
    std::vector<int> col;
    int nrows, ncols;
    std::ifstream ifs;
    ifs.open(input);
    if (ifs.is_open()) {
        ifs >> nrows >> ncols;
        double v;
        int r, c;
        while (ifs >> r >> c >> v) {
            val.push_back(v);
            row.push_back(r);
            col.push_back(c);
        }
        ifs.close();
    }
    else {
        std::cerr << "ERROR: Failed to open file " << input << std::endl;
    }

    /* convert matrix form from COO to CSR in place */
    COO2CSR(val, row, col);

    /* initialize vectors and tolerance */
    std::vector<double> x(nrows, 1.);
    std::vector<double> b(nrows, 0.);
    double tol = 1.e-5;

    /* solve the linear system by CG algorithm and print failure messages if did not converge */
    int niter = CGSolver(val, row, col, b, x, tol);
    if (niter == -1) {
        std::cout << "FAILURE: CG solver did not converge." << std::endl;
        return 0;
    }

    /* write the solution vector to the outfile in scientific notation with 4 decimal places */
    std::ofstream ofs;
    ofs.setf(std::ios::scientific, std::ios::floatfield);
    ofs.precision(4);
    ofs.open(output);
    if (ofs.is_open()) {
        for (auto value : x) {
            ofs << value << std::endl;
        }
        ofs.close();
    }
    else {
        std::cerr << "ERROR: Failed to open file " << output << std::endl;
    }

    /* print success messages with number of iterations */
    std::cout << "SUCCESS: CG solver converged in " << niter << " iterations." << std::endl;
    return 0;
}