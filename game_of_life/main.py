import pyglet 
from random import randint

creature_size = 5

world_width = 100
world_height = 100

dot = pyglet.image.create(
    width=5,
    height=5,
    pattern=pyglet.image.SolidColorImagePattern(
        color=(255, 255, 255, 0)
    )
)

class World:
    def __init__(self, width, height):
        self.width = width;
        self.height = height;
        self.map = self.__create(lambda: True if randint(0, 8) == 0 else None)

    def __create(self, gen):
        return [[gen() for x in range(self.width)] for y in range(self.height)]

    def spawn(self, chance):
        return True if randint(0, chance) == 0 else None

    def get(self, x, y):
        return self.map[x % self.width][y % self.height]

    def get_value(self, x, y):
        return 1 if self.get(x, y) else 0

    def get_neighbour_count(self, x, y):
        return self.get_value(x-1, y+1) \
             + self.get_value(x  , y+1) \
             + self.get_value(x+1, y+1) \
             + self.get_value(x-1, y  ) \
             + self.get_value(x+1, y  ) \
             + self.get_value(x-1, y-1) \
             + self.get_value(x  , y-1) \
             + self.get_value(x+1, y-1)

    def step(self):
        new_map = self.__create(lambda: None)
        for x in range(self.width):
            for y in range(self.height):
                count = self.get_neighbour_count(x, y)
                if count == 3:
                    new_map[x][y] = True
                elif count == 2 and self.get(x, y) != None:
                    new_map[x][y] = True
        self.map = new_map


    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.get(x, y) != None: 
                    dot.blit((x+1) * dot.width, (y+1) * dot.height)

if __name__ == "__main__":
    window = pyglet.window.Window(
            width=((2 + world_width) * creature_size),
            height=((2 + world_height) * creature_size)
        )

    world = World(world_width, world_height)

    @window.event
    def on_draw():
        window.clear()
        world.draw()

    def step(dt):
        window.clear()
        world.step()
        world.draw()

    pyglet.clock.schedule_interval(step, 1.0/5)
    pyglet.app.run()

