#include <algorithm>
#include <boost/multi_array.hpp>
#include <iostream>
#include <string>

#include "hw6.hpp"
#include "image.hpp"

#define BOOST_DISABLE_ASSERTS

/* constructor accepts a filename string to read the image of the file */
image::image(const std::string& inputname) {
    this->filename = inputname;
    ReadGrayscaleJPEG(inputname, this->img);
}

/* save the current image with the given filename */
void image::Save(const std::string& outputname) {
    WriteGrayscaleJPEG(outputname == "" ? this->filename : outputname, this->img);
}

/* operate a kernel on an input image and generate an output image */
void image::Convolution(boost::multi_array<unsigned char, 2>& input,
                        boost::multi_array<unsigned char, 2>& output,
                        boost::multi_array<float, 2>&         kernel) {

    /* check if the input and output are of the same size */
    if (input.shape()[0] != output.shape()[0] || input.shape()[1] != output.shape()[1]) {
        std::cerr << "The input and output are not of the same size!" << std::endl;
        exit(1);
    }
    /* check if the kernel is square */
    if (kernel.shape()[0] != kernel.shape()[1]) {
        std::cerr << "The kernel is not square!" << std::endl;
        exit(1);
    }
    int k = (int) kernel.shape()[0];
    /* check if the kernel size is odd and at least 3 */
    if (k < 3 || k % 2 == 0) {
        std::cerr << "The kernel has a wrong size!" << std::endl;
        exit(1);
    }
    int nrows = (int) input.shape()[0];
    int ncols = (int) input.shape()[1];
    /* iterate over the image */
    for (int i = 0; i < nrows; i++) {
        for (int j = 0; j < ncols; j++) {
            /* initialize the calculate result at the current pixel */
            double sum = 0.;
            /* iterate over the kernel */
            for (int ii = 0; ii < k; ii++) {
                /* find the row index of the corresponding pixel on the image 
                 * and handle out-of-bound cases */
                int r = std::min(std::max(i + ii - k / 2, 0), nrows - 1);
                for (int jj = 0; jj < k; jj++) {
                    /* find the col index of the corresponding pixel on the image 
                     * and handle out-of-bound cases */
                    int c = std::min(std::max(j + jj - k / 2, 0), ncols - 1);
                    sum += input[r][c] * kernel[ii][jj];
                }
            }
            /* cast result at the current pixel to unsigned char and handle overflow cases */
            output[i][j] = (unsigned char) std::min(std::max(std::floor(sum), 0.), 256.);
        }
    }
}

/* smooth the current image with the given kernel size */
void image::BoxBlur(int size) {
    boost::multi_array<float, 2> kernel(boost::extents[size][size]);
    /* generate the kernel by filling */
    std::fill(kernel.origin(), kernel.origin() + kernel.num_elements(), 1./size/size);
    boost::multi_array<unsigned char, 2> temp = this->img;
    Convolution(temp, this->img, kernel);
}

/* calculate the sharpness of the current image */
unsigned int image::Sharpness() {
    boost::multi_array<float, 2> kernel(boost::extents[3][3]);
    kernel[0][0] = 0.;
    kernel[0][1] = 1.;
    kernel[0][2] = 0.;
    kernel[1][0] = 1.;
    kernel[1][1] = -4.;
    kernel[1][2] = 1.;
    kernel[2][0] = 0.;
    kernel[2][1] = 1.;
    kernel[2][2] = 0.;
    boost::multi_array<unsigned char, 2> temp = this->img;
    Convolution(this->img, temp, kernel);
    /* find the max elem on the output multi array and return it as result */
    unsigned int sharpness = *std::max_element(temp.origin(), temp.origin() + temp.num_elements());
    return sharpness;
}
