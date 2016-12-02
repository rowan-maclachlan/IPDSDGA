import json
import copy

base = {
    'surface': {
        'height': 10,
        'width': 10
    }
}

for seed in range(0, 8):
    params = copy.deepcopy(base)
    params['random_seed'] = seed
    with open('small_{}.json'.format(seed), 'w+') as f:
        json.dump(params, f, indent=4, sort_keys=True)
