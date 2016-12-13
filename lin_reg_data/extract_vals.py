#!/usr/bin/env python3

from plotly import offline as py
from plotly import graph_objs as go
import json
import glob
import collections
import os.path as path

if __name__ == '__main__':
    import sys

    NUM_SEEDS = 10
    NUM_BLEEDS = 30
    # Assign a list with 10 indices: 1 for every bleed 2.0 - 2.9
    avg_slopes_tft = collections.OrderedDict()
    avg_slopes_alld = collections.OrderedDict()
    avg_slopes_allc = collections.OrderedDict()
    avg_slopes_init = collections.OrderedDict()

    for bleed in range( NUM_BLEEDS ):
        # Get the pathnames of all files of a 
        # particular bleed for every seed.
        this_glob = "./second/vary_bleed_s[0-9]_b" + str(bleed) + "_*"
        path_names = glob.glob( this_glob )
        # reset the avg slope for the new calculation
        avg_slope_tft = 0
        avg_slope_alld = 0
        avg_slope_allc = 0
        avg_slope_init = 0
        for p in path_names:
            p += "/data.json"
            print(p)
            if not path.isfile( p ):
                continue
            with open( p, 'r' ) as json_file:
                data = json.load( json_file )
                init_alld = data[0]['rule_frac_alld']
                fin_alld = data[len(data)-1]['rule_frac_alld']
                init_allc = data[0]['rule_frac_allc']
                fin_allc = data[len(data)-1]['rule_frac_allc']
                init_tft = data[0]['rule_frac_tfts']
                fin_tft = data[len(data)-1]['rule_frac_tfts']
                init_init = data[0]['init_move_frac']
                fin_init = data[len(data)-1]['init_move_frac']
            avg_slope_alld += (fin_alld - init_alld)
            avg_slope_allc += (fin_allc - init_allc)
            avg_slope_tft += (fin_tft - init_tft)
            avg_slope_init += (fin_init - init_init)
        avg_slopes_tft[ 1.0 + (bleed/10.0) ] = ((avg_slope_tft/10)/100)
        avg_slopes_alld[ 1.0 + (bleed/10.0) ] = ((avg_slope_alld/10)/100)
        avg_slopes_allc[ 1.0 + (bleed/10.0) ] = ((avg_slope_allc/10)/100)
        avg_slopes_init[ 1.0 + (bleed/10.0) ] = ((avg_slope_init/10)/100)

    print( "plotting..." )

    trace_tft = go.Scatter(
            x = list(avg_slopes_tft.keys()),
            y = list(avg_slopes_tft.values()),
            mode = 'lines+markers',
            name = 'Bleed vs Avg. Slope of TFT Population'
            )
    
    trace_alld = go.Scatter(
            x = list(avg_slopes_alld.keys()),
            y = list(avg_slopes_alld.values()),
            mode = 'lines+markers',
            name = 'Bleed vs Avg. Slope of all D Population'
            )

    trace_init = go.Scatter(
            x = list(avg_slopes_init.keys()),
            y = list(avg_slopes_init.values()),
            mode = 'lines+markers',
            name = 'Bleed vs Avg. Slope of all D initial move'
            )

    trace_allc = go.Scatter(
            x = list(avg_slopes_allc.keys()),
            y = list(avg_slopes_allc.values()),
            mode = 'lines+markers',
            name = 'Bleed vs Avg. Slope of all C Population'
            )

    py.plot( [trace_tft, trace_alld, trace_allc, trace_init], filename='bleed_vs_pop_frac' )
