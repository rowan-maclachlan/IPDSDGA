import random
import auxiliaryGenetics
import Gene

class State():

    _gene = None

    def __init__( self, sizeMem=None, firstMove=None, gene=None ):
        # generate a gene to match specifications
        self._gene = Gene.Gene( sizeMem, firstMove )

if( __name__ == "__main__" ):

    INIT_NUM_ORGS = 10;

    orgs = []
    for x in xrange( 0, INIT_NUM_ORGS ):
        orgX = State( random.randint( 1, 3 ))
        orgs.append( orgX )
        print orgX._gene.DisplayGene()

