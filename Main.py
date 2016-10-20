import Gene
import Cell
import numpy as np
import random

GENERATIONS = 10
SIMULATION_STEPS = 100

if __name__ == "__main__":

    cellA = Cell.Cell(0)
    cellB = Cell.Cell(1)

    print str(cellA)
    print str(cellB)

    cellC = Cell.Cell(2, cellA, cellB)

    print str(cellC)




