# genetic-algorithms
Efficient python implementation for multiobjective evolutionary algorithms 

This is a part of my term project in the course of Genetic Algorithms under Prof. Nirupam Chakraborti at IIT Kharagpur.

The code implements Kalyanmoy Deb's fast non-dominated sorting algorithms NSGA-II, using numpy.
NSGA-II is used to generate the Pareto Optimal solutions for MEMS sensor design. Two objective functions, the sensor area and sensor noise are considered. 
It can be seen that NSGA-II finds the Pareto Optimal solutions easily. 

This implementation is markedly different compared to other open source implementations, in that, it does not rely on for loops and lists for its implementation.

Using efficient numpy functions, the algorithm was able to run in **4 seconds** for population size of 100 and 100 generations, on an i9 hexacore processor. 

The animation below helps visualize the output of the solutions in the objective space.
<p align="center"> 
<img src="https://github.com/JaydeepGodbole/genetic-algorithms/blob/master/44xglv.gif">
</p>
