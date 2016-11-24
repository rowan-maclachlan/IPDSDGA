from Position import Position
import statistics as stats

neighbour_offsets = [Position(-1, 1), Position( 0, 1), Position( 1, 1),
                     Position(-1, 0), Position( 0, 0), Position( 1, 0),
                     Position(-1,-1), Position( 0,-1), Position( 1,-1)]


class Surface:
    def __init__(self, width, height):
        self.map = [ [ None ] * width ] * height

    def get(self, pos):
        return self.map[pos.y % self.height][pos.x % self.width]

    def set(self, pos, cell):
        self.map[pos.y % self.height][pos.x % self.width] = cell

    def __map(self, method):
        for column in self.map:
            for cell in column:
                if cell != None:
                    method(cell)

    def get_scores(self):
        cells = set()
        self.__map(lambda c: cells.add(c.get_score()))
        return cells

    def get_avg_defection_stats(self):
        """
        Get the statistics for the fraction of defect choice in Cells' genes
        :return: mean, mode, stddev
        """
        fraction_defect = set()
        self.__map(lambda c: fraction_defect.add(c.get_gene().get_defect_fraction()))
        mean_def_fraction = stats.mean(fraction_defect)
        mode_def_fraction = stats.mode(fraction_defect)
        stddev_def_fraction = stats.pstdev(fraction_defect, mean_def_fraction)

        return mean_def_fraction, mode_def_fraction, stddev_def_fraction

    def get_init_move_stats(self):
        """
        Get the statistics for the initial move of the Cells
        :return: mean, mode, stddev
        """
        initial_move = set()
        self.__map(lambda c: initial_move.add(c.get_gene().get_choice_at(1)))
        mean_init_fraction = stats.mean(initial_move)
        mode_init_fraction = stats.mode(initial_move)
        stddev_init_fraction = stats.pstdev(initial_move, mean_init_fraction)

        return mean_init_fraction, mode_init_fraction, stddev_init_fraction


    def get_neighbours(self, cell):
        neighbours = set()
        for offset in neighbour_offsets:
            neighbour = self.get(cell.position + offset)
            if neighbour != None:
               neighbours.add(self.get(cell.position + offset))

        return neighbours

    def __interaction_tick(self):
        self.__map(lambda c: c.clear_interractions())
        self.__map(lambda c: c.interract(self.get_neighbours(c)))
    
    def __death_tick(self):
        self.__map(lambda c: self.set(c.position, None if c.is_dead() else c))
    
    def __reproduction_tick(self):
        pass

    def __movement_tick(self):
        pass

    def tick(self):
        self.__interaction_tick()
        self.__death_tick()
        self.__reproduction_tick()
        self.__movement_tick()

    def draw(self):
        pass


