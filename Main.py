import Gene
import Cell
import numpy as np
import random
import Position as ps

GENERATIONS = 10
SIMULATION_STEPS = 100

if __name__ == "__main__":

    # Print and recombinate tests

    cellA = Cell.Cell(0, ps.Position(1, 1))
    cellB = Cell.Cell(1, ps.Position(1, 2))
    cellC = Cell.Cell(2, ps.Position(2, 1))
    cellD = Cell.Cell(3, ps.Position(2, 2))

    print str(cellA)
    print str(cellB)
    print str(cellC)
    print str(cellD)

    cellE = Cell.Cell(2, ps.Position(0, 0), cellA, cellB)
    cellF = Cell.Cell(2, ps.Position(0, 1), cellC, cellD)

    print str(cellE)
    print str(cellF)

    # Interaction Tests

    print "\n"

    neighbours = [cellB, cellC, cellD]
    cellA.interact(neighbours)
    if not cellA.hasInteracted(cellB): print "err: cellA, cellB"
    if not cellA.hasInteracted(cellC): print "err: cellA, cellC"
    if not cellA.hasInteracted(cellD): print "err: cellA, cellD"
    if cellA.hasInteracted(cellE): print "err: cellA, cellE"
    if cellA.hasInteracted(cellF): print "err: cellA, cellF"

    neighbours = [cellD, cellE, cellF]
    cellC.interact(neighbours)
    if not cellC.hasInteracted(cellD): print "err: cellC, cellD"
    if not cellC.hasInteracted(cellE): print "err: cellC, cellE"
    if not cellC.hasInteracted(cellF): print "err: cellC, cellF"
    if not cellC.hasInteracted(cellA): print "err: cellC, cellA"
    if cellC.hasInteracted(cellB): print "err: cellC, cellB"







