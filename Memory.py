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
        """ list(char): The sequence of all the moves that occurred. """
        self._full_sequence = list()
        if sequence is not None:
            self._sequence = sequence
            self._full_sequence = sequence

    def add_choice_to_memory(self, choice, mem_size):
        """
        Adds the choice to this memory making adjustments for memory size
        If the memory is full, remove the choice from the front of the
        sequence, and add the new choice to the end.
        :param choice: a choice 'c' or 'd'
        :param mem_size: the length of memory
        """
        # Record the interaction in the context
        # of this cell's memory only
        if len(self._sequence) >= mem_size:
            self._sequence.pop(0)
        # Add this to the list of absolute interactions
        self._full_sequence.append(choice)
        self._sequence.append(choice)
        # record the interaction
        self.record_interaction()

    def get_mem_seq(self):
        """
        :return: list<char> the code sequence of this memory
        """
        return self._sequence

    def get_char_from_mem(self, x):
        """
        Retrieve the character at offset x from this Memory's
        sequence.
        :param x: (int) The offset in the Memory's sequence
        :return: the character at offset x
        """
        return self._sequence[x]

    def has_interacted(self):
        """
        :return: Boolean Whether or not this cell has interacted.
        """
        return self._has_interacted

    def record_interaction(self):
        """Record the interaction in memory"""
        self._has_interacted = True

    def clear_interaction(self):
        """Clear the interaction from memory"""
        self._has_interacted = False

    def __str__(self):
        return "".join(self._sequence)


