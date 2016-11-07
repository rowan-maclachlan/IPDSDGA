class Memory():
    """
    This object behaves as a tuple of a Boolean and a List of Choices.
    It is the member which is held in the _memory dictionary of a Cell.
    """

    """ A boolean to define whether the Cell of this memory has been interacted with. """
    _hasInteracted = None
    """ The sequence of remembered moves. """
    _sequence = None

    def __init__(self, sequence=None):
        self._hasInteracted = True
        if sequence is not None:
            self._sequence = sequence


    def addToMemory(self, choice, memSize):
        """
        Adds the choice to this memory making adjustments for memory size
        :param choice: a choice 'c' or 'd'
        :param memSize: the length of memory
        :return: None
        """
        if len(self._sequence) >= memSize:
            self._sequence.pop[0]
        self._sequence.append(choice)
        self.recordInteraction()
        return None

    def recordInteraction(self):
        """Record the interaction in memory"""
        self._hasInteracted = True

    def clearInteraction(self):
        """Clear the interaction from memory"""
        self._hasInteracted = False



