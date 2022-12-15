#include "COO2CSR.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

/* Method to modify sparse matrix dimensions */
void SparseMatrix::Resize(int nrows, int ncols) {
    this->ncols = ncols;
    this->nrows = nrows;
}

/* Method to add entry to matrix in COO format */
void SparseMatrix::AddEntry(int i, int j, double val) {
    i_idx.push_back(i);
    j_idx.push_back(j);
    a.push_back(val);
}

/* Method to convert COO matrix to CSR format using provided function */
void SparseMatrix::ConvertToCSR() {
    COO2CSR(a, i_idx, j_idx);
}

/* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
std::vector<double> SparseMatrix::MulVec(const std::vector<double> &vec) {
    return MulMatVec(a, i_idx, j_idx, vec);
}