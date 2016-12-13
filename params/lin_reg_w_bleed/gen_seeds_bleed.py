#!/usr/bin/env python3
"""
Generate 10 seeds for parameter files for
values of loss-per-tick from 1.0 to 3.9 in 0.1
step increments.
"""
import json
import copy

if __name__ == '__main__':
    import sys

    params = {}
    name = "vb"

    for seed in range(0, 10):
        for x in range(0, 30):
            params['random_seed'] = seed
            params['loss_per_tick'] = 1.0 + float(x)/10
            with open('{}_s{}_b{}.json'.format(name, seed, x), 'w+') as f:
                json.dump(params, f, indent=4, sort_keys=True)
