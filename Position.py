class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return "<%s instance at %s, x: %s, y: %s>" %\
                (self.__class__.__name__, id(self), self.x, self.y)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

