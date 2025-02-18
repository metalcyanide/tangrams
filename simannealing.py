import polygonrep
from sys import float_info
from shapely.geometry import Polygon, Point, LineString
from shapely import affinity
from math import sqrt, exp
import numpy as np
import random

import placement

# • Compute the difference polygon D between the target and the current solution.
# • Consider the tentative solution S
# 0
# formed by taking a random polygon P and placing it
# on D using the corner heuristic.
# • With some probability p(S, S0
# , i) (where i is the number of iterations completed so far),
# and their costs, we move from S to S
# 0

'''
Need to think about deep copy probs in simannealing solution
'''
'''

###################################### NEED TO WORK ON THIS ####################
'''
def get_initial_solution(polygons, target_polygon):
    polygons_placed, initial_sol,flip_check = placement.place_polygons_on_target(polygons, target_polygon)
    return initial_sol

def temperature_function(iteration, alpha=0.9):
    return pow(alpha, iteration)


def get_next_solution(polygons, target_polygon, solution):

    index = random.randrange(len(polygons))
    solution[3*index:3*index+3] = [0]*3
    diff_polygon = difference_polygon(polygons, target_polygon, solution)
    sequence, flip_check = placement.place_polygon_by_edge(diff_polygon, polygons[index])
    solution[3*index: 3*index+3] = sequence
    return solution

'''
############ code from here done #######################
'''
def prob_function(polygons, target_polygon, initial_solution, next_solution, iteration, alpha=0.9):
    loss_initial_solution = polygonrep.loss_function(initial_solution, polygons, target_polygon)
    loss_next_solution = polygonrep.loss_function(next_solution, polygons, target_polygon)
    temp_val = (temperature_function(iteration, alpha))
    if temp_val == 0:
        temp_val = 0.01/iteration
    prob = exp((loss_initial_solution - loss_next_solution) / temp_val)

    if prob > 1:
        return 1
    else:
        return prob


def difference_polygon(polygons, target_polygon, solution):
    transformed_polygons = polygonrep.perform_sequence(polygons, solution)
    overlay_polygons = polygonrep.union_polygons(transformed_polygons)

    diff_polygon = target_polygon.difference(overlay_polygons)

    if diff_polygon.geom_type == 'MultiPolygon':
        random_index = random.randrange(len(diff_polygon))
        diff_polygon = diff_polygon[random_index]

    return diff_polygon

def simannealing_solve(polygons, target_polygon, initial_solution, file_loc="./loss.txt"):
    iteration = 1
    solution = initial_solution
    eps = float_info.epsilon
    itr = 0
    loss = polygonrep.loss_function(solution, polygons, target_polygon)
    min_loss = loss
    f = open(file_loc, "a+")
    f.write(str(loss))
    while loss > eps:
        res = "Iteration {itr}, loss {loss}\n".format(itr = iteration, loss = loss)
        f.write(res)
        if loss < min_loss:
            print("min loss: " + str(min_loss))
            print("solution: " + str(solution))
            min_loss = loss
        itr += 1
        next_solution = get_next_solution(polygons, target_polygon, solution)
        prob = prob_function(polygons, target_polygon, solution, next_solution, iteration)
        random_num = random.random()
        if random_num < prob :
            solution = next_solution
        iteration +=1
        loss = polygonrep.loss_function(solution, polygons, target_polygon)
    f.close()

    return solution



def solve_target(polygons, target_polygon, file_loc="./loss.txt"):
    initial_sol = get_initial_solution(polygons, target_polygon)
    solution_simanneal = simannealing_solve(polygons, target_polygon, initial_sol, file_loc)
    print(solution_simanneal)

    polygonrep.vizualizer(solution_simanneal, polygons, target_polygon)

    return True

if __name__ == "__main__":

    polygons = polygonrep.create_tanpieces()
    target_polygon = polygonrep.regular_parallelogram(sqrt(8),sqrt(8), 90)
    solve_target(polygons, target_polygon)