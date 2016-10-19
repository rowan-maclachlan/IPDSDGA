import Gene
import Cell
import numpy as np
import random

if __name__ == "__main__":

    cellA = Cell.Cell()
    cellB = Cell.Cell()

    print str(cellA)
    print str(cellB)

    cellC = Cell.Cell(cellA, cellB)
    cellD = Cell.Cell(cellA, cellB)

    print str(cellC)
    print str(cellD)

