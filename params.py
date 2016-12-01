import json
import random

params = dict()

params['random_seed'] = 0

params['surface'] = {
    'width': 30,
    'height': 30,
}

params['generations'] = 300
params['interactions'] = 10

params['score_matrix'] = {
    'c': { 'c': 3, 'd': 0 },
    'd': { 'c': 5, 'd': 1 }
}
params['loss_per_tick'] = 2
params['initial_score'] = 20

params['default_memory_size'] = 3

params['mutation_chance_insert'] = 0.2
params['mutation_chance_delete'] = 0.2
params['mutation_chance_flip'] = 0.2

params['move_chance'] = 0.1
params['move_ratio'] = 0.1

params['reproduction_ratio'] = 0.05

params['aging'] = False
params['age_of_death'] = 10

def get_score(me, them):
    return params['score_matrix'][me][them]


def init(path):
    if path is not None:
        with open(path) as f:
            params.update(json.load(f))

    random.seed(params['random_seed'])

    print("parameters: {}".format(params))
