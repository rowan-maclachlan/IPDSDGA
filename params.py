"""
This module serves as a repository for
simulation parameters.  Dictionary values can 
be overwritten for any particular simulation run
to enable changing parameter values all across
the simulation.  Otherwise, changing parameter values
would require navigating to any number of other files.
"""

import json
import random

""" 
keys are the names of model parameters.
values are particular simulation parameter values.
"""
params = dict()

""" Copied and varied to allow for reproducible results """
params['random_seed'] = 0

""" The size of the surface """
params['surface'] = {
    'width': 20,
    'height': 20,
}

""" The number of generations to run the simulation """
params['generations'] = 300
""" The number of interactions with neighbours per generation """
params['interactions'] = 10

"""
The payoff matrix for the iterated prisoner's dilemma.
General rules should be followed:
    T > R > P > S and
    ( T + P ) / 2 < R
where 
    T = 5, ( 5 - cost )
    R = 3, ( 3 - cost )
    P = 1, ( 1 - cost ), and
    S = 0  ( 0 - cost )
"""
params['score_matrix'] = {
    'c': { 'c': 3, 'd': 0 },
    'd': { 'c': 5, 'd': 1 }
}
""" Cell score loss per interaction """
params['loss_per_tick'] = 2.5
""" The base score of a cell at the start of a generation """
params['initial_score'] = 20

""" The initial size of Gene sequence is
between 2^2 and 2^3. """
params['default_memory_size'] = 3

""" The chance of a particular choice being 
inserted into a gene """
params['mutation_chance_insert'] = 0.1

""" The chance of a particular choice being 
deleted from a gene. """
params['mutation_chance_delete'] = 0.1

""" The chance of a particular choice 
being flipped from one to the other. """
params['mutation_chance_flip'] = 0.1

""" The probability that a poorly performing cell will move """
params['move_chance'] = 0.2

""" The fraction of a population that may move """
params['move_ratio'] = 0.2

""" The fraction of the population that may reproduce """
params['reproduction_ratio'] = 0.05
""" The age at which cells die """
params['age_of_death'] = 20
""" Whether or not the simulation is being run with ageing """
params['ageing'] = False

"""
Retrieve the score from the score matrix.
:param me: The choice of the calling Cell
:type me: char
:param them: The choice of the calling Cell's neighbour
:type them: char
:return: The score of the two choices
:rtype: int
"""
def get_score(me, them):
    return params['score_matrix'][me][them]

def init(path):
    if path is not None:
        with open(path) as f:
            params.update(json.load(f))

    random.seed(params['random_seed'])

    print("parameters: {}".format(params))

if __name__ == "__main__":
    with open('params/default.json', 'w+') as f:
        json.dump(params, f, sort_keys=True, indent=4)
        f.write('\n')
