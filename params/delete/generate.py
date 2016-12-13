#!/usr/bin/env python3

import json

def write(params, name):
    with open(name, 'w+') as f:
        json.dump(params, f, indent=4, sort_keys=True)

if __name__ == '__main__':
    params = {}
    name = "delete_{f}_{seed}.json"
    for seed in range(10):
        params['random_seed'] = seed
        for f in range(0, 105, 5):
            params['mutation_chance_delete'] = f / 100.0
            write(params, name.format(f=f,seed=seed))
