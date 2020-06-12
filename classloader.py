'''
This defines classes for the population of variables, and the costs functions. This is generic to any genetic algorithm
'''
import numpy as np
import random

class designVariables:
    # This class produces an object that contains the population of design variables
    # It also contains the parameters of the design variables and the algorithm, such as constraints, number of generations, population size, etc.
    # In this case, the variables are  l_beam, l_mass, w_mass, t_mass
    def __init__(self, num_variables=1, constraints=[[0,1]], num_generations=10, population_size=100):
        # num_variables is the number of design variables, which in this case is 4
        # constraints is a list of list of constraints per design variable. Index [0] is the min and [1] is max.   
        assert(num_variables == len(constraints))
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_variables = num_variables
        self.constraints = np.ndarray(shape = (num_variables, 2))
        for i in range(num_variables):
            self.constraints[i][0] = constraints[i][0]
            self.constraints[i][1] = constraints[i][1]
        self.population = np.random.rand(population_size, num_variables)
        self.offspring = self.population  # This is just for initialization, with the size of offspring population equal to that of parent population
        for i in range(population_size):
            for j in range(num_variables):
                self.population[i][j] = self.constraints[j][0] + (self.constraints[j][1] - self.constraints[j][0])*self.population[i][j]


'''
The first ojective function is the sensor area= 2*(l_beam*(w_beam +t_beam)) + 2*(l_mass*(w_mass +t_mass)) + w_mass*t_mass, which is to be minimized
The area of the width and thichness of the beam and mass connection is not considered, as it is negligible

The second objective function is sensor noise per unit frequency
Noise is proportional to the sqrt(w)/volume of moving mass
The power spectral density is proportional to (w_beam * t_beam^3)/(l_mass * l_beam^2 * (l_beam*w_beam*t_beam + l_mass*w_mass*t_mass)^3)
Since the beam contributes very less to the total moving mass of the system, the approximate objective function is as below
Approximate objective function: w_beam * t_beam^3 * l_beam^(-2) * l_mass^(-4) * w_mass^(-3) * t_mass*(-3)
Since w_beam and t_beam only are in the numerator of the two objective functions, they have to be minimum
So, w_beam and t_beam can be chosen as the minimum values allowable based on mechanical properties, in this case, 0.2 and 0.05 mm respectively
Now, the modified objective function is l_beam^2 * l_mass^4 * w_mass^3 * t_mass^3, which is to be maximized
To keep optimization as minimization, the negative value has been taken
'''

class objectives:
    # This is the class for the objective functions
    def __init__(self, num_objectives):
        self.num_objectives = num_objectives

    def find_costs(self, designVariables):
        # returns the costs for all the design variables as a numpy array.
        # Here, 2 objectives have been defined, and costs for them will be the output. This can also be 3, but it's not advisable to use NSGA for 1 or >3 objectives
        
        costs = np.ndarray(shape=(designVariables.shape[0], self.num_objectives))
        
        costs[:, 0:1] = 2*designVariables[:, 0:1]*(0.3*0.05) + 2*np.multiply(designVariables[:, 1:2], designVariables[:, 2:3] + designVariables[:, 3:4]) + np.multiply(designVariables[:, 2:3], designVariables[:, 3:4])
        costs[:, 1:2] = (1) /(designVariables[:, 0:1]**2 * designVariables[:, 1:2]**4 * designVariables[:, 2:3]**3 * designVariables[:, 3:4]**3)
        # Update the line below if 3 objective functions are to be used
        # costs[:, 2:3] = function()

        return costs
