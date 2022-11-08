# CME 211 Homework 1

### Author: Zherui Lin

## Part 2

### Command line log:

$ python3 generatedata.py 1000 600 50 "ref_1.txt" "reads_1.txt"  
reference length: 1000  
number reads: 600  
read length: 50  
aligns 0: 0.168333  
aligns 1: 0.718333  
aligns 2: 0.113333  

$ python3 generatedata.py 10000 6000 50 "ref_2.txt" "reads_2.txt"  
reference length: 10000  
number reads: 6000  
read length: 50  
aligns 0: 0.150333  
aligns 1: 0.742500  
aligns 2: 0.107167  

$ python3 generatedata.py 100000 60000 50 "ref_3.txt" "reads_3.txt"  
reference length: 100000  
number reads: 60000  
read length: 50  
aligns 0: 0.149100  
aligns 1: 0.748367  
aligns 2: 0.102533  

### Short answers:

- The reference test data I used is "ATCGATCATA", where I used all four letters (bases) and concatenate all prefix substrings of "ATCG". In this case any substring beside "ATC" has at most one occurrence and there are no adjacent letters are the same. Thus any read with adjacent letters must not exist in the reference. Since my test data include all possible cases for reads associated with the reference, my code will always work correctly for other datasets if it works for my test data.

- The 15%/75%/10% distribution cannot be guaranteed since random.random() is applied, which makes the actual frequency of each type of reads distract from the theoretical probability. In other words, the uncontrolled random process will definitely affect the exact distribution of the reads.

- I spent about **1.5 hours** to reading the specifications, writing codes and debugging.

## Part 3

### Command line log:

$ python3 processdata.py ref_1.txt reads_1.txt align_1.txt  
reference length: 1000  
number reads: 600  
aligns 0: 0.168333  
aligns 1: 0.718333  
aligns 2: 0.113333  
elapsed time: 0.006340  

$ python3 processdata.py ref_2.txt reads_2.txt align_2.txt  
reference length: 10000  
number reads: 6000  
aligns 0: 0.150333  
aligns 1: 0.742500  
aligns 2: 0.107167  
elapsed time: 0.257226  

$ python3 processdata.py ref_3.txt reads_3.txt align_3.txt  
reference length: 100000  
number reads: 60000  
aligns 0: 0.149100  
aligns 1: 0.748367  
aligns 2: 0.102533  
elapsed time: 23.814931  

### Short answers:

- The result distributions from processdata.py exactly match those from generatedata.py. This is because the implementation finish the expected work, of course.

- If the size of the reference and read length increase, the operation time will dramatically increase, **possibly geometrically**. Assume the read length and the coverage are equal to those in the test datasets, the time needed will geometrically increase based on the increase of the reference length. Thus the expected runtime will be (2 ~ 2.5)*10^10 secs, which equals to 630 ~ 800 years, which is not possible for my program to analyze all the data for a human. 

- I spend about **2.5 hours** to reading the specifications, writing codes and debugging.
