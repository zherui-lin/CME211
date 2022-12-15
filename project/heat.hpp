#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
  private:
    SparseMatrix A;
    std::vector<double> b, x;

    /* TODO: Add any additional private data attributes and/or methods you need */
    double l; // length of periodic section
    double w; // width of wall
    double h;
    double th;
    double tc;
    int nrows;
    int ncols;

    /* calculate the lower boundary temperature at column index j on the x axis */
    double CalCoolTemp(int j);

    /* add isothermal and periodic boundaries temperature data to solution file
     * which is created by CG solver and has only calculated result */
    void AddBoundaryTemp(const std::string &solnfile);

  public:
    /* Method to setup Ax=b system */
    int Setup(const std::string &inputfile);

    /* Method to solve system using CGsolver */
    int Solve(const std::string &soln_prefix);

    /* TODO: Add any additional public methods you need */

};

#endif /* HEAT_HPP */
