import random
import auxiliaryGenetics
import Gene
import numpy as np

class State():

    _gene = None

    def __init__( self, sizeMem=None, firstMove=None, gene=None ):
        # generate a gene to match specifications
        self._gene = Gene.Gene( sizeMem, firstMove )

if( __name__ == "__main__" ):

    SPREAD_OF_MEMORY = 5    # The initial variation in State organism memory
    INIT_ARR_NUM_X = 10     # The size of the array
    INIT_ARR_NUM_Y = 10     # The size of the array
    INIT_NUM_ORGS = INIT_ARR_NUM_X * INIT_ARR_NUM_Y; # The initial number of State organisms in the simulation

    # create a placeholder 2-d array
    orgs = np.empty(shape=[INIT_ARR_NUM_X, INIT_ARR_NUM_Y], dtype=object)
    # populate the array with State organisms
    for i in xrange( 0, INIT_ARR_NUM_X ):
        for j in xrange( 0, INIT_ARR_NUM_Y ):
            orgX = State( random.randint( 1, SPREAD_OF_MEMORY ))
            orgs[ (i, j) ] = orgX
            print orgX._gene.DisplayGene()

    print orgs

