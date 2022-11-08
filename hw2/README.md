# CME 211 Homework 2

### Author: Zherui Lin

## Part 1

1. The test data should make 10 users watch all 3 movies, in which there will be 30 records and for each pair of movies there will be enough common users. Also, the ratings should be random.
2. In the real data file, there might be consecutive blankspaces among numbers in a line, which align different lines. I also make this in my test data.
3. I did create a reference solution for my test data, and I made it with the help of other computational software.

## Part 2

### Command line log:

$ python3 similarity.py ml-100k/u.data similarities.txt  
Input MovieLens file: ml-100k/u.data  
Output file for similarity data: similarities.txt  
Minimum number of common users: 5  
Read 100000 lines with total of 1682 movies and 943 users  
Computed similarities in 35.423529 seconds  

### First 10 lines of the output similarity file:

1 (918,0.91,5)  
2 (1056,1.00,5)  
3 (1081,0.98,5)  
4 (35,0.80,6)  
5 (976,0.93,5)  
6 (279,0.96,5)  
7 (968,1.00,7)  
8 (590,0.86,6)  
9 (113,0.96,5)  
10 (1202,0.97,5)  

### Program decomposition:

1. Transfer original data into a nested dictionary, which maps movies to users and then maps users to ratings.
2. Calculate the mean of all ratings of each movie and store it in another dictionary mapping from movies to mean ratings.
3. Declare a result dictionary which maps movies to other movies and then maps other movies to similarities between the first movie and the second movie. The calculation is done by a helper function.
4. Iterate the result dictionary in the order of the movie id and find the maximum similarity of each movie, and then append to the result list.
