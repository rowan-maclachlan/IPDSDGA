import auxiliaryGenetics as ag
import random
import math

class Gene():

    _DEFAULT_SIZE_MEM = 3

    def __init__(self, gene_a=None, gene_b=None, size_mem=None):
        """
        :type size_mem: int The initial memory size
        :type gene_a: Gene Parent A's Gene
        :type gene_b: Gene Parent B's Gene
        """

        """ list(char): The genetic sequence """
        self._code = list()
        """ int: the depth of the genetic sequence tree, or log2(len(_code)) """
        self._size_mem = None

        # set the memory size of this gene
        if size_mem is not None: self._size_mem = size_mem
        else: self._size_mem = self._DEFAULT_SIZE_MEM
        # produce a new genetic code if this Gene does not have 2 parents
        # If it has parents, produce the code through recombination
        if gene_a is None or gene_b is None:
            self._code = self.ProduceRandomGene()
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
        choice = self._code[1]
        for x in range(0, len(history.getSequence())):
            # If c, get left child
            if 'c' == history.getSequence()[x]:
                if not ag.isValidPosition(self._code, 2*offset):
                    choice = self._code[offset]
                else:
                    offset = 2*offset
            # else its 'd', so get right child
            else:
                if not ag.isValidPosition(self._code, 2*offset+1):
                    choice = self._code[offset]
                else:
                    offset = 2*offset+1
        return choice

    def updateSizeMem(self):
        self._size_mem = int(math.log(len(self._code), 2))

    def ProduceRandomGene(self, size_mem=None):
        """
        Produce a randomly generated _gene of size 2^_size_mem.
        The relevant portions of the gene extend from offset
        0 through 2^_size_mem ( inclusive )
        :return: A _gene sequence
        """
        # If a size is not provided, use this gene's size
        if size_mem is None: size_mem = self._size_mem
        # If the size is provided, make sure
        # to update this gene's memory size
        else: self._size_mem = size_mem
        code = []
        code.append(0)
        for x in xrange(1, 2 ** size_mem):
            code.append(ag.getRandomChoice())
        return code

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
        display += self._code[1]
        display += "\ngene: "
        for x in xrange(1, len(self._code)):
            display += str(self._code[x])
        return display

    def GetFractionDefect(self):
        """
        :return: The percentage of this Gene which is 'd'
        """
        count_defect = 0
        for x in range(1, len(self._code)):
            if 'd' == self._code[x]:
                count_defect += 1
        return float(count_defect) / float(len(self._code)-1)
