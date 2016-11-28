import random
from params import params


def recombinate(parent_a, parent_b):
    """
    :param parent_a: Gene Parent A's Gene
    :param parent_b: Gene Parent B's Gene
    :return: A new code formed from parent A' gene's
    code and parent B's gene's code.
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

def ProduceRandomGene(size_mem):
    """
    Produce a randomly generated _gene of size 2^_size_mem.
    The relevant portions of the gene extend from offset
    0 through 2^_size_mem ( inclusive )
    :return: A _gene sequence
    """
    # If the size is provided, make sure
    # to update this gene's memory size
    code = []
    code.append(0)
    for x in range(1, 2 ** size_mem):
        code.append(getRandomChoice())
    return code

def getRandomChoice(chance=0.5):
    """
    Produce a choice, 'c' or 'd',
    depending on the random value chance
    :return:
    """
    return 'd' if chance > random.random() else 'c'

def getOtherChoice(choice):
    """
    Return the opposite choice of the argument provided
    :param choice: the choice character for which the opposite is desired
    :return: the character of the opposite choice
    """
    return 'd' if choice == 'c' else 'c'

def isValidChoice(choice):
    """
    Return true if the 'choice' is a valid choice.
    Return false otherwise.
    :param choice: A choice 'c' or 'd'
    :return: Boolean true or false
    """
    if choice != 'd' or choice != 'c':
        return False
    else:
        return True

def isValidPosition(code, pos):
    """
    Return true if the 'pos' is a valid _position.
    Return false otherwise.
    :param pos: An offset in this code
    :param code: A list of choices
    :return: Boolean true or false
    """
    if 1 > pos: return False
    if len(code) <= pos: return False
    return True

def mutate(code):
    """
    Apply the simulation mutations to this Gene's _gene
    """
    applyFlips(code)
    applyDeletions(code)
    applyInsertions(code)

def applyFlips(code):
    """
    Proceed over the code and apply flip mutations
    according to the probabilty of a flip.
    :param code: List<char> a list of character as code
    :return: None
    """
    for x in range(1, len(code)):
        if params['mutation_chance_flip'] > random.random():
            code[x] = getOtherChoice(code[x])
    return None

def applyDeletions(code):
    """
    Apply deletions over this Gene's _gene according
     to the probability of a deletion per choice in
     the length of the Gene's _gene
    :param code: List<char> a list of character as code
    """
    # We cannot delete a choice if the length of the
    # code is already only 2 long. 2 long is just
    # 1 choice.

    for x in range(1, len(code)):
        if len(code) <= 2:
            break;
        if params['mutation_chance_delete'] > random.random():
            removeChoice(code, x)

def applyInsertions(code):
    """
    Apply any mutational insertions to this Gene's _gene
    according to the probability of insertion per choice
    over the length of the Gene's gene.
    :param code: List<char> a list of character as code
    :return: None
    """
    for x in range(1, len(code)):
        if params['mutation_chance_insert'] > random.random():
            insertChoice(code, getRandomChoice(), x)
    return None

def insertChoice(code, choice, pos):
    """
    insert the choice 'c' or 'd' into the _position in the gene
    directly after 'pos'.
    :param code: List<char> a list of character as code
    :param choice: char The choice of 'c' or 'd'
    :param pos: int The _position after which to insert the choice
    :return: None
    """
    if not isValidChoice(choice):
        choice = getRandomChoice()
    if not isValidPosition(code, pos):
        code.append(choice)
    else:
        code.insert(pos, choice)
    return None

def appendChoice(code, choice):
    """
    Append the choice to the this gene
    :param code: List<char> a list of character as code
    :param choice: the choice to append
    :return: None
    """
    if not self.isValidChoice(choice):
        choice = self.getRandomChoice()
    code.append(choice)
    return None

def removeChoice(code, pos):
    """
    Remove the choice at _position 'pos' in the code.
    If the _position is not valid, the last choice is removed.
    :param code: List<char> a list of character as code
    :param pos: the _position of the choice to remove
    :return: None
    """
    if not isValidPosition(code, pos):
        pos = len(code) - 1
    del code[pos]
    return None
