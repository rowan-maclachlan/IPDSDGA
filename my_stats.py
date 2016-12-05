import Surface
import Cell as c
import Gene as g
import statistics as s

def init_move_stats(surface, stats):
    # get initial move statistics
    if 0 != surface.population:
        initial_moves = list()
        surface.my_map(
            lambda c: initial_moves.append(
                c.get_gene().get_choice_at(1)))
    
        init_move_frac = 0
        for move in initial_moves:
            if 'd' is move:
                init_move_frac += 1
        init_move_frac = float(init_move_frac)/len(initial_moves)
        
        stats['init_move_frac'] = init_move_frac
    else:
        stats['init_move_frac'] = None

def fraction_def_stats(surface, stats):
    # get gene defection fraction stats
    if 0 != surface.population:
        fraction_defect = list()

        surface.my_map(
                lambda c: fraction_defect.append(
                    c.get_gene().get_defect_fraction()))
        mean = s.mean(fraction_defect)
        try:
            mode = s.mode(fraction_defect)
        except s.StatisticsError:
            mode = None
        stddev = s.pstdev(fraction_defect, mean)
    else:
        mean = None
        mode = None
        stddev = None

    stats['mean_def_frac'] = mean
    stats['mode_def_frac'] = mode
    stats['stddev_def_frac'] = stddev

def gene_length_stats(surface, stats):

    if 0 != surface.population:
        lengths = list()
        surface.my_map(lambda c: lengths.append(len(c.get_gene().get_seq())-1))
        mean = s.mean(lengths)
        try:
            mode = s.mode(lengths)
        except s.StatisticsError:
            mode = None
        stddev = s.pstdev(lengths, mean)
    else:
        mean = None
        mode = None
        stddev = None

    stats['mean_length'] = mean
    stats['mode_length'] = mode
    stats['stddev_length'] = stddev

def get_score_stats(surface, stats):
    if 0 != surface.population:
        scores = list()
        surface.my_map(lambda c: scores.append(c.get_score()))
        mean = s.mean(scores)
        try:
            mode = s.mode(scores)
        except s.StatisticsError:
            mode = None
        stddev = s.pstdev(scores, mean)
    else:
        mean = None
        mode = None
        stddev = None

    stats['mean_scores'] = mean
    stats['mode_scores'] = mode
    stats['stddev_scores'] = stddev

def get_age_stats(surface, stats):
    if 0 != surface.population:
        ages = list()
        surface.my_map(lambda c: ages.append(c.get_age()))
        mean = s.mean(ages)
        try:
            mode = s.mode(ages)
        except s.StatisticsError:
            mode = None
        stddev = s.pstdev(ages, mean)
    else:
        mean = None
        mode = None
        stddev = None

    stats['mean_age'] = mean
    stats['mode_age'] = mode
    stats['stddev_age'] = stddev

def get_rule_stats(surface, stats):
    if 0 != surface.population:
        num_tfts = 0
        for c in surface.get_all():
            if c.is_tft():
                num_tfts += 1
            # elif ...
        frac_tfts = float(num_tfts)/surface.population
    else:
        frac_tfts = None

    stats['frac_tfts'] = frac_tfts * 100.0

def get_stats(surface):
    """
    Retrieve statistics about the Surface and the
    Cellular population.
    :return: dict() A dictionary full of statistics
    """
    stats = dict()
   
    stats['population'] = surface.population
    init_move_stats(surface, stats)
    fraction_def_stats(surface, stats)
    gene_length_stats(surface, stats)
    get_score_stats(surface, stats)
    get_rule_stats(surface, stats)
    get_age_stats(surface, stats)

    return stats
    
def output_plot(path, data):
    from plotly import offline as py
    from plotly import graph_objs as go

    plot_data = {}
    for key in data[0].keys():
        plot_data[key] = {
            'x': [],
            'y': [],
            'mode': 'lines+markers',
            'name': key
        }

    for i, d in enumerate(data):
        for k, v in d.items():
            plot_data[k]['x'].append(i)
            plot_data[k]['y'].append(v)

    to_plot = []
    for k in sorted(plot_data.keys()):
        to_plot.append(go.Scatter(plot_data[k]))

    py.plot(to_plot, filename=path, auto_open=False)

