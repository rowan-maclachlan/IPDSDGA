import Cell
import Position as ps

GENERATIONS = 2
SIMULATION_STEPS = 8


def get_largest(cells):
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

    avg_def = 0
    initial_move_percent = 0
    totalScore = 0
    for cell in allCells:
        avg_def += cell.get_gene().get_defect_fraction()
        if 'd' == cell.get_gene().get_choice_at(1):
            initial_move_percent += 1
        totalScore += cell._score
    if not 0 == len(allCells):
        print("\nAverage %defect: " + str(avg_def / len(allCells)))
        print("Initial move %defect: " + str(float(initial_move_percent) / float(len(allCells))))
        print("Average score: " + str(float(totalScore) / float(len(allCells))))

    for i in range(GENERATIONS):
        for cell in allCells:
            cell.clear_score()
        for x in range(SIMULATION_STEPS):
            for cell in allCells:
                cell.clear_interactions()
            for cell in allCells:
                cell.interact(allCells)
            for cell in allCells:
                if cell.is_dead():
                    allCells.remove(cell)
        allCells.sort(key=lambda c: c._score)
        allCells.remove(allCells[0])
        best_cell_a, best_cell_b = get_largest(allCells)
        allCells.append(Cell.Cell(cellID, cellID, best_cell_a, best_cell_b))
        cellID += 1

    avg_def = 0
    initial_move_percent = 0
    totalScore = 0
    for cell in allCells:
        avg_def += cell.get_gene().get_defect_fraction()
        if 'd' == cell.get_gene().get_choice_at(1):
            initial_move_percent += 1
        totalScore += cell._score
    if not 0 == len(allCells):
        print("\nAverage %defect: " + str(avg_def/len(allCells)))
        print("Initial move %defect: " + str(float(initial_move_percent)/float(len(allCells))))
        print("Average score: " + str(float(totalScore)/float(len(allCells))))

    allCells.sort(key=lambda c: c._score)
    cell_1, cell_2 = get_largest(allCells)
    print("\nBest Cells: \n")
    print("a:" + str(cell_1))
    print("b: " + str(cell_2))

    allCells.sort(key=lambda c: c._score)
    for cell in allCells:
        print(str(cell))





