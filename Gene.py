import auxiliaryGenetics as ag
import random
import math

class Gene():

    _DEFAULT_SIZE_MEM = 3

    def __init__(self, gene_a=None, gene_b=None):
        """
        :type gene_a: Gene Parent A's Gene
        :type gene_b: Gene Parent B's Gene
        """

        """ list(char): The genetic sequence """
        self._code = list()
        """ int: the depth of the genetic sequence tree, or log2(len(_code)) """
        self._size_mem = self._DEFAULT_SIZE_MEM

        # produce a new genetic code if this Gene does not have 2 parents
        # If it has parents, produce the code through recombination
        if gene_a is None or gene_b is None:
            self._code = ag.ProduceRandomGene(self._size_mem)
            ag.mutate(self._code)
            self.updateSizeMem()
        else:
            self._code = ag.recombinate(gene_a, gene_b)
            ag.mutate(self._code)
            self.updateSizeMem()

    def getDecision(self, history):
        """
        Find the choice of this Gene's Cell depending on the
        history provided.  If the move is a 'c', get the left
        child.  If it a 'd', get the right child.  If we reach
        a leaf node, return that value
        :param history: Memory The history or moves provided
        :return: the choice dictated by the gene and history provided
        """
        offset = 1
        for x in history.getSequence():
            # If c, get left child
            if 'c' == x:
                if not ag.isValidPosition(self._code, 2*offset):
                    return self.getCharacter(offset)
                else:
                    offset = 2*offset
            # else its 'd', so get right child
            else:
                if not ag.isValidPosition(self._code, 2*offset+1):
                    return self.getCharacter(offset)
                else:
                    offset = (2*offset)+1
        return self.getCharacter(offset)

    def getCharacter(self, x):
        """
        Retrieve the character at offset 'x' from this Gene's code
        :param x: (int) the offset
        :return: the character at offset 'x' in the gene
        """
        return self._code[x]

    def updateSizeMem(self):
        """
        Update the size of the Gene's memory to the
        the floor of base 2 log of the length of this
        Gene's code
        """
        self._size_mem = int(math.log(len(self._code), 2))

    def __str__(self):
        """
        Prints a string representation of all
        important information of the Gene
        :return:
        """
        display = "\nmemory size: "
        display += str(self._size_mem)
        display += "\npercent defect: "
        display += str(self.GetFractionDefect())
        display += "\ninitial move: "
        display += self.getCharacter(1)
        display += "\ngene: "
        for x in xrange(1, len(self._code)):
            display += str(self._code[x])
        #display += "\n"

        return display

    def GetFractionDefect(self):
        """
        :return: The percentage of this Gene which is 'd'
        """
        count_defect = 0
        for x in range(1, len(self._code)):
            if 'd' == self.getCharacter(x):
                count_defect += 1
        return float(count_defect) / float(len(self._code)-1)
