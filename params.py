import json
import random

params = dict()

params['random_seed'] = 0

params['surface'] = {
    'width': 20,
    'height': 20,
}

params['generations'] = 200
params['interactions'] = 20

params['score_matrix'] = {
    'c': { 'c': 3, 'd': 0 },
    'd': { 'c': 5, 'd': 1 }
}
params['loss_per_tick'] = 2.5
params['initial_score'] = 20

params['default_memory_size'] = 3

params['mutation_chance_insert'] = 0.1
params['mutation_chance_delete'] = 0.1
params['mutation_chance_flip'] = 0.2

params['move_chance'] = 0.1
params['move_ratio'] = 0.1

params['reproduction_ratio'] = 0.05

def get_score(me, them):
    return score_matrix[me][them]


def init(path):
    if path != None:
        with open(path) as f:
            params.update(json.load(f))

    random.seed(params['random_seed'])

    print("parameters: {}".format(params))
