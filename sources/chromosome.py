import random

from sources.tools.point import Point
from sources.action import Action
from sources.envmarslander import EnvMarsLander
from sources.gene import *


class Chromosome:
    score = 0  
    landing_distance = None
    landing_point = None
    landing_on_site = None
    starting_index = 0
    
    @staticmethod
    def get_score(chromosome):
        return chromosome.score

    @staticmethod
    def generator(chromosome_size : int):
        pass

    def __str__(self) -> str:
        return "|".join(map(str, self))

    def mutation(self, probability):
        pass

    def crossover(self,other):
        pass

    def use(self):
        pass



