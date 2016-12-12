#!/usr/bin/env python3

from plotly import offline as py
from plotly import graph_objs as go
import json
import glob
import collections

if __name__ == '__main__':
    import sys

    # Assign a list with 10 indices: 1 for every bleed 2.0 - 2.9
    avg_slopes = collections.OrderedDict()

    for bleed in range(10):
        # Get the pathnames of all files of a 
        # particular bleed for every seed.
        this_glob = "./vary_bleed_[0-9]_" + str(bleed) + "_*"
        path_names = glob.glob( this_glob )
        # reset the avg slope for the new calculation
        avg_slope = 0
        if( len(path_names) != 10 ):
            exit()
        for p in path_names:
            p += "/data.json"
            with open( p, 'r' ) as json_file:
                data = json.load( json_file )
                init = data[0]['rule_frac_tfts']
                fin = data[len(data)-1]['rule_frac_tfts']
            avg_slope += (fin - init)
        avg_slopes[ 2.0 + (bleed/10) ] = ((avg_slope/10)/100)

    
    trace = go.Scatter(
            x = list(avg_slopes.keys()),
            y = list(avg_slopes.values()),
            mode = 'lines+markers',
            name = 'Bleed vs Avg. Slope of TFT Population'
            )

    data = {
            'x' : avg_slopes.keys(),
            'y' : avg_slopes.values(),
            'mode' : 'lines+markers',
            'name' : 'Bleed vs Avg. Slope of TFT Population'
            }

    py.plot( [trace], filename='bleed_vs_tft_pop' )
