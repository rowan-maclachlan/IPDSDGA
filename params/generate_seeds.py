#!/usr/bin/env python3

import json
import copy

if __name__ == '__main__':
    import sys

    base = {
        'surface': {
            'height': int(sys.argv[2]),
            'width': int(sys.argv[2])
        }
    }

    for seed in range(0, 8):
        params = copy.deepcopy(base)
        params['random_seed'] = seed
        with open('{}_{}.json'.format(sys.argv[1], seed), 'w+') as f:
            json.dump(params, f, indent=4, sort_keys=True)
