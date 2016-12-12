#!/usr/bin/env python3

import json
import copy

if __name__ == '__main__':
    import sys

    params = {}
    name = "vary_bleed"

    for seed in range(0, 10):
        for x in range(0, 10):
            params['random_seed'] = seed
            params['loss_per_tick'] = 2.0 + float(x) / 10
            with open('{}_{}_{}.json'.format(name, seed, x), 'w+') as f:
                json.dump(params, f, indent=4, sort_keys=True)
