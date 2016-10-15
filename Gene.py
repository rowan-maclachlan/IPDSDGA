import auxiliaryGenetics
import random
import math


class Gene():
    _DEFAULT_SIZE_MEM = 2
    P_OF_INSERTION = 0.05
    P_OF_DELETION = 0.05
    P_OF_FLIPPING = 0.05

    _gene = []
    _sizeMem = None

    def __init__(self, gene1=None, gene2=None, sizeMem=_DEFAULT_SIZE_MEM):
        """
        :type sizeMem: int
        :type gene1: Gene
        :type gene2: Gene
        """
        # set the memory size of this gene
        self._sizeMem = sizeMem
        # produce a new genetic code if this Gene does not have 2 parents
        # If it has parents, produce the code through recombination
        if gene1 is None or gene2 is None:
            self._gene = self.ProduceRandomGene()
        else:
            self._gene = self.recombinate(gene1._gene, gene2._gene)

    def recombinate( self, parent2Code, parent1Code ):
        # type: (Gene._gene, Gene._gene) -> Gene._gene
        """
        :param parent1Code:
        :param parent2Code:
        :return:
        """
        newLength = (len(parent1Code) + len(parent2Code)) // 2
        # Find out which is the longer gene
        if len(parent1Code) < len(parent2Code):
            shorterParentCode = parent1Code
            longerParentCode = parent2Code
        else:
            shorterParentCode = parent2Code
            longerParentCode = parent1Code
        newGeneticCode = []
        # Calculate the length of the new gene which can and
        # cannot be generated from both parents
        parentsLength = len(shorterParentCode)
        remainingLength = newLength - parentsLength
        # Produce as much of the new gene from a combination of
        # both parent's _genes as is possible
        for x in xrange( 0, parentsLength ):
            newGeneticCode[x] = parent1Code[x] if ( random.randint(0,1) == 0 ) else parent2Code[x]
        # produce the rest of the gene from the longer parent's _gene
        newGeneticCode[parentsLength:] = longerParentCode[parentsLength:newLength-1]
        # apply mutations to the new gene
        self.mutate()
        return newGeneticCode
        
    def mutate( self ):
        """
        Apply the simulation mutations to this Gene's _gene
        :return: None
        """
        self.applyFlips()
        self.applyDeletions()
        self.applyInsertions()
        return None

    def applyFlips(self):
        """
        :return: None
        """
        for x in xrange( 1, len( self._gene )):
            if self.P_OF_FLIPPING > random.random():
                self._gene[x] = self.getOtherChoice(self._gene[x])
        return None

    def applyDeletions(self):
        """
        Apply deletions over this Gene's _gene according
         to the probability of a deletion per choice in
         the length of the Gene's _gene
        :return: None
        """
        for x in xrange( 1, len( self._gene )):
            if self.P_OF_DELETION > random.random():
                self.removeChoice(x)
        return None

    def applyInsertions(self):
        """
        Apply any mutational insertions to this Gene's _gene
        according to the probability of insertion per choice
        over the length of the Gene's gene.
        :return: None
        """
        for x in xrange(1, len(self._gene)):
            if self.P_OF_INSERTION > random.random():
                self.insertChoice(x, auxiliaryGenetics.GetRandomChoice())
        return None

    def insertChoice(self, choice, pos):
        """
        insert the choice 'c' or 'd' into the position in the gene
        directly after 'pos'.  A choice cannot be
        inserted at position 1
        :param choice: The choice of 'c' or 'd'
        :param pos: The position after which to insert the choice
        :return: None
        """
        if not self.isValidPosition():
            pos = 1
        if not self.isValidChoice(choice):
            choice = auxiliaryGenetics.GetRandomChoice()
        self._gene.insert(pos, choice)
        self.updateSizeMem()

    def appendChoice(self, choice):
        """
        Append the choice to the this gene
        :param choice: the choice to append
        :return: None
        """
        if not self.isValidChoice(choice):
            choice = auxiliaryGenetics.GetRandomChoice()
        self._gene.append(choice)
        self.updateSizeMem()

    def removeChoice(self, pos):
        """
        Remove the choice at position 'pos' in the gene.
        If the position is not valid, the last choice is removed.
        :param pos: the position of the choice to remove
        :return: None
        """
        if not self.isValidChoice(pos):
            pos = len(self._gene)-1
        self._gene.remove(pos)
        self.updateSizeMem()

    def updateSizeMem(self):
        self._sizeMem = math.log(len(self._gene), 2)

    def getOtherChoice(self, choice):
        """
        Return the opposite choice of the argument provided
        :param choice: the choice character for which the opposite is desired
        :return: the character of the opposite choice
        """
        otherChoice = 'd' if choice == 'c' else 'c'
        return otherChoice

    def isValidChoice(self, choice):
        """
        Return true if the 'choice' is a valid choice.
        Return false otherwise.
        :param choice: A choice 'c' or 'd'
        :return: Boolean true or false
        """
        if choice != 'd' or choice != 'c':
            return False
        else:
            return True

    def isValidPosition(self, pos):
        """
        Return true if the 'pos' is a valid position.
        Return false otherwise.
        :param choice: An offset in this Gene's _gene
        :return: Boolean true or false
        """
        if 1 > pos: return False
        if len(self._gene) <= pos: return False
        return True


    def ProduceRandomGene(self, sizeMem=None):
        """
        Produce a randomly generated _gene of size 2^_sizeMem.
        The relevant portions of the gene extend from offset
        0 through 2^_sizeMem ( inclusive )
        :return: A _gene sequence
        """
        # If a size is not provided, use this gene's size
        if sizeMem is None: sizeMem = self._sizeMem
        # If the size is provided, make sure
        # to update this gene's memory size
        else: self._sizeMem = sizeMem
        gene = []

        gene[0] = 0
        for x in xrange(1, 2 ** sizeMem):
            gene[x] = auxiliaryGenetics.GetRandomChoice()
        return gene

    def DisplayGene(self):
        """
        :return: A string of the memory size of the Gene,
         the initial choice, and the gene string.
        """
        display = "\nmemory size: "
        display += str(self._sizeMem)
        display += "\ngene: "
        for x in xrange(1, len(self._gene)):
            display += str(self._gene[x])
        return display

    def GetPercentDefect(self):
        """
        :return: The percentage of this Gene which is 'd'
        """
        countDefect = 0
        for x in range(1, len(self._gene)):
            if 'd' == self._gene[x]:
                countDefect += 1
        return countDefect / len(self._gene)-1
