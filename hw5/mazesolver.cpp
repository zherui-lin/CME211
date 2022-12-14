#include <fstream>
#include <iostream>
#include <string>

int main(int argc, char *argv[]) {

    // check command line parameters
    if (argc < 3) {
        std::cout << "Usage:" << std::endl;
        std::cout << " " << argv[0] << " <maze file> <solution file>" << std::endl;
        return 0;
    }

    // extract command line parameters
    std::string mazeName = argv[1];
    std::string solnName = argv[2];

    // initialize 2-d static boolean array for maze representation
    bool maze[201][201];
    for (int i = 0; i < 201; i++) {
        for (int j = 0; j < 201; j++) {
            maze[i][j] = false;
        }
    }

    // read maze file to the static array
    int maxRow, maxCol;
    std::ifstream fmaze;
    fmaze.open(mazeName);
    if (fmaze.is_open()) {
        // read maze size and verify the static array size
        fmaze >> maxRow >> maxCol;
        if (maxRow > 201 || maxCol > 201) {
            std::cout << "Maze size too big!" << std::endl;
            return 0;
        }
        // mark wall as true in the static boolean array
        int row, col;
        while (fmaze >> row >> col) {
            maze[row][col] = true;
        }
        fmaze.close();
    }
    else {
        std::cerr << "ERROR: Failed to open maze file" << std::endl;
    }

    /* represent 4 directions by specifying the coordinate changes to the next cell
       the order is counter-clockwise to simulate right hand wall follower alogorithm
    */
    int dirs[4][2] = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
    // initialize direction by tracking the index in the dirs array
    int currDir = 0;
    // initialize entrance cell
    int currRow = 0;
    int currCol = 0;

    // find the entrance on the 0th row
    for (int j = 0; j < maxCol; j++) {
        if (!maze[0][j]) {
            currCol = j;
        }
    }

    // generate solution path and write it to the solution file
    std::ofstream fsoln;
    fsoln.open(solnName);
    if (fsoln.is_open()) {
        // keep generating path until current position gets to maxRow
        while (currRow < maxRow) {
            // record current cell before looking for next cell
            fsoln << currRow << " " << currCol << std::endl;
            // iterate over 4 directions and look for next cell
            for (int d = 0; d < 4; d++) {
                // the starting direction should be clockwise next direction
                int nextDir = (currDir + 3 + d) % 4;
                int nextRow = currRow + dirs[nextDir][0];
                int nextCol = currCol + dirs[nextDir][1];
                // valid next cell should neither exceed the maze nor be a wall
                if (nextRow >= 0 && nextCol >= 0 && nextCol < maxCol && !maze[nextRow][nextCol]) {
                    currDir = nextDir;
                    currRow = nextRow;
                    currCol = nextCol;
                    // move to the next cell immediately if finding one valid
                    break;
                }
            }           
        }
        fsoln.close();
    }
    else {
        std::cerr << "ERROR: Failed to open solution file" << std::endl;
    }
    return 0;
}
