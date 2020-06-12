'''
This file defines functions specific to NSGA-II. 
Namely, the fast non dominated sorting, and crowding distance calculation functions have been implemented 
'''
import numpy as np
import matplotlib.pyplot as plt

def magnitude(x):
    if x>=0:
        return x
    else:
        return -1*x

# The function below carries out the fast non-dominated sorting, input is a numpy array of values of objective functions 
def non_dominated_sorting(costs):
    # costs is a numpy array with dimensions (population_size, num_objectives)
    # Returns a 1D array with domination count (number of solutions that dominate a given soln), and a list of lists of solutions that each solution dominates
    list_of_dominated_solutions = [[] for i in range(costs.shape[0])]
    front = []  # front[0] is the pareto optimal front, and so on
    current_front_solutions = []
    next_front_solutions = []
    rank = np.zeros(costs.shape[0])
    domination_count = np.zeros(costs.shape[0])
    
    for i in range(costs.shape[0]):
        for j in range(1, costs.shape[0] - i):
            if costs[i][0] <= costs[i + j][0] and costs[i][1] <= costs[i + j][1]:
                # This means, soln_i dominates soln_i+j
                #print(str(i) + " dominates " + str(i+j))
                domination_count[i+j] += 1
                list_of_dominated_solutions[i].append(i+j)
            elif costs[i][0] >= costs[i + j][0] and costs[i][1] >= costs[i + j][1]:
                # This means, soln_i+j dominates soln_i
                #print(str(i+j) + " dominates " + str(i))
                domination_count[i] += 1
                list_of_dominated_solutions[i+j].append(i)
            else:
                # Neither solution dominates the other
                pass
        if domination_count[i]==0:
            current_front_solutions.append(i)
            #rank[i] = 0 # This is not like in the algorithm, but will be used here, to comply with python notation
    front.append(current_front_solutions)
    i = 0
    while(1):
        if(len(front[i]) == 0):
            break
        next_front_solutions = []
        for j in range(len(front[i])):
            for k in range(len(list_of_dominated_solutions[front[i][j]])):
                domination_count[list_of_dominated_solutions[front[i][j]][k]] -= 1
                if domination_count[list_of_dominated_solutions[front[i][j]][k]] == 0:
                    #rank[domination_count[list_of_dominated_solutions[front[i][j]][k]]] = i + 1
                    next_front_solutions.append(list_of_dominated_solutions[front[i][j]][k])
        
        front.append(next_front_solutions)
        i += 1
    return front

# The function below calculates the crowding distance for all solutions in the given front
def calculate_crowding_distance(costs, front, num_objectives):
    assert(costs.shape[1] == num_objectives)
    l = len(front)

    dist = np.zeros(l)
    costs_new = np.zeros((l, num_objectives))
    for i in range(l):
        for j in range(num_objectives):
            costs_new[i][j] = costs[front[i]][j]
    for i in range(num_objectives):
        sorted_indices = np.argsort(costs_new[:,i])
        dist[sorted_indices[0]] = dist[sorted_indices[l-1]] = 100
        for j in range(1,l-1):
            dist[sorted_indices[j]] += magnitude((costs_new[sorted_indices[j+1]][i] - costs_new[sorted_indices[j-1]][i]))/magnitude((costs_new[:, i:i+1].min() - costs_new[:, i:i+1].max()))
    return dist