import random
import Gene
import ScoreMatrix as sm
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
    """ dic(Cell,Memory) To hold the memory of past interactions with other cells"""
    _memory = None
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
        self._id = id

    def reproduce(self, partner):
        """
        Produce a new Cell by combining this cell and another
        :param partner: another Cell
        :return: a new Cell
        """
        return Cell(self, partner)

    def interact(self, neighbours):
        """
        Process the interaction stages for this cell interacting with all its neighbours.
        :param neighbours: Set<Cell> The list of neighbouring cells this Cell will interact with.
        :return: None
        """
        theirChoice = 'd' # <- where does this come from?
        for neighbour in neighbours:
            myChoice = self.decide(neighbour)
            self.adjustScore(myChoice, theirChoice)
            self.adjustMemory(neighbour, theirChoice)

    def decide(self, neighbour):
        return self._gene.getDecision(self._memory[neighbour.getID()])

    def adjustScore(self, myChoice, theirChoice):
        score = sm.getScore(myChoice,theirChoice)
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
        # record the interaction
        self._memory[neighbour.getID()].recordInteraction()

    def getChoice(self, memory):
        """
        Retreive the correct response from the Cell's gene
        :param memory: A list of characters defining a memory sequence
        :return: A character 'c' or 'd'
        """
        choice = self._gene.getChoice(memory)
        return choice

    def getID(self):
        return self._id

    def __str__(self):
        display = str(self._gene)
        display += "\nScore: "
        display += str(self._score)
        return display


