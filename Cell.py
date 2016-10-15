import random
import Gene

class Cell():

    _gene = None
    _score = 0

    def __init__(self, parentCell1=None, parentCell2=None):
        # generate a gene to match specifications
        if parentCell1 is None or parentCell2 is None:
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
        string = self._gene.DisplayGene()
        string += "\nScore: " + str(self._score)
        print string

