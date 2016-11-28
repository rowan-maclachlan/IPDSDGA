import Gene
import ScoreMatrix
import Memory


class Cell:
    """ The Cell is the entity which contains the rule-defining Gene.
    The Cell hosts the Gene, and explicitly defines the viability of the
    rule through realizing associated scores and health metrics. """

    def __init__(self, id, position, parent_a=None, parent_b=None):
        """
        Generate a Cell with a new Gene.  The Gene is formed
        through recombination if parent cells are provided.
        """
        """ int: For uniquely identifying cells """
        self._id = 0
        """ int: Possibly used for data or life-span related functions """
        self._age = 0;
        """ int: To measure the success of a gene """
        self._score = ScoreMatrix.INITIAL_SCORE
        """ Gene: The decision making entity of the cell."""
        self._gene = None
        """ dict(Cell,Memory): To hold the memory of past interactions with other cells"""
        self._memory = {}
        """ Position: The location of the Cell within the toroidal world. """
        self._position = None

        if parent_a is not None and parent_b is not None:
            self._gene = Gene.Gene(parent_a.get_gene(), parent_b.get_gene())
        else:
            self._gene = Gene.Gene()
        self._position = position
        self._id = id

    def reproduce(self, id, position, partner):
        """
        Produce a new Cell by combining this cell and another
        :param id: int The ID for the new Cell
        :param position: Position The new Cell's Position in the world
        :param partner: Cell another Cell to reproduce with
        :return: a new Cell
        """
        return Cell(id, position, self, partner)

    def interact(self, neighbours):
        """
        Process the interaction stages for this cell interacting with all 
        its neighbours. For every neighbour, this Cell and its neighbour
        trade decisions, adjust scores, and adjust memories for a single tick.
        :param neighbours: Set<Cell> The list of neighbouring cells this 
        Cell will interact with.
        :return: None
        """
        for neighbour in neighbours:
            if not self.__eq__(neighbour):
                my_choice = self.get_my_decision(neighbour)
                their_choice = neighbour.get_my_decision(self)

                self.adjust_score(my_choice, their_choice)
                neighbour.adjust_score(their_choice, my_choice)

                self.adjust_memory(neighbour, their_choice)
                neighbour.adjust_memory(self, my_choice)

    def clear_interactions(self):
        """
        Clear the memory of previous tick's
        interactions with other Cells.
        """
        for key in self._memory.keys():
            self._memory[key].clear_interaction()

    def is_dead(self):
        """
        Is this Cell dead?
        :return: True if this Cell's energy is 0
        or lower, and False otherwise.
        """
        return True if 0 >= self._score else False

    def get_my_decision(self, neighbour):
        """
        Retrieve a decision based on the history of this Cell
        with its neighbour.  The decision is retrieved from the gene
        of this cell, using the memory the Cell has of its neighbour
        as input.
        :param neighbour: Cell Another cell to interact with
        :param choice: char A choice 'c' or 'd'
        :return: char The response of this cell to its memory
        of the neighbour cell.
        """
        if neighbour not in self._memory:
            self._memory[neighbour] = Memory.Memory()
        my_choice = self.get_gene().get_decision(self.get_memory_of(neighbour))
        self.get_memory_of(neighbour).record_interaction()
        return my_choice

    def get_position(self):
        return self._position

    def set_position(self, new_pos):
        self._position = new_pos

    def get_score(self):
        return self._score

    def adjust_score(self, my_choice, their_choice):
        """
        Adjust the score of this Cell according to the
        score matrix values and the two input choices.
        Also subtract the energy bleed from this Cell
        :param my_choice: char A choice 'c' or 'd'
        :param their_choice: char A choice 'c' or 'd'
        :return: None
        """
        inc = ScoreMatrix.get_score(my_choice, their_choice)
        self._score += inc
        self._score -= ScoreMatrix.LOSS_PER_TICK

    def reset_score(self):
        """
        Resets the score of this Cell to the
        default score
        :return: None
        """
        self._score = ScoreMatrix.INITIAL_SCORE

    def adjust_memory(self, neighbour, neighbour_choice):
        """
        Adjust the memory of this cell by looking at
        the memory dictionary for a past relationship with the
        neighbour, and adding the new interaction to that memory.
        :param neighbour: Cell the cell involved in the interaction
        :param neighbour_choice: a choice 'c' or 'd' from the other cell
        :return: None
        """
        if neighbour in self._memory:
            self.get_memory_of(neighbour).add_choice_to_memory(
                    neighbour_choice, self.get_gene().get_mem_size())
        else:
            print ("err: getMemory: no memory of subjectID "
                  + str(neighbour.get_id()))

    def get_id(self):
        """
        Get the unique identifier self._id from
        this cell.
        :return: int This Cell's unique ID
        """
        return self._id

    def get_memory_of(self, cell):
        """
        Retrieve the memory associated with the Cell cell
        :param cell: Cell The Cell who is the subject
         of the memory that is wanted.
        :return: Memory A memory of a Cell cell, or
        None if no memory of 'cell' exists
        """
        if cell not in self._memory:
            return None
        else:
            return self._memory[cell]

    def get_gene(self):
        return self._gene

    def is_tft(self):
        g = self.get_gene().get_seq()
        if 'c' != g[1]:
            return False
        for x in range(2, len(g)):
            dec = 'c' if x % 2 == 0 else 'd'
            if dec != g[x]:
                return False
        return True

    def __str__(self):
        return "ID: {}\nPosition: {}{}\nScore: {}\nMemory: {}".format(
                self._id,
                self._position,
                self._gene,
                self._score,
                [ str(mem) for mem in self._memory.values() ]
                )

    def __hash__(self):
        return self._id

    def __cmp__(self, other):
        """
        Return -1 if self._id < other._id,
        return 0 if self._id == other._id,
        and return 1 if self._id > other._id
        :param other: Another Cell
        :return: Return
        -1 if self._id < other._id,
        0 if self._id == other._id,
        1 if self._id > other._id
        """
        if self.get_id() < other.get_id():
            return -1
        elif self.get_id() == self.get_id():
            return 0
        else:
            return 1

    def __eq__(self, other):
        """
        :param other: Cell The Cell being compared to.
        :return: True if the ID of this Cell is
        equal to the ID of the other Cell, False otherwise
        """
        if other == None:
            return False
        return True if self._id == other._id else False

    def has_interacted(self, other):
        """
        Check for interaction between this Cell and the other Cell.
        Test function only.
        :param other: Cell Another cell who may have been interacted with
        :return: True if the other cell has been
        interacted with, False otherwise.
        """
        if other in self._memory:
            if self.get_memory_of(other).has_interacted():
                return True
            else:
                return False
        else:
            return False
