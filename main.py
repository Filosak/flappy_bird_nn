from flappy import game_class
from nn import Network
import numpy as np
import random

# vars
population = 10
nns = []
for _ in range(population):
    nns.append(Network())
game = game_class(population, nns)

def copy(one_nn):
    network = []

    for layer in one_nn.setup:
        network.append(np.matrix.copy(layer.weights))

    return network


for i in range(50):
    parents = list(game.start().values())[population-3:]
    parents_distance_sum = np.sum(np.array(parents)[:, 1])

    fitness = []
    curr_sum = 0
    for parent in parents:
        curr_fittnes = parent[1] / parents_distance_sum
        fitness.append([parent[0], curr_fittnes + curr_sum])
        curr_sum += curr_fittnes

    children = []
    for i in range(10):
        r_num = random.randint(0, 1)

        for fit in fitness:
            if fit[1] < r_num:
                continue

            copied_nn = copy(fit[0])
            children.append(Network(copied_nn))
            break

    game.networks = children