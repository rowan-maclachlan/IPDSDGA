class Memory():
    """
    This object behaves as a tuple of a Boolean and a List of Choices.
    It is the member which is held in the _memory dictionary of a Cell.
    """

    def __init__(self, sequence=None):
        """

        :param sequence:
        """
        """ Boolean: Defines whether the Cell of this memory has been interacted with. """
        self._has_interacted = False
        """ list(char): The sequence of remembered moves. """
        self._sequence = list()
        if sequence is not None:
            self._sequence = sequence
        self._has_interacted = False

    def addToMemory(self, choice, mem_size):
        """
        Adds the choice to this memory making adjustments for memory size
        :param choice: a choice 'c' or 'd'
        :param mem_size: the length of memory
        :return: None
        """
        if len(self._sequence) >= mem_size:
            self._sequence.pop(0)
        self._sequence.append(choice)
        self.recordInteraction()
        return None

    def getSequence(self):
        """
        :return: list<char> the code sequence of this memory
        """
        return self._sequence

    def getCharacter(self, x):
        """
        Retrieve the character at offset x from this Memory's
        sequence.
        :param x: (int) The offset in the Memory's sequence
        :return: the character at offset x
        """
        return self._sequence[x]

    def hasInteracted(self):
        """
        :return: Boolean Whether or not this cell has interacted.
        """
        return self._has_interacted

    def recordInteraction(self):
        """Record the interaction in memory"""
        self._has_interacted = True

    def clearInteraction(self):
        """Clear the interaction from memory"""
        self._has_interacted = False

    def __str__(self):
        repr = str(self._sequence)
        return repr


