TrafficRoadCalculation
======================

This is a solver for finding the shortest path to work taking in account the Traffic Costs that each of 
the available roads have (based on their traffic levels). The software implements two algorithms in order
to find a solution to the problem:
 
* UCS: Uniform-Cost Search

* IDA*: Iterative Deepening A*

The IDA* heuristic function is the UCS itself, resulting in a more Dijkstra-like algorithm for traversing 
the graph. It also results in a much higher complexity of the IDA* algorithm while having little gain in 
the actual generated cost.

Finally the format which our dataset was provided was not very good, nor intuitive but that was out of 
my hands and had to deal with it.


Enjoy the code.

Peace out!
