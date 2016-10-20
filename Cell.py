import random
import Gene

class Cell():

    _id = 0;
    _gene = None
    _score = 0
    _memory = None

    def __init__(self, id, parentCell1=None, parentCell2=None):
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

    def interact(self, partner, partnersChoice):
        # If there is a memory of a previous interaction with this partner,
        # retrieve it. Else, create a new memory with the first option.
        if partner.getID() in self._memory:
            memoryOfPartner = self._memory[partner.getID()]
            self._memory[partner.getID()] = self.addToMemory(memoryOfPartner, partnersChoice)
        else:
            if 'd' == partnersChoice:
                self._memory[partner.getID()] = 'd'
            else:
                self._memory[partner.getID()] = 'c'
        response = self.getChoice(self._memory[partner.getID()])
        print response

    def getChoice(self, memory):
        choice = self._gene.getChoice(memory)

    def addToMemory(self, previousMemory, newChoice):
        if len(previousMemory) < self._gene._sizeMem:
            previousMemory.append(newChoice)
        else:
            previousMemory.pop[0]
            previousMemory.append(newChoice)
        return previousMemory


    def getID(self):
        return self._id

    def __str__(self):
        display = str(self._gene)
        display += "\nScore: "
        display += str(self._score)
        return display


