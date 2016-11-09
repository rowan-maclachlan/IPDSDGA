import Cell
import Position as ps

GENERATIONS = 10
SIMULATION_STEPS = 100

if __name__ == "__main__":

    # Print and recombinate tests

    cell_a = Cell.Cell(1, ps.Position(1, 1))
    cell_b = Cell.Cell(2, ps.Position(1, 2))
    cell_c = Cell.Cell(3, ps.Position(2, 1))
    cell_d = Cell.Cell(4, ps.Position(2, 2))

    cell_e = Cell.Cell(5, ps.Position(0, 0), cell_a, cell_b)
    cell_f = Cell.Cell(6, ps.Position(0, 1), cell_c, cell_d)

    # Interaction Tests

    all = [cell_a, cell_b, cell_c, cell_d, cell_d, cell_f]
    for cell in all:
        print "\nid: " + str(cell.getID())

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

    print str(cell_a)
    print str(cell_b)
    print str(cell_c)
    print str(cell_d)
    print str(cell_e)
    print str(cell_f)





