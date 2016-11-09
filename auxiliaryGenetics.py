import random
import Gene

_CHANCE = 0.5
P_OF_INSERTION = 0.1
P_OF_DELETION = 0.05
P_OF_FLIPPING = 0.05

def recombinate(parentA, parentB):
    """
    :param parentA: Gene Parent A's Gene
    :param parentB: Gene Parent B's Gene
    :return: A new code formed from parent A' gene's
    code and parent B's gene's code.
    """
    codeA = parentA._code
    codeB = parentB._code
    newCodeLength = (len(codeA) + len(codeB)) // 2
    # Find out which is the longer gene
    if len(codeA) < len(codeB):
        shorterParentCode = codeA
        longerParentCode = codeB
    else:
        shorterParentCode = codeB
        longerParentCode = codeA
    newGeneticCode = []
    # Calculate the length of the new gene which can and
    # cannot be generated from both parents
    sharedParentsLength = len(shorterParentCode)
    # Produce as much of the new gene from a combination of
    # both parent's _genes as is possible
    for x in xrange(0, sharedParentsLength - 1):
        newGeneticCode.append(codeA[x] if (random.randint(0, 1) == 0) else codeB[x])
    # produce the rest of the gene from the longer parent's _gene
    newGeneticCode[sharedParentsLength:] = longerParentCode[sharedParentsLength:newCodeLength - 1]
    return newGeneticCode

def getRandomChoice(chance=_CHANCE):
    """
    Produce a choice, 'c' or 'd',
    depending on the random value _CHANCE
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
    Return true if the 'pos' is a valid position.
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
    for x in xrange(1, len(code)):
        if P_OF_FLIPPING > random.random():
            code[x] = getOtherChoice(code[x])
    return None

def applyDeletions(code):
    """
    Apply deletions over this Gene's _gene according
     to the probability of a deletion per choice in
     the length of the Gene's _gene
    :param code: List<char> a list of character as code
    :return: None
    """
    for x in xrange(1, len(code)):
        if P_OF_DELETION > random.random():
            removeChoice(code, x)
    return None

def applyInsertions(code):
    """
    Apply any mutational insertions to this Gene's _gene
    according to the probability of insertion per choice
    over the length of the Gene's gene.
    :param code: List<char> a list of character as code
    :return: None
    """
    for x in xrange(1, len(code)):
        if P_OF_INSERTION > random.random():
            insertChoice(code, getRandomChoice(), x)
    return None

def insertChoice(code, choice, pos):
    """
    insert the choice 'c' or 'd' into the position in the gene
    directly after 'pos'.
    :param code: List<char> a list of character as code
    :param choice: char The choice of 'c' or 'd'
    :param pos: int The position after which to insert the choice
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
    Remove the choice at position 'pos' in the code.
    If the position is not valid, the last choice is removed.
    :param code: List<char> a list of character as code
    :param pos: the position of the choice to remove
    :return: None
    """
    if not isValidPosition(code, pos):
        pos = len(code) - 1
    del code[pos]
    return None