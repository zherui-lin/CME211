#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

#include <vector>

/* calculate the result of sum of two vectors, i.e., a + b */
std::vector<double> AddVec(const std::vector<double> &a, const std:: vector<double> &b);

/* calculate the result of scalar multiplication of vector, i.e., kv */
std::vector<double> MulScl(double k, const std::vector<double> &v);

/* calculate the result of matrix multiplication of vector in CSR form, i.e., Mv */
std::vector<double> MulMatVec(const std::vector<double> &val,
                              const std::vector<int>    &row_ptr,
                              const std::vector<int>    &col_idx,
                              const std::vector<double> &v);

/* calculate the dot product of two vectors, i.e., a·b */
double MulVec(const std::vector<double> &a, const std::vector<double> &b);

/* calculate the norm of vector, i.e., ||v|| */
double Norm(const std::vector<double> &v);

#endif /* MATVECOPS_HPP */