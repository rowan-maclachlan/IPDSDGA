import random
import Gene

class Cell():

    _gene = None
    _score = 0

    def __init__(self, parentCell1=None, parentCell2=None):
        # generate a gene to match specifications
        if parentCell1 is not None and parentCell2 is not None:
            self._gene = Gene.Gene(parentCell1._gene, parentCell2._gene)
        else:
            self._gene = Gene.Gene()

    def reproduce(self, partner):
        """
        Produce a new Cell by combining this cell and another
        :param partner: another Cell
        :return: a new Cell
        """
        return Cell(self, partner)

    def __str__(self):
        display = str(self._gene)
        display += "\nScore: "
        display += str(self._score)
        return display

