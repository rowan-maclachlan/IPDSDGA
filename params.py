import json
import random

params = dict()

params['random_seed'] = 0

params['surface'] = {
    'width': 20,
    'height': 20,
}

params['generations'] = 200
params['interactions'] = 10

params['score_matrix'] = {
    'c': { 'c': 3, 'd': 0 },
    'd': { 'c': 5, 'd': 1 }
}
params['loss_per_tick'] = 2
params['initial_score'] = 50

params['default_memory_size'] = 3

params['mutation_chance_insert'] = 0.05
params['mutation_chance_delete'] = 0.05
params['mutation_chance_flip'] = 0.05


def get_score(me, them):
    return score_matrix[me][them]


def init(path):
    with open(path) as f:
        params.update(json.load(f))

    random.seed(params['random_seed'])

    print("parameters: {}".format(params))
