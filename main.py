'''
This function implements the main algorithm
'''
import numpy as np
import classloader
import nsga2
import genetic_operators
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

# Algorithm parameters
num_variables = 4
num_objectives = 2
num_generations = 50
population_size = 100
constraints = [[0.5, 2], [0.5, 3], [0.5, 3], [0.25,0.5]] # The constraints are for min and max values of l_beam, l_mass, w_mass, t_mass respectively. All dimensions in mm.

p = classloader.designVariables(num_variables=num_variables, constraints=constraints, num_generations=num_generations, population_size=population_size)
c = classloader.objectives(num_objectives=num_objectives)
costs = c.find_costs(p.population)

p = genetic_operators.recombination(p)
p.offspring = genetic_operators.mutation(p.offspring, p.constraints)
costs_offspring = c.find_costs(p.offspring)
t = time.time()

generation_count = num_generations
while generation_count>0:
    generation_count -= 1
    combined_population = np.zeros(shape=(2 * p.population.shape[0], p.population.shape[1]))
    combined_population[0:p.population.shape[0], :] = p.population
    combined_population[p.population.shape[0]:2 * p.population.shape[0], :] = p.offspring
    combined_costs = np.zeros(shape=(2 * costs.shape[0], costs.shape[1]))
    combined_costs[0:costs.shape[0], :] = costs
    combined_costs[costs.shape[0]:2 * costs.shape[0], :] = costs_offspring
    
    fronts = nsga2.non_dominated_sorting(combined_costs)
    new_population_count = 0
    new_population = np.zeros((population_size, num_variables))
    i = 0
    while new_population_count + len(fronts[i]) <= population_size:
        for k in range(len(fronts[i])):
            new_population[new_population_count] = combined_population[fronts[i][k]]
            new_population_count += 1
        i += 1
    crowding_distances = nsga2.calculate_crowding_distance(combined_costs, fronts[i], num_objectives)
    sort_by_distance = np.argsort(crowding_distances)
    l = len(fronts[i])
    N = l - (population_size - new_population_count)


    for j in range(l-N):
        new_population[new_population_count] = combined_population[fronts[i][sort_by_distance[l-1-j]]]
        new_population_count += 1
    p.population = new_population
    costs = c.find_costs(p.population)
    p = genetic_operators.recombination(p)
    p.offspring = genetic_operators.mutation(p.offspring, p.constraints)
    costs_offspring = c.find_costs(p.offspring)
    print("Done computing generation number " + str(num_generations - generation_count))

plt.title("Generation" + str(num_generations - generation_count))
plt.xlabel('Sensor area', fontsize=15)
plt.ylabel('Sensor noise(scaled)', fontsize=15)
plt.scatter(costs[:, 0], costs[:, 1])
plt.show()
print("")
print("Time for execution of algorithm was " + str(time.time() - t) + " seconds")

#if np.any(costs==0):
#    print(costs)
#    print(p.population)

