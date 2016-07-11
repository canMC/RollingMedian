## Required libraries
sys
re
os
datetime
json
time
dateutil.parser
skiplist - included in SRC. This library implements the data structure that allows for a fast O(ln n) insert and remove of the degree of the node. The benefits to have this special data structure over others (eg. store the degrees in an array/list) is that it maintains sorted data as new elements are added and old one removed as a sliding window advances over a stream of data. It also gives O(1) indexed access to values. Therefore running time per median update is proportional to the log of the number of nodes in the graph.


## Running
In the terminal, go to the root directory and type ./run.sh

## Testing
In the terminal, go to the insight_testsuite directory and type ./run_tests.sh

## Overview
- class Vertex: implements the most basic part of the graph, a node. The Vertex class uses a dictionary (adjacent) to keep track of the vertices to which it is connected, and the weight of each edge (timestamp of the payment). 
The add_neighbor() method is used to add a connection from this vertex to another. 
The get_connections() method returns all of the vertices in the adjacency list. 
The get_degree() method returns the degree of the node. 

- class Graph: The Graph class contains a dictionary(vert-dict) that maps vertex names to vertex objects.
Graph also provides methods for adding vertices to a graph (add_vertex()) and connecting one vertex to another (add_edge()). The get_vertices() method returns the names of all of the vertices in the graph. 
The computeMedianDegree() method calculates the median using skip list library.

- class MedianPayment: the core class of the program
The method processPayments() is responsible for reading the input data from the file and processing payments
The method addPayment() determines whether the new payment to be added to the end of the list, is out of order or outdated and should be ignored.

## Output
The output of each test, output.txt is stored into the corresponding venmo_output folder.

## Logging 
By default logging is enabled, and creates log_file.txt. Logging can be disabled if needed.

