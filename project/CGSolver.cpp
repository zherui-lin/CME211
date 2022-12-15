#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

/* Solve a linear system in CSR form by CG algorithm and return the times of iteration. */
int CGSolver(SparseMatrix &matrix,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             const std::string &soln_prefix) {
                
    /* take the solution vector size as maximum number of iterations */
    int nitermax = (int) x.size();
    std::vector<double> r = AddVec(b, MulScl(-1., matrix.MulVec(x)));
    double norm0 = Norm(r);
    std::vector<double> p = r;
    int niter = 0;

    /* write the solution for the first iteration */
    WriteSoln(soln_prefix, 0, x);

    while (niter < nitermax) {
        niter++;
        /* cache the dot product of current r itself */
        double rr = MulVec(r, r);
        /* cache the result of multiplication of the original matrix A and vector p */
        std::vector<double> Ap = matrix.MulVec(p);
        double alpha = rr / MulVec(p, Ap);
        x = AddVec(x, MulScl(alpha, p));
        r = AddVec(r, MulScl(-alpha, Ap));
        double norm = Norm(r);
        if (norm / norm0 < tol) {
            break;
        }
        double beta = MulVec(r, r) / rr;
        p = AddVec(r, MulScl(beta, p));

        /* write solution after every 10 itertions */
        if (niter % 10 == 0) {
            WriteSoln(soln_prefix, niter, x);
        }
    }
    
    /* write solution and return the current iteration number if converged */
    if (niter <= nitermax) {
        WriteSoln(soln_prefix, niter, x);
        return niter;
    }
    return -1;
}

/* write current solution vector x to file with given solution prefix and itertion times n */
void WriteSoln(const std::string &soln_prefix, int n, const std::vector<double> &x) {

    /* generate solution file name with prefix and iteration times 
     * by stringstream for formatting */
    std::stringstream ss;
    ss.fill('0');
    ss << soln_prefix << std::setw(3) << n << ".txt";

    std::ofstream f;
    f.open(ss.str());
    if (f.is_open()) {
        /* write vector x to file one value per line */
        for (double d : x) {
            f << d << std::endl;
        }
        f.close();
    }
    else {
        std::cerr << "ERROR: Failed to open file " << ss.str() << std::endl;
        exit(1);
    }
}