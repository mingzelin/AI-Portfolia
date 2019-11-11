Mingze Lin

email:m59lin@edu.uwaterloo.ca


Run question1 commandline:
python tsp_solver.py


Heuristic function will perform 3 steps:

Step 1:	find the shortest path from city_k to any of the cities from the rest n-k cities, call it cost1


Step2: 	get the list of distance between each cities from the rest n-k cities
sort the list by the distance values
sum the top n-k-1-2 = n-k-3 shortest distances, call it cost2

Step3: 	find the shortest path from city A (start point) to any of the cities from the rest n-k cities, call it cost3

h(k) = cost1 + cost2 + cost3


node: a representation of each state, it records f, g, name, X, Y for the last added node and it stores the visited node (in format [[Name]….]) and the unvisited node (in format [[Name, X, Y]…])
heap: a priority queue that ranks nodes by their corresponding f value.

A star function:
While we have not travelled to all the cities, pop min from heap generate a node for each of min’s unvisited cities and push the new nodes into heap and once done continue loop. Once we have travelled all the cities return the g of the last popped node.

