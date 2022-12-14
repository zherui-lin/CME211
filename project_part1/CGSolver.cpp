#include <vector>

#include "CGSolver.hpp"
#include "matvecops.hpp"

/* Solve a linear system in CSR form by CG algorithm and return the times of iteration. */
int CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol) {
    /* take the solution vector size as maximum number of iterations */
    int nitermax = (int) x.size();
    std::vector<double> r = AddVec(b, MulScl(-1., MulMatVec(val, row_ptr, col_idx, x)));
    double norm0 = Norm(r);
    std::vector<double> p = r;
    int niter = 0;
    while (niter < nitermax) {
        niter++;
        /* cache the dot product of current r itself */
        double rr = MulVec(r, r);
        /* cache the result of multiplication of the original matrix A and vector p */
        std::vector<double> Ap = MulMatVec(val, row_ptr, col_idx, p);
        double alpha = rr / MulVec(p, Ap);
        x = AddVec(x, MulScl(alpha, p));
        r = AddVec(r, MulScl(-alpha, Ap));
        double norm = Norm(r);
        if (norm / norm0 < tol) {
            break;
        }
        double beta = MulVec(r, r) / rr;
        p = AddVec(r, MulScl(beta, p));
    }
    /* return the current iteration number if converged */
    if (niter <= nitermax) {
        return niter;
    }
    return -1;
}