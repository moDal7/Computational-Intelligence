### Lab 1 - set covering

Various tests on the lab 1 problem proposed by Professor Squillero.
The solutions are incomplete, developed in autonomy unfortunately not with enough time: I have had this course locked since wednesday due to overbooking.
I published anyway to participate and looking for suggestions.

The alternate greedy solution starts with the longest list and then restarts from the shortest ones. It performs generally slightly worse than the normal greedy solution but it does better with N = 20. It clearly depends on lucky distribution of the random lists. It probably yields higher weights, but maybe could explore fewer nodes.

The second started solution looked to implement Dijkstra search on the problem, by building a graph with edges and related weights (with weights being length of the destination list).
It has been copied from [the solution proposed by this lesson on StackAbuse](https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/dijkstras-algorithm/) and will be expanded after the deadline expires, just to try to get it right.
