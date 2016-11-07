import auxiliaryGenetics as ag
import random
import math

class Gene():

    _DEFAULT_SIZE_MEM = 3
    P_OF_INSERTION = 0.05
    P_OF_DELETION = 0.05
    P_OF_FLIPPING = 0.05

    _code = None
    _sizeMem = None

    def __init__(self, gene1=None, gene2=None, sizeMem=_DEFAULT_SIZE_MEM):
        """
        :type sizeMem: int The initial memory size
        :type gene1: Gene Parent A's Gene
        :type gene2: Gene Parent B's Gene
        """
        # set the memory size of this gene
        self._sizeMem = sizeMem
        # produce a new genetic code if this Gene does not have 2 parents
        # If it has parents, produce the code through recombination
        if gene1 is None or gene2 is None:
            self._code = self.ProduceRandomGene()
        else:
            self._code = ag.recombinate(gene1, gene2)
            self.mutate(self._code)

    def getDecision(self, history):
        """
        Find the choice of this Gene's Cell depending on the
        history provided.  If the move is a 'c', get the left
        child.  If it a 'd', get the right child.  If we reach
        a leaf node, return that value
        :param history: List<Choice> The history or moves provided
        :return: the choice dictated by the gene and history provided
        """
        offset = 1
        choice = self._code[1]
        for x in range(0, len(history)):
            # If c, get left child
            if 'c' == history[x]:
                if not self.isValidPosition(2*offset):
                    choice = self._code[offset]
                else:
                    offset = 2*offset
            # else its 'd', so get right child
            else:
                if not self.isValidPosition(2*offset+1):
                    choice = self._gene[offset]
                else:
                    offset = 2*offset+1
        return choice

    def updateSizeMem(self):
        self._sizeMem = int(math.log(len(self._gene), 2))

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
        code = list(0)

        for x in xrange(1, 2 ** sizeMem):
            code.append(ag.GetRandomChoice())
        return code

    def __str__(self):
        """
        Prints a string representation of all
        important information of the Gene
        :return:
        """
        display = "\nmemory size: "
        display += str(self._sizeMem)
        display += "\npercent defect: "
        display += str(self.GetFractionDefect())
        display += "\ninitial move: "
        display += self._code[1]
        display += "\ngene: "
        for x in xrange(1, len(self._gene)):
            display += str(self._gene[x])
        return display

    def GetFractionDefect(self):
        """
        :return: The percentage of this Gene which is 'd'
        """
        countDefect = 0
        for x in range(1, len(self._gene)):
            if 'd' == self._gene[x]:
                countDefect += 1
        return float(countDefect) / float(len(self._gene)-1)
