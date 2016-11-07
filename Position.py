
class Position():

    _position = None

    def __init__(x, y, pos=None):
        if pos is None:
            _position = (x, y)
        else:
            _position = pos

    def getPositionRelativeTo(self, other):
        """
        Get the Position of the `other` Position relative to `self`
        :param other: Position
            The position desired in relative terms
        :return: Position
            A tuple (x,y) describing the relative Position
        """
        return ((self._position[0] - other._position[0]), (self._position[1] - other._position[1]))

    def getPositionAbsolute(self, other):
        """
        Get the absolute value of a Position `other`,
        described relative to self.
        :param other: Position
            A position described relative to self
        :return: Position
            An absolute Position
        """
        # Very not sure about this:
        self.getPositionRelativeTo(other)
