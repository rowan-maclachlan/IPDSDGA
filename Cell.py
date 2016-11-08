import random
import Gene
import ScoreMatrix
import Memory

class Cell():
    """ The Cell is the entity which contains the rule-defining Gene.
    The Cell hosts the Gene, and explicitly defines the vialibity of the
    rule through realizing associated scores and health metrics. """

    """ (int) For uniquely identifying cells """
    _id = 0;
    """ (int) Possibly used for data or life-span related functions """
    _age = 0;
    """ (int) To measure the success of a gene """
    _score = 0
    """ (Gene) The decision making entity of the cell."""
    _gene = None
    """ dict(Cell,Memory) To hold the memory of past interactions with other cells"""
    _memory = {}
    """ (Position) The location of the Cell within the toroidal world. """
    currentPosition = None
    """ (Position) The next location the Cell aspires to. """
    nextPosition = None

    def __init__(self, id, position, parentCell1=None, parentCell2=None):
        # generate a gene to match specifications
        if parentCell1 is not None and parentCell2 is not None:
            self._gene = Gene.Gene(parentCell1._gene, parentCell2._gene)
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
        Process the interaction stages for this cell interacting with all its neighbours.
        :param neighbours: Set<Cell> The list of neighbouring cells this Cell will interact with.
        :return: None
        """
        for neighbour in neighbours:
            myChoice = self.getMyDecision(neighbour)
            theirChoice = neighbour.getMyDecision(self)

            self.adjustScore(myChoice, theirChoice)
            neighbour.adjustScore(theirChoice, myChoice)

            self.adjustMemory(neighbour, theirChoice)
            neighbour.adjustMemory(self, myChoice)

    def getMyDecision(self, neighbour):
        """
        :param neighbour: Cell Another cell to interact with
        :param choice: char A choice 'c' or 'd'
        :return: char The response of this cell to its memory
        of the neighbour cell.
        """
        if not neighbour.getID() in self._memory:
            self._memory[neighbour.getID()] = Memory.Memory()
        myChoice = self._gene.getDecision(self._memory[neighbour.getID()])
        self._memory[neighbour.getID()].recordInteraction()
        return myChoice

    def adjustScore(self, myChoice, theirChoice):
        """
        Adjust the score of this Cell according to the
        score matrix values and the two input choices.
        :param myChoice: char A choice 'c' or 'd'
        :param theirChoice: char A choice 'c' or 'd'
        :return: None
        """
        score = ScoreMatrix.getScore(myChoice,theirChoice)
        self._score += score

    def adjustMemory(self, neighbour, neighbourChoice):
        """
        Adjust the memory of this cell by looking at
        the memory dictionary for a past relationship with the
        neighbour, and adding the new interaction to that memory.
        :param neighbour: Cell the cell involved in the interaction
        :param neighbourChoice: a choice 'c' or 'd' from the other cell
        :return: None
        """
        if neighbour.getID() in self._memory:
            self._memory[neighbour.getID()].addToMemory(neighbourChoice, self._gene._sizeMem)
        else:
            if 'd' == neighbourChoice:
                self._memory[neighbour.getID()] = Memory.Memory('d')
            else:
                self._memory[neighbour.getID()] = Memory.Memory('c')

    def getID(self):
        return self._id

    def __str__(self):
        display = "\nID: "
        display += str(self._id)
        display += str(self._gene)
        display += "\nScore: "
        display += str(self._score)
        display += "\nMemory: "
        for mem in self._memory:
            display += str(self._memory[mem])
        return display

    def hasInteracted(self, other):
        """
        Check for interaction between this cell and the other cell.
        :param other: Cell Another cell who may have been interacted with
        :return: Boolean True if the other cell has been interacted with, false otherwise.
        """
        if other.getID() in self._memory:
            if self._memory[other.getID()]._hasInteracted:
                return True;
            else:
                return False
        else: return False

