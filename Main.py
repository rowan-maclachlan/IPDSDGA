import Cell
import Position as ps

GENERATIONS = 10
SIMULATION_STEPS = 10

def getBestCells(cells):
    cell_a = cells[0]
    cell_b = cells[1]
    for x in xrange(len(cells)):
        if cell_a._score < cells[x]._score:
            cell_a = cells[x]
        elif cell_b._score < cells[x]._score:
            cell_b = cells[x]
    return cell_a, cell_b

if __name__ == "__main__":

    # Print and recombinate tests

    cellID = 0

    cell_a = Cell.Cell(cellID, ps.Position(0, cellID))
    cellID += 1
    cell_b = Cell.Cell(cellID, ps.Position(0, cellID))
    cellID += 1
    cell_c = Cell.Cell(cellID, ps.Position(0, cellID))
    cellID += 1
    cell_d = Cell.Cell(cellID, ps.Position(0, cellID))
    cellID += 1

    cell_e = Cell.Cell(cellID, ps.Position(0, cellID), cell_a, cell_b)
    cellID += 1
    cell_f = Cell.Cell(cellID, ps.Position(0, cellID), cell_c, cell_d)
    cellID += 1
    # Interaction Tests

    allCells = [cell_a, cell_b, cell_c, cell_d, cell_e, cell_f]

    print "\n"

    neighbours = [cell_b, cell_c, cell_d]
    cell_a.interact(neighbours)
    if not cell_a.hasInteracted(cell_b): print "err: cell_a, cell_b"
    if not cell_a.hasInteracted(cell_c): print "err: cell_a, cell_c"
    if not cell_a.hasInteracted(cell_d): print "err: cell_a, cell_d"
    if cell_a.hasInteracted(cell_e): print "err: cell_a, cell_e"
    if cell_a.hasInteracted(cell_f): print "err: cell_a, cell_f"

    neighbours = [cell_d, cell_e, cell_f]
    cell_c.interact(neighbours)
    if not cell_c.hasInteracted(cell_a): print "err: cell_c, cell_a"
    if cell_c.hasInteracted(cell_b): print "err: cell_c, cell_b"
    if not cell_c.hasInteracted(cell_d): print "err: cell_c, cell_d"
    if not cell_c.hasInteracted(cell_e): print "err: cell_c, cell_e"
    if not cell_c.hasInteracted(cell_f): print "err: cell_c, cell_f"

    neighbours = [cell_a, cell_b, cell_c]
    cell_d.interact(neighbours)
    if not cell_d.hasInteracted(cell_a): print "err: cell_d, cell_a"
    if not cell_d.hasInteracted(cell_b): print "err: cell_d, cell_b"
    if not cell_d.hasInteracted(cell_c): print "err: cell_d, cell_c"
    if cell_d.hasInteracted(cell_e): print "err: cell_d, cell_e"
    if cell_d.hasInteracted(cell_f): print "err: cell_d, cell_f"

    for cell in allCells:
        cell.clearInteractions()

    if cell_a.hasInteracted(cell_b): print "err: cell_a, cell_b"
    if cell_a.hasInteracted(cell_c): print "err: cell_a, cell_c"
    if cell_a.hasInteracted(cell_d): print "err: cell_a, cell_d"

    if cell_c.hasInteracted(cell_d): print "err: cell_c, cell_d"
    if cell_c.hasInteracted(cell_e): print "err: cell_c, cell_e"
    if cell_c.hasInteracted(cell_f): print "err: cell_c, cell_f"

    if cell_d.hasInteracted(cell_a): print "err: cell_d, cell_a"
    if cell_d.hasInteracted(cell_b): print "err: cell_d, cell_b"
    if cell_d.hasInteracted(cell_c): print "err: cell_d, cell_c"

    for i in xrange(GENERATIONS):
        for x in xrange(SIMULATION_STEPS):
            for cell in allCells:
                cell.clearInteractions()
            for cell in allCells:
                print str(cell._id)
                cell.interact(allCells)
            if cell in allCells:
                if cell.isDead():
                    allCells.remove(cell)
        best_cell_a, best_cell_b = getBestCells(allCells)
        print "b1: " + str(best_cell_a)
        print "b2: " + str(best_cell_b)
        allCells.append(Cell.Cell(cellID, cellID, best_cell_a, best_cell_b))
        cellID += 1

    print "\nALL CELLS:\n"
    for cell in allCells:
        print str(cell)





