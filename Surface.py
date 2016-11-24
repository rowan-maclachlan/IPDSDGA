from Cell import Cell
from Position import Position
import statistics as stats
import random

neighbour_offsets = [Position(-1,-1), Position( 0,-1), Position( 1,-1),
                     Position(-1, 0), Position( 0, 0), Position( 1, 0),
                     Position(-1, 1), Position( 0, 1), Position( 1, 1)]

class Surface:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._all_cells = set()
        self.map = [];
        for i in range(height):
            self.map.append([ None ] * width)

    def get(self, pos):
        return self.map[(self.height + pos.y) % self.height][(self.width + pos.x) % self.width]

    def set(self, pos, cell):
        if cell == None:
            self._all_cells.remove(self.map[pos.y][pos.x])
        else:
            self._all_cells.add(cell);
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
            neighbour = self.get(cell.current_position + offset)
            if neighbour != None:
                neighbours.add(neighbour)
        return neighbours
    
    def get_empty_neighbour_position(self, cell):
        candidates = []
        for offset in neighbour_offsets:
            neighbour = self.get(cell.current_position + offset)
            if neighbour == None:
                candidates.append(cell.current_position + offset)
        if len(candidates) == 0:
            return None
        return random.choice(candidates)

    def __interaction_tick(self):
        self.__map(lambda c: c.clear_interactions())
        self.__map(lambda c: c.interact(self.get_neighbours(c)))
    
    def __death_tick(self):
        self.__map(lambda c: self.set(c.current_position, None if c._score <= 0 else c))
    
    def reproduction_tick(self):
        ratio = 0.25 # TODO: move to paramater
        top_cells = sorted(self._all_cells, key=lambda c: -c._score)[:round(len(self._all_cells) * ratio)]
        chosen_cells = set()

        for cell in top_cells:
            if not cell in chosen_cells:
                # find best neighbour
                open_position = self.get_empty_neighbour_position(cell)
                if open_position == None:
                    continue
                neighbours = self.get_neighbours(cell)
                best_neighbour = max(neighbours, key=lambda c: -c._score)
                if not best_neighbour in chosen_cells:
                    chosen_cells.add(cell)
                    chosen_cells.add(best_neighbour)
                    self.set(open_position, Cell(
                        cell._id + best_neighbour._id,
                        open_position,
                        cell,
                        best_neighbour
                    ))


        print("-" * 80)

    def __movement_tick(self):
        pass

    def tick(self):
        self.__interaction_tick()
        self.__death_tick()
        #self.__reproduction_tick()
        self.__movement_tick()

    def draw(self):
        pass

    def __str__(self):
        out = ""
        for y in range(self.height):
            for x in range(self.width):
                out += "c" if self.get(Position(x,y)) != None else " "
            out += "\n"
        return out




if __name__ == "__main__":  
    surface = Surface(5, 5);
    cells = []
    for i in range(25):
        cells.append(Cell(i, Position(i // 5, i % 5)))
    for cell in cells:
        surface.set(cell.current_position, cell)

    print(surface)

    for i in range(10):
        surface.tick()
        surface.reproduction_tick()
        print(surface)


