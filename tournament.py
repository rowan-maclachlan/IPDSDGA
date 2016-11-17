#!/usr/bin/env python2

import sys
import json

# Default parameters
params = dict()
params['random_seed'] = 0
params['number_of_cells'] = 2
params['number_of_iterations'] = 8
params['number_of_generations'] = 1

# Load parameter file if 
if len(sys.argv) == 2:
    with open(sys.argv[1]) as f:
        params.update(json.load(f))

print("parameters: " + str(params))

import random
from uuid import uuid4 
from copy import deepcopy
from Cell import Cell
from Position import Position

random.seed(params['random_seed'])

def create_cell(generation_index, cell_index, parent_a=None, parent_b=None):
    return Cell(uuid4().int, Position(generation_index, cell_index), parent_a, parent_b)

generation = [[create_cell(0, i) for i in range(params['number_of_cells'])]]

def tournament(cells):
    neighbours = dict()
    for cell in cells:
        cell.clearScore()
        neighbours[cell] = set([c for c in cells if c is not cell])

    for i in range(params['number_of_iterations']):
        for cell in cells:
            cell.clearInteractions()

        for cell in cells:
            cell.interact(neighbours[cell])

tournament(generation[0])

def next_generation(cells):
    boundary = params['number_of_cells'] / 2
    survivors = cells[:boundary]

    for i in range(boundary):
        survivors.append(create_cell(
                1,
                i, 
                survivors[random.randint(0, boundary - 1)],
                survivors[random.randint(0, boundary - 1)]
            )
        )

    return survivors


for i in range(params['number_of_generations']):
        tournament(generation[i])
        generation[i].sort(key=lambda c: -c._score)
        generation.append(next_generation(generation[i]))

generation[-2].sort(key=lambda c: c._score)
for cell in generation[-2]:
   print(cell)

