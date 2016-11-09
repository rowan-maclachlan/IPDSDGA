import random
import Gene
import ScoreMatrix
import Memory
import itertools as iter

class Cell():
    """ The Cell is the entity which contains the rule-defining Gene.
    The Cell hosts the Gene, and explicitly defines the vialibity of the
    rule through realizing associated scores and health metrics. """

    def __init__(self, id, position, parent_a=None, parent_b=None):
        """
        Generate a Cell with a new Gene.  The Gene is formed
        through recombination if parent cells are provided.
        """

        """ int: For uniquely identifying cells """
        self._id = 0
        """ int: Possibly used for data or life-span related functions """
        self._age = 0;
        """ int: To measure the success of a gene """
        self._score = 0
        """ Gene: The decision making entity of the cell."""
        self._gene = None
        """ dict(Cell,Memory): To hold the memory of past interactions with other cells"""
        self._memory = {}
        """ Position: The location of the Cell within the toroidal world. """
        self.current_position = None
        """ Position: The next location the Cell aspires to. """
        self.next_position = None

        if parent_a is not None and parent_b is not None:
            self._gene = Gene.Gene(parent_a._gene, parent_b._gene)
        else:
            self._gene = Gene.Gene()
        self.currentPosition = position
        self._id = id

    def reproduce(self, id, position, partner):
        """
        Produce a new Cell by combining this cell and another
        :param id: int The ID for the new Cell
        :param position: Position The new Cell's Position in the world
        :param partner: Cell another Cell to reproduce with
        :return: a new Cell
        """
        return Cell(id, position, self, partner)

    def interact(self, neighbours):
        """
        Process the interaction stages for this cell interacting with all 
        its neighbours. For every neighbour, this Cell and its neighbour
        trade decisions, adjust scores, and adjust memories for a single tick.
        :param neighbours: Set<Cell> The list of neighbouring cells this 
        Cell will interact with.
        :return: None
        """
        for neighbour in neighbours:
            my_choice = self.getMyDecision(neighbour)
            their_choice = neighbour.getMyDecision(self)

            self.adjustScore(my_choice, their_choice)
            neighbour.adjustScore(their_choice, my_choice)

            self.adjustMemory(neighbour, their_choice)
            neighbour.adjustMemory(self, my_choice)

    def getMyDecision(self, neighbour):
        """
        Retrieve a decision based on the history of this Cell
        with its neighbour.  The decision is retrieved from the gene
        of this cell, using the memory the Cell has of its neighbour
        as input.
        :param neighbour: Cell Another cell to interact with
        :param choice: char A choice 'c' or 'd'
        :return: char The response of this cell to its memory
        of the neighbour cell.
        """
        if not neighbour in self._memory:
            self._memory[neighbour] = Memory.Memory()
        myChoice = self._gene.getDecision(self.getMemory(neighbour))
        self.getMemory(neighbour).recordInteraction()
        return myChoice

    def adjustScore(self, my_choice, their_choice):
        """
        Adjust the score of this Cell according to the
        score matrix values and the two input choices.
        :param my_choice: char A choice 'c' or 'd'
        :param their_choice: char A choice 'c' or 'd'
        :return: None
        """
        score = ScoreMatrix.getScore(my_choice, their_choice)
        self._score += score

    def adjustMemory(self, neighbour, neighbour_choice):
        """
        Adjust the memory of this cell by looking at
        the memory dictionary for a past relationship with the
        neighbour, and adding the new interaction to that memory.
        :param neighbour: Cell the cell involved in the interaction
        :param neighbour_choice: a choice 'c' or 'd' from the other cell
        :return: None
        """
        if neighbour in self._memory:
            self.getMemory(neighbour).addToMemory( \
                    neighbour_choice, self._gene._size_mem)
        else:
            print "err: getMemory: no memory of subjectID " \
                  + str(neighbour.getID())

    def getID(self):
        return self._id

    def getMemory(self, cell):
        """
        Retrieve the memory associated with the Cell cell
        :param cell: Cell The Cell who is the subject
         of the memory that is wanted.
        :return: Memory A memory of a Cell cell
        """
        return self._memory[cell]

    def __str__(self):
        display = "\nID: "
        display += str(self._id)
        display += str(self._gene)
        display += "\nScore: "
        display += str(self._score)
        display += "\nMemory: "
        for key in self._memory.keys():
            display += str(self._memory[key])
        return display

    def __hash__(self):
        return self._id

    def __cmp__(self, other):
        if self.getID() < other.getID():
            return -1
        elif self.getID() == self.getID():
            return 0
        else: return 1


    def hasInteracted(self, other):
        """
        Check for interaction between this cell and the other cell.
        :param other: Cell Another cell who may have been interacted with
        :return: Boolean True if the other cell has been 
        interacted with, false otherwise.
        """
        if other in self._memory:
            if self.getMemory(other).hasInteracted():
                return True;
            else:
                return False
        else:
            return False