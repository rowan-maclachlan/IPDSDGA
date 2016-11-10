import Cell
import Position as ps
import heapq as hq

GENERATIONS = 30
SIMULATION_STEPS = 50


def getLargest(cells):
    return cells[len(cells)-1], cells[len(cells)-2]

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
        for cell in allCells:
            cell.clearScore()
        for x in xrange(SIMULATION_STEPS):
            for cell in allCells:
                cell.clearInteractions()
                if len(cell.getGene()._code) <= 1:
                    print "small Gene: cell: " + str(cell._id)
                    print str(cell)
            for cell in allCells:
                    cell.interact(allCells)
            for cell in allCells:
                if cell.isDead():
                    allCells.remove(cell)
        if 1 == len(allCells):
            print str(allCells[0])
        elif 0 == len(allCells):
            print "\nDead.\n"
        else:
            best_cell_a, best_cell_b = getLargest(allCells)
            allCells.append(Cell.Cell(cellID, cellID, best_cell_a, best_cell_b))
            cellID += 1

    print "\nALL CELLS:\n"
    for cell in allCells:
        print str(cell)

    avg_def = 0
    initial_move_percent = 0
    for cell in allCells:
        avg_def += cell.getGene().GetFractionDefect()
        if 'd' == cell.getGene().getCharacter(1):
            initial_move_percent += 1
    if not 0 == len(allCells):
        print "\nAverage %defect: " + str(avg_def/len(allCells))
        print "Initial move %defect: " + str(initial_move_percent/len(allCells))

    allCells.sort(key=lambda c: c._score)
    if 2 <= len(allCells):
        cell_1, cell_2 = getLargest(allCells)
        print "\nBest Cells: \n"
        print "a:" + str(cell_1)
        print "b: " + str(cell_2)
    else:
        print str(allCells)




