#include <iomanip>
#include <iostream>
#include <string>

#include "hw6.hpp"
#include "image.hpp"

int main() {
    image original = image("stanford.jpg");
    std::cout << "Original image: " << original.Sharpness() << std::endl;
    int k_size[] = {3, 7, 11, 15, 19, 23, 27};
    for (int k : k_size) {
        image img = image("stanford.jpg");
        img.BoxBlur(k);
        /* generate output image name by stringstream for formatting */
        std::stringstream ss;
        ss.fill('0');
        ss << "BoxBlur" << std::setw(2) << k << ".jpg";
        img.Save(ss.str());
        std::cout << "BoxBlur(" << std::setw(2) << k << "): " << img.Sharpness() << std::endl;
    }
    return 0;
}
