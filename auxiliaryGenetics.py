import random
_CHANCE = 0.5
def GetRandomChoice(chance=_CHANCE):
    """
    Produce a choice, 'c' or 'd',
    depending on the random value _CHANCE
    :return:
    """
    return 'd' if chance > random.random() else 'c'
