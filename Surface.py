from Cell import Cell
from Position import Position
import random

import my_stats as s 
import params as p

neighbour_offsets = [Position(-1,-1), Position( 0,-1), Position( 1,-1),
                     Position(-1, 0), Position( 0, 0), Position( 1, 0),
                     Position(-1, 1), Position( 0, 1), Position( 1, 1)]


class Surface:
    def __init__(self, width, height):
        self.population = 0
        self.width = width
        self.height = height
        self._all_cells = set()
        self.map = []
        self.ID = 0
        self.total_alive = width * height
        self.total_dead = 0
        for i in range(height):
            self.map.append([ None ] * width)

    def get_all(self):
        living_cells = list()
        for y in range(self.height):
            for x in range(self.width):
                if self.get(Position(x, y)) is not None:
                    living_cells.append(self.get(Position(x, y)))
        return living_cells

    def get(self, pos):
        return self.map[(self.height + pos.y) % self.height][(self.width + pos.x) % self.width]

    def set(self, pos, c):
        if c is None:
            self._all_cells.remove(self.get(pos))
        else:
            self._all_cells.add(c)
        self.map[(self.height + pos.y) % self.height][(self.width + pos.x) % self.width] = c

    def my_map(self, method):
        for column in self.map:
            for c in column:
                if c is not None:
                    method(c)

    def get_neighbours(self, cell):
        neighbours = set()
        for offset in neighbour_offsets:
            neighbour = self.get(cell.get_position() + offset)
            if neighbour is not None:
                neighbours.add(neighbour)
        return neighbours
    
    def get_empty_neighbour_position(self, c):
        """
        Return the _position of a neighbouring empty cell
        :param c: A cell
        :return: A random open _position from among neighbouring
        open _position, or None if there are no open positions.
        """
        candidates = []
        for offset in neighbour_offsets:
            neighbour = self.get(c.get_position() + offset)
            if neighbour is None:
                candidates.append(c.get_position() + offset)
        if len(candidates) == 0:
            return None
        return random.choice(candidates)

    def __interaction_tick(self):
        self.my_map(lambda c: c.interact(self.get_neighbours(c)))
    
    def __death_tick(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x][y] is not None:
                    if self.map[x][y].is_dead():
                        self.map[x][y] = None
                        self.population -= 1
                        self.total_dead += 1
    
    def __reproduction_tick(self):
        ratio = p.params['reproduction_ratio']        
        top_cells = sorted(
                self._all_cells, 
                key=lambda c: -c.get_score())[:round(len(self._all_cells) * ratio)]
        chosen_cells = set()

        for c in top_cells:
            if c not in chosen_cells:
                # find best neighbour
                open_position = self.get_empty_neighbour_position(c)
                if open_position is None:
                    continue
                neighbours = self.get_neighbours(c)
                if 0 == len(neighbours):
                    continue
                best_neighbour = max(neighbours, key=lambda c: -c.get_score())
                if best_neighbour not in chosen_cells:
                    chosen_cells.add(c)
                    chosen_cells.add(best_neighbour)
                    self.set(open_position, Cell(
                        self.ID,
                        open_position,
                        c,
                        best_neighbour
                    ))
                    self.ID += 1
                    self.population += 1
                    self.total_alive += 1

    def __move_cell(self, c, destination):
        """ 
        Move the Cell 'c' to the its destination.  Set its current
        position to none, set its new position to destination,
        and set the map slot at 'destination' to hold the cell 'c'.
        """
        destination.x = (destination.x + self.width) % self.width
        destination.y = (destination.y + self.height) % self.height
        self.set(c.get_position(), None)
        c.set_position(destination)
        self.set(destination, c)

    def __movement_tick(self):
        """
        This method could be expanded in functionality to encourage moving
        when performing poorly.  Right now it will just have a random chance
        to move.
        :return:
        """
        move_chance = p.params['move_chance']        
        # shuffle so that priority is not given to cells at map[0][0]
        # This could be made to favour well performing cells
        live_cells = self.get_all()
        random.shuffle(live_cells)
        for c in live_cells:
            if random.random() > move_chance:
                continue
            # find neighbouring open spots
            open_position = self.get_empty_neighbour_position(c)
            # If there is a _position, move the cell c from
            # its current _position to its new _position
            if open_position is not None:
                self.__move_cell(c, open_position)

    def __alt_movement_tick(self):
        """
        This method accomplishes the same as the __movement_tick,
        only Cells are more likely to move if they are performing
        poorly.
        """
        ratio = p.params['move_ratio']
        move_chance = p.params['move_chance']
        # get the bottom 'ratio' cells
        all_cells = self.get_all()
        sorted_cells = sorted(all_cells, key=lambda c: c.get_score())
        bottom_cells = sorted_cells[:round(len(all_cells) * ratio)]
        # check if poorly performing cell will move
        for c in bottom_cells:
            if random.random() > move_chance:
                continue
            open_position = self.get_empty_neighbour_position(c)
            # If there is a _position, move the cell c from
            # its current _position to its new _position
            if open_position is not None:
                self.__move_cell(c, open_position)

    def get_best_x(self, ratio):
        """
        Return the best 'ratio' percent of Cells
        """
        all_cells = self.get_all()
        sorted_cells = sorted(all_cells, key=lambda c: -c.get_score())
        return sorted_cells[:round(len(all_cells) * ratio)]

    def __age_tick(self):
        self.my_map(lambda c: c.age())

    def tick(self, inters):
        """
        Run a tick.  Reset scores and memories, and run
        the interaction tick, death tick, and movement tick
        for inters times.  Then, run the reproduction tick.
        :param inters: int the number of interactions per tick
        :return: None
        """
        self.__clean()
        if p.params['ageing']:
            self.__age_tick()
        for x in range(inters):
            self.__interaction_tick()
            self.__death_tick()
            self.__alt_movement_tick()
        self.__reproduction_tick()

    def __clean(self):
        """
        Clear and reset the scores of all Cells alive
        :return:
        """
        self.my_map(lambda c: c.clear_interactions())
        self.my_map(lambda c: c.reset_score())

    def draw(self):
        pass

    def __str__(self):
        out = "*"
        for x in range(self.width):
            out += "-----"
        out += "*\n"
        for y in range(self.height):
            out += "|"
            for x in range(self.width):
                c = self.get(Position(x, y))
                if c is None:
                    out += "     "
                else:
                    out += c.draw() + " "
            out += "|\n"
        out += "*"
        for x in range(self.width):
            out += "-----"
        out += "*\n"
        out += " | population: "    + str(self.population) \
                + " | born: "       + str(self.total_alive) \
                + " | died: "       + str(self.total_dead) + "\n"
        
        return out

if __name__ == "__main__":
    import sys
    import json
    from time import strftime

    start = strftime("%Y-%m-%dT%H:%M:%S")

    if len(sys.argv) == 2:
        p.init(sys.argv[1])
    else:
        p.init(None)

    surface_w = p.params['surface']['width']
    surface_h = p.params['surface']['height']
    gens = p.params['generations']
    interactions = p.params['interactions']

    surface = Surface(surface_w, surface_h)

    for i in range(surface_w * surface_h):
        c_init = Cell(surface.ID, Position(i // surface_w, i % surface_h))
        surface.ID += 1
        surface.population += 1
        surface.set(c_init.get_position(), c_init)
    
    sim_stats = list()

    for i in range(gens):
        print(surface)
        surface.tick(interactions)
        sim_stats.append(s.get_stats(surface))

    for c in surface.get_best_x(0.02):
        print(str(c))

    with open("out/" + start + ".json", "w+") as out:
        json.dump(sim_stats, out, indent=4)


