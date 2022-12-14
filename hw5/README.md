# CME 211 Homework 5

### Author: Zherui Lin

## Brief Statement

The given maze file represents a maze where each pair of coordinates represents a wall at that position. The task is to find a valid path from the entrance on the top line to the exit on the bottom line of the maze by the right hand wall follower algorithm. The coordinates of cells on the path should be printed in a file with the given solution file name in order. The supplementary task is to check if the solution file provides an exactly valid solution for the original maze file.

## Description of mazesolver.cpp

The program takes maze file name and solution file name as command line parameters. The maze is represented as a 2-d static boolean array, whose size is at most 201 by 201. The path is generated by the right hand wall follower algorithm from the non-wall entrance at the top row of the maze. For each step, the next cell to move to is attempted by checking the adjacent 4 cells of the current cell, in order based on the direction from the previous cell to the current cell. Once we find a valid next cell, we should immediately move to it and keep generating the path until the current cell is on the bottom row. The coordinates on the path are written to the solution file during the path generation.

## Brief Summary of checksoln.py

The program takes maze file name and solution file name as command line parameters. The maze is represented as a 2-d np boolean array and the solution path is represented as a list. We first check if the beginning and the ending coordinates on the path are on the top and the bottom row of the maze, respectively. Then, for each cell on the path, we should check if it is within the boundary of the maze, if it is not a wall, and if the step from the previous cell moves exactly one position. If any invalid condition found, print out the invalid message and exit the program.