'''
This defines genetic operators such as selection, crossover and mutation
'''
import numpy as np
import random

def clip(val, min, max):
    if val < min:
        return min
    elif val > max:
        return max
    else:
        return val

def uniform_probability_offspring(p1, p2, constraints, lower_bound, upper_bound):
    # This function returns the offspring, with uniform probability, such that, for each variable, the offspring has its values on the line joining the two parents
    assert(p1.shape[0] == p2.shape[0] == constraints.shape[0])
    temp = p1 + np.multiply(p2-p1, lower_bound*np.ones(p1.shape[0]) + (upper_bound-lower_bound)*np.random.random(p1.shape[0]))
    return np.clip(temp, constraints[:, 0], constraints[:, 1])

def selection(p):
    # This function should perform selection for selecting the parents to offspring
    # It is not used in the code, but if needed, it can be used 
    pass

def mutation(p, constraints):
    # This function performs mutation on the offspring of the population by perturbing the variables withing 10% of their current values, while taking into account the constraints
    # constraints is a numpy array of min and max values for each variable
    # p is a numpy array of the offspring population only
    assert(p.shape[1] == constraints.shape[0])
    for j in range(p.shape[0]):
        for i in range(constraints.shape[0]):
            r = random.random()
            if r < 0:
                p[j][i] *= (0.9 + random.random()*0.2)
                p[j][i] = clip(p[j][i], constraints[i][0], constraints[i][1])
    return p

def recombination(p):
    # This function performs crossover (or recombination) in the population set and the returns the population.
    # This function generates two offsprings, with a uniform distribution for each variable, within the domain -0.25 to 1.25 (0 being parent 1, 1 being parent 2)
    # p is an object of the designVariables class
    # This function overwrites the offspring variable of the p object, with new offspring population
    
    np.random.shuffle(p.population)
    for i in range(int(p.population.shape[0] / 2)):
        p.offspring[2*i][:] = uniform_probability_offspring(p.population[2*i][:], p.population[2*i+1][:], p.constraints, -0.25, 1.25)
        p.offspring[2*i+1][:] = uniform_probability_offspring(p.population[2*i][:], p.population[2*i+1][:], p.constraints, -0.25, 1.25)

    return p