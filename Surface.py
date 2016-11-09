from Position import Position

neighbour_offsets = [Position(-1, 1), Position( 0, 1), Position( 1, 1),
                     Position(-1, 0), Position( 0, 0), Position( 1, 0),
                     Position(-1,-1), Position( 0,-1), Position( 1,-1)]

class Surface:
    def __init__(self, width, height):
        self.map = [ [ None ] * width ] * height

    def get(self, pos):
        return self.map[pos.y % self.height][pos.x % self.width]

    def set(self, pos, cell):
        return self.map[pos.y % self.height][pos.x % self.width] = cell

    def __map(self, method):
        for column in self.map:
            for cell in column:
                if cell != None:
                    method(cell)

    def get_scores(self):
        cells = set()
        self.__map(lambda c: cells.add(c.get_score()))
        return cells

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
        self.__map(lambda c: self.set(c.position, c if c.score > 0 else None))
    
    def __reproduction_tick(self):
        pass

    def tick(self):
        self.__interaction_tick()
        self.__death_tick()
        self.__reproduction_tick()

    def draw(self):
        pass


