import random
_CHANCE = 0.5
def GetRandomChoice(chance=_CHANCE):
    """
    Produce a choice, 'c' or 'd',
    depending on the random value _CHANCE
    :return:
    """
    return 'd' if chance > random.random() else 'c'


def getOtherChoice(self, choice):
    """
    Return the opposite choice of the argument provided
    :param choice: the choice character for which the opposite is desired
    :return: the character of the opposite choice
    """
    otherChoice = 'd' if choice == 'c' else 'c'
    return otherChoice


def isValidChoice(self, choice):
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