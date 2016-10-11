import random

def GetRandomChoice():
    chance = random.random();
    if (0.5 > chance):
        choice = 'd'
    else:
        choice = 'c'
    return choice