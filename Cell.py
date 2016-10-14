import random
import Gene

class Cell():

    _gene = None
    _score = 0

    def __init__(self, gene=None):
        # generate a gene to match specifications
        if gene is not None:
            self._geneticCode = gene
        else:
            self._geneticCode = Gene.Gene()

    def isAlive(self):
        return True

    def reproduce(self, partner):
        """
        Produce a new Cell by combining this cell and another
        :param partner: another Cell
        :return: a new Cell
        """
        newGene = Gene(self, partner)
        newCell = Cell(newGene)
        return newCell

    def __str__(self):
        string = self._gene.DisplayGene()
        string += "\nScore: " + str(self._score)
        print string

