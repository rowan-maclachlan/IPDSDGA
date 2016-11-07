import Gene
import Cell
import numpy as np
import random
import Position as ps

GENERATIONS = 10
SIMULATION_STEPS = 100

if __name__ == "__main__":

    cellA = Cell.Cell(0, ps.Position(1,2))
    cellB = Cell.Cell(1, ps.Position(2,2))

    print str(cellA)
    print str(cellB)

    cellC = Cell.Cell(2, ps.Position(2,3), cellA, cellB)

    print str(cellC)




