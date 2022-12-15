#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

#include "CGSolver.hpp"
#include "heat.hpp"
#include "sparse.hpp"

/* calculate the lower boundary temperature at column index j on the x axis */
double HeatEquation2D::CalCoolTemp(int j) {
    double x = j * h;
    return -tc * (std::exp(-10 * std::pow(x - l / 2, 2)) - 2);
}

/* add isothermal and periodic boundaries temperature data to solution file */
void HeatEquation2D::AddBoundaryTemp(const std::string &solnfile) {
    std::vector<double> temp;

    /* append upper isothermal boundary temperature */
    for (int j = 0; j <= ncols; j++) {
        temp.push_back(th);
    }

    /* append interior node and periodic boundaries temperature 
     * from existing solution file */
    std::ifstream ifs;
    ifs.open(solnfile);
    if (ifs.is_open()) {
        double tmp;
        for (int i = 0; i < nrows; i++) {
            /* cache beginning temperature on periodic boundary */
            double periodic;
            for (int j = 0; j < ncols; j++) {
                ifs >> tmp;
                temp.push_back(tmp);
                if (j == 0) {
                    periodic = tmp;
                }
            }
            /* append periodic temperature for ending a row */
            temp.push_back(periodic);
        }
        ifs.close();
    }
    else {
        std::cerr << "ERROR: Failed to open file " << solnfile << std::endl;
        exit(1);
    }

    /* append lower isothermal boundary temperature */
    for (int j = 0; j <= ncols; j++) {
        temp.push_back(CalCoolTemp(j));
    }

    /* rewrite modified vector to original solution file */
    std::ofstream ofs;
    ofs.open(solnfile);
    if (ofs.is_open()) {
        for (double d : temp) {
            ofs << d << std::endl;
        }
        ofs.close();
    }
    else {
        std::cerr << "ERROR: Failed to open file " << solnfile << std::endl;
        exit(1);
    }
}

/* Method to setup Ax=b system */
int HeatEquation2D::Setup(const std::string &inputfile) {

    /* read input variables and initial attributes */
    std::ifstream f;
    f.open(inputfile);
    if (f.is_open()) {
        f >> l >> w >> h;
        f >> tc >> th;
        f.close();
    }
    else {
        std::cerr << "ERROR: Failed to open input file" << std::endl;
        exit(1);
    }
    nrows = (int) (w / h) - 1;
    ncols = (int) (l / h);
    /* take average of th and tc as initial guess of each elem */
    double init = (th + tc) / 2;

    /* generate matrix and vector b */
    for (int i = 0; i < nrows; i++) {
        for (int j = 0; j < ncols; j++) {
            /* unknown temperature is indexed by flatten grid */
            int ctr = i * ncols + j;
            /* take mudulo to wrap around domain */
            int left = i * ncols + (j - 1 + ncols) % ncols;
            int right = i * ncols + (j + 1) % ncols;
            int up = ctr - ncols;
            int down = ctr + ncols;
            A.AddEntry(ctr, ctr, 4.);
            A.AddEntry(ctr, left, -1.);
            A.AddEntry(ctr, right, -1.);
            /* handle isothermal boundary cases */
            if (i == 0) {
                b.push_back(th);
            }
            else {
                A.AddEntry(ctr, up, -1.);
            }
            if (i == nrows - 1) {
                b.push_back(CalCoolTemp(j));
            }
            else {
                A.AddEntry(ctr, down, -1.);
            }
            if (i != 0 && i != nrows - 1) {
                b.push_back(0.);
            }
            /* generate initial guess */
            x.push_back(init);
        }
    }
    return 0;
}

/* Method to solve system using CGsolver */
int HeatEquation2D::Solve(const std::string &soln_prefix) {
    A.ConvertToCSR();
    double tol = 1.e-5;

    /* solve the linear system by CG algorithm and print failure messages if did not converge */
    int niter = CGSolver(A, b, x, tol, soln_prefix);
    if (niter == -1) {
        std::cout << "FAILURE: CG solver did not converge." << std::endl;
        return 0;
    }

    /* add boundary temperature to complete raw solution in each solution file */
    for (int i = 0; i <= niter; i++) {
        if (i % 10 != 0 && i != niter) {
            continue;
        }
        std::stringstream ss;
        ss.fill('0');
        ss << soln_prefix << std::setw(3) << i << ".txt";
        AddBoundaryTemp(ss.str());
    }

    /* print success messages with number of iterations */
    std::cout << "SUCCESS: CG solver converged in " << niter << " iterations." << std::endl;
    return 0;
}