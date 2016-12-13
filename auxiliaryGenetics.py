import random
from params import params


def recombine(parent_a, parent_b):
    """
    Recombine the code sequences of parent_a and parent_b
    into a new code sequence.
    :param parent_a: Parent A's Gene
    :type parent_a: Gene
    :param parent_b: Parent B's Gene
    :type parent_b: Gene:
    :return: A new code formed from parent A' gene's
    code and parent B's gene's code.
    :rtype: A list of characters
    """
    code_a = parent_a.get_seq()
    code_b = parent_b.get_seq()
    # Do not let the length of a gene fall less that 2
    new_code_length = max(((len(code_a) + len(code_b)) // 2), 2)
    # Find out which is the longer gene
    if len(code_a) < len(code_b):
        shorter_parent_code = code_a
        longer_parent_code = code_b
    else:
        shorter_parent_code = code_b
        longer_parent_code = code_a
    new_gen_code = list()
    # Calculate the length of the new gene which can and
    # cannot be generated from both parents
    shared_parent_length = len(shorter_parent_code)
    # Produce as much of the new gene from a combination of
    # both parent's _genes as is possible
    for x in range(0, shared_parent_length):
        new_gen_code.append(code_a[x] if random.choice([True,False]) else code_b[x])
    # produce the rest of the gene from the longer parent's _gene
    new_gen_code[shared_parent_length:] = longer_parent_code[shared_parent_length:new_code_length - 1]
    return new_gen_code


def produce_random_gene(size_mem):
    """
    Produce a randomly generated _gene of size 2^_size_mem.
    The relevant portions of the gene extend from offset
    0 through 2^_size_mem ( inclusive )
    :param size_mem: the size of a Cell's memory
    :type size_mem: int
    :return: A _gene sequence
    :rtype: a list of characters
    """
    # If the size is provided, make sure
    # to update this gene's memory size
    code = []
    code.append(0)
    for x in range(1, 2 ** size_mem):
        code.append(get_random_choice())
    return code


def get_random_choice(chance=0.5):
    """
    Produce a choice, 'c' or 'd',
    depending on the random value chance
    :param chance: The chance that a random choice
        will be a 'd' instead of a 'c'
    :type chance: float Representing a probability
    :return: a 'd' or a 'c'
    :rtype: char
    """
    return 'd' if chance > random.random() else 'c'


def get_other_choice(choice):
    """
    Return the opposite choice of the argument provided
    :param choice: the choice character for which the opposite is desired
    :type choice: char
    :return: the character of the opposite choice
    :rtype: char
    """
    return 'd' if choice == 'c' else 'c'


def is_valid_choice(choice):
    """
    Return true if the 'choice' is a valid choice.
    Return false otherwise.
    :param choice: A choice 'c' or 'd'
    :type choice: char
    :return: true if the choice is valid,
        or false otherwise.
    :rtype: boolean
    """
    if choice != 'd' or choice != 'c':
        return False
    else:
        return True


def is_valid_position(code, pos):
    """
    Return true if the 'pos' is a valid _position.
    Return false otherwise.
    :param pos: An offset in this code
    :type pos: int
    :param code: A list of choices
    :type code: list(char)
    :return: true if the position in the code
        is valid, and false otherwise.
    :rtype: boolean
    """
    if 1 > pos: return False
    if len(code) <= pos: return False
    return True


def mutate(code):
    """
    Apply the simulation mutations to a Gene's _gene
    :param code: A list of choices, a Gene's sequence.
    :type code: list(char)
    """
    apply_flips(code)
    applyDeletions(code)
    apply_insertions(code)


def apply_flips(code):
    """
    Proceed over the code and apply flip mutations
    according to the probabilty of a flip.
    :param code: a list of character as code
    :type code: list(char)
    """
    for x in range(1, len(code)):
        if params['mutation_chance_flip'] > random.random():
            code[x] = get_other_choice(code[x])

def applyDeletions(code):
    """
    Apply deletions over this Gene's _gene according
     to the probability of a deletion per choice in
     the length of the Gene's _gene
    :param code: a Gene's code sequence
    :type code: list(char)
    """
    # We cannot delete a choice if the length of the
    # code is already only 2 long. 2 long is just
    # 1 choice.
    for x in range(1, len(code)):
        if len(code) <= 2:
            break;
        if params['mutation_chance_delete'] > random.random():
            remove_choice(code, x)


def apply_insertions(code):
    """
    Apply any mutational insertions to this Gene's _gene
    according to the probability of insertion per choice
    over the length of the Gene's gene.
    :param code: a list of character as code
    :type code: list(char)
    """
    for x in range(1, len(code)):
        if params['mutation_chance_insert'] > random.random():
            insert_choice(code, get_random_choice(), x)


def insert_choice(code, choice, pos):
    """
    insert the choice 'c' or 'd' into the _position in the gene
    directly after 'pos'.
    :param code: A list of character as code
    :type code: list(char)
    :param choice: The choice of 'c' or 'd'
    :type choice: char
    :param pos: The position in the code after which to insert the choice
    :type pos: int
    """
    if not is_valid_choice(choice):
        choice = get_random_choice()
    if not is_valid_position(code, pos):
        code.append(choice)
    else:
        code.insert(pos, choice)


def append_choice(code, choice):
    """
    Append the choice to the this gene
    :param code: A list of character as code
    :type code: list(char)
    :param choice: the choice to append
    :type choice: char
    """
    if not is_valid_choice(choice):
        choice = get_random_choice()
    code.append(choice)


def remove_choice(code, pos):
    """
    Remove the choice at _position 'pos' in the code.
    If the _position is not valid, the last choice is removed.
    :param code: A Gene sequence
    :type code: list(char)
    :param pos: the position of the choice to remove
    :type pos: int
    """
    if not is_valid_position(code, pos):
        pos = len(code) - 1
    del code[pos]
