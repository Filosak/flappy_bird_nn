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

for i in range(100000):
    parents = list(game.start().values())[population-3:]

    fitness = []
    curr_sum = 0
    for parent in parents:
        curr_fittnes = parent[1] - parent[2]

        if curr_fittnes <= 0 or parent[1] - parent[2] <= 0:
            continue

        fitness.append([parent[0], (curr_fittnes / 1000)**2 + curr_sum])
        curr_sum += (curr_fittnes / 1000)**2

    if not fitness:
        children = []
        for _ in range(population):
            children.append(Network())
    else:
        children = [parents[-1][0]]
        for i in range(population-1):
            r_num = random.uniform(0.0, curr_sum)

            for fit in fitness:
                if fit[1] < r_num:
                    continue

                copied_nn = copy(fit[0])
                children.append(Network(copied_nn))
                break

    game.networks = children