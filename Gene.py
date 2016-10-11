import auxiliaryGenetics

class Gene():

    _DEFAULT_SIZE_MEM = 1

    _gene = None
    _sizeMem = None
    _initChoice = None

    def __init__( self, sizeMem=None, initChoice=None ):
        # set the memory size of this gene
        if( None == sizeMem ): self._sizeMem = self._DEFAULT_SIZE_MEM
        else: self._sizeMem = sizeMem
        # set the initial choice of this gene
        if( None == initChoice ): self._initChoice = auxiliaryGenetics.GetRandomChoice()
        else: self._initChoice = initChoice
        # produce the gene
        self._gene = self.ProduceRandomGene()

    def ProduceRandomGene( self ):
        gene = ""
        gene = self._initChoice
        for x in xrange( 0, 2**self._sizeMem ):
            gene += auxiliaryGenetics.GetRandomChoice()
        return gene

    def DisplayGene( self ):
        display = "\nmemory size: "
        display += str( self._sizeMem )
        display += "\ninitial choice: "
        display += str( self._initChoice )
        display += "\ngene: "
        display += str( self._gene )
        return display

