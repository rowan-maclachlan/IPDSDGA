import Gene
import Memory
import params as p

class Cell:
    """ 
    The Cell is the entity which contains the rule-defining Gene.
    The Cell hosts the Gene, and explicitly defines the viability of the
    rule through realizing associated scores and health metrics. 
    """

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
        self._score =  p.params['initial_score']
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
        :param id: The ID for the new Cell
        :type id: int
        :param position: The new Cell's Position in the world
        :type position: Position
        :param partner: another Cell to reproduce with
        :type partner: Cell
        :return: a new Cell
        :rtype: Cell
        """
        return Cell(id, position, self, partner)

    def interact(self, neighbours):
        """
        Process the interaction stages for this cell interacting with all 
        its neighbours. For every neighbour, this Cell and its neighbour
        trade decisions, adjust scores, and adjust memories for a single tick.
        :param neighbours: The list of neighbouring cells this 
                           Cell will interact with.
        :type neighbours: list(Cell)
        """
        for neighbour in neighbours:
            if not self.__eq__(neighbour):
                my_choice = self._get_my_decision(neighbour)
                their_choice = neighbour._get_my_decision(self)

                self._adjust_score(my_choice, their_choice)
                neighbour._adjust_score(their_choice, my_choice)

                self._adjust_memory(neighbour, their_choice)
                neighbour._adjust_memory(self, my_choice)

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
        or lower or it is too old, and False otherwise.
        :rtype: boolean
        """
        dead = True if 0 >= self._score else False
        if p.params['ageing'] and self._age > p.params['age_of_death']:
            dead = True
        return dead

    def _get_my_decision(self, neighbour):
        """
        Retrieve a decision based on the history of this Cell
        with its neighbour.  The decision is retrieved from the gene
        of this cell, using the memory the Cell has of its neighbour
        as input.
        :param neighbour: Another cell to interact with
        :type neighbour: Cell
        :return: The response of this cell to its memory
        of the neighbour cell.
        :rtype: char
        """
        if neighbour not in self._memory:
            self._memory[neighbour] = Memory.Memory()
        my_choice = self.get_gene().get_decision(self.get_memory_of(neighbour))
        self.get_memory_of(neighbour).record_interaction()
        return my_choice

    def get_position(self):
        """
        Get this Cell's position.
        :return: This Cell's position on the toroidal world.
        :rtype: Position
        """
        return self._position

    def set_position(self, new_pos):
        """
        Set this Cell's position.
        :param new_pos: The new position for this Cell.
        :type new_pos: Position
        """
        self._position = new_pos

    def get_score(self):
        """
        Get this Cell's score.
        :return: This Cell's score.
        :rtype: float
        """
        return self._score

    def _adjust_score(self, my_choice, their_choice):
        """
        Adjust the score of this Cell according to the
        score matrix values and the two input choices.
        Also subtract the score bleed from this Cell
        :param my_choice: A choice 'c' or 'd'
        :type my_choice: char
        :param their_choice: A choice 'c' or 'd'
        :type their_choice: char
        """
        self._score += p.params['score_matrix'][my_choice][their_choice]
        self._score -= p.params['loss_per_tick']

    def reset_score(self):
        """
        Resets the score of this Cell to the default score.
        """
        self._score = p.params['initial_score']

    def _adjust_memory(self, neighbour, neighbour_choice):
        """
        Adjust the memory of this cell by looking at
        the memory dictionary for a past relationship with the
        neighbour, and adding the new interaction to that memory.
        :param neighbour: the cell involved in the interaction
        :type neighbour: Cell
        :param neighbour_choice: a choice 'c' or 'd' from the other cell
        :type neighbour_choice: char
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
        :return: This Cell's unique ID
        :rtype: int
        """
        return self._id

    def get_memory_of(self, cell):
        """
        Retrieve the memory associated with the Cell cell
        :param cell: The Cell who is the subject
                     of the memory that is wanted.
        :type cell: Cell
        :return: A memory of a Cell cell, 
                 or None if no memory of 'cell' exists
        :rtype: Memory || None
        """
        if cell not in self._memory:
            return None
        else:
            return self._memory[cell]

    def age(self):
        """
        Increment the age of this Cell by 1.
        """
        self._age += 1

    def get_age(self):
        """
        Get the age of this Cell.
        :return: The age of this Cell.
        :rtype: int
        """
        return self._age

    def get_gene(self):
        """
        Get this Cell's Gene.
        :return: This Cell's Gene.
        :rtype: Gene
        """
        return self._gene

    def is_tft(self):
        """
        Is this Cell's rule a perfect Tit-For-Tat?
        :return: True if this Cell's rule is a perfect TFT,
                 False if it is not.
        :rtype: boolean
        """
        g = self.get_gene().get_seq()
        if 'c' != g[1]:
            return False
        if not len(g) >= 4:
            return False
        for x in range(2, len(g)):
            dec = 'c' if x % 2 == 0 else 'd'
            if dec != g[x]:
                return False
        return True

    def is_ftf(self):
        """
        Is this Cell's rule a mean tit for tat
        :return: True if this Cell is a mean TFT, false otherwise.
        :rtype: boolean
        """
        g = self.get_gene().get_seq()
        if 'd' != g[1]:
            return False
        if not len(g) >= 4:
            return False
        for x in range(2, len(g)):
            dec = 'c' if x % 2 == 0 else 'd'
            if dec != g[x]:
                return False
        return True

    def is_t2t(self):
        """
        Is this Cell's rule a perfect Tit-For-Two-Tats?
        :return: True if this Cell's rule is a perfect T2T,
                 False if it is not.
        :rtype: boolean
        """
        g = self.get_gene().get_seq()
        if 'c' != g[1]:
            return False
        if not len(g) >= 8:
            return False
        for x in range(2, 4):
            if g[x] is not 'c':
                return False
        for x in range(1, len(g)-3):
            dec = 'd' if x % 4 == 0 else 'c'
            if g[x+3] is not dec:
                return False
        return True

    def is_alld(self):
        """
        Is this Cell's rule strictly defect?
        :return: True if this Cell's rule always defects,
                 False if it does not.
        :rtype: boolean
        """
        g = self.get_gene().get_seq()
        for i in range(1, len(g)):
            if g[i] is 'c':
                return False
        return True
    
    def is_allc(self):
        """
        Is this Cell's rule strictly cooperate?
        :return: True if this Cell's rule always cooperates,
                 False if it does not.
        :rtype: boolean
        """
        g = self.get_gene().get_seq()
        for i in range(1, len(g)):
            if g[i] is 'd':
                return False
        return True

    def draw(self):
        """
        Return a string that represents the Cell and its rule
        :return: A string that represent's this Cell's rule
        :rtype: str
        """
        drawing = ""
        
        if self.get_gene().get_choice_at(1) is 'c':
            drawing += 'o'
        else:
            drawing += 'x'
        
        if self.is_tft():
            drawing += "tft"
            return drawing
        elif self.is_t2t():
            drawing += "t2t"
            return drawing
        elif self.is_ftf():
            drawing += "ftf"
            return drawing

        rule = self.get_gene().get_defect_fraction()
        fraction_display = 0.166

        if rule >= 1.0:
            drawing += "ddd"
        elif rule > (5*fraction_display):
            drawing += "ddc"
        elif rule > (4*fraction_display):
            drawing += "dcd"
        elif rule > (3*fraction_display):
            drawing += "dcc"
        elif rule > (2*fraction_display):
            drawing += "cdd"
        elif rule > (1*fraction_display):
            drawing += "cdc"
        elif rule > (0*fraction_display):
            drawing += "ccd"
        else:
            drawing += "ccc"

        return drawing

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
        :param other: The Cell being compared to.
        :type other: Cell
        :return: True if the ID of this Cell is equal 
                 to the ID of the other Cell, False otherwise
        :rtype: boolean
        """
        if other == None:
            return False
        return True if self._id == other._id else False

    def has_interacted(self, other):
        """
        Check for interaction between this Cell and the other Cell.
        Test function only.
        :param other: Another Cell who may have been interacted with
        :type other: Cell
        :return: True if the other cell has been
                 interacted with, False otherwise.
        :rtype: boolean
        """
        if other in self._memory:
            if self.get_memory_of(other).has_interacted():
                return True
            else:
                return False
        else:
            return False
