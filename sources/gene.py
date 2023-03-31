##
#%%

from sources.action import *
import random

class Gene:
    def __init__(self):
        pass

    def mutate(self):
        pass
    

class LinearGene(Gene):
    def __init__(self):
        self.weight = 0

    def mutate(self):
        self.weight = random.random()

