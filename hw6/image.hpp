#ifndef IMAGE_HPP
#define IMAGE_HPP

#include <boost/multi_array.hpp>
#include <string>

class image {

private:

    std::string filename;
    boost::multi_array<unsigned char, 2> img;

    /* operate a kernel on an input image and generate an output image */
    void Convolution(boost::multi_array<unsigned char, 2>& input,
                     boost::multi_array<unsigned char, 2>& output,
                     boost::multi_array<float, 2>&         kernel);

public:

    /* constructor accepts a filename string to read the image of the file */
    image(const std::string& inputname);

    /* save the current image with the given filename */
    void Save(const std::string& outputname);

    /* smooth the current image with the given kernel size */
    void BoxBlur(int size);

    /* calculate the sharpness of the current image */
    unsigned int Sharpness();
};

#endif /* IMAGE_HPP */
