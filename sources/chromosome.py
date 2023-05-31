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
        chromosome = Chromosome()
        return chromosome

    def __str__(self) -> str:
        return "|".join(map(str, self))

    def mutation(self, probability):
        pass

    def crossover(self,other):
        pass

    def create_action(self):
        pass

    def use(self, env : EnvMarsLander):
        done = False

        while not done:
            done = env.step(self.create_action(env))
        
        self.landing_point = Point(env.lander.x, env.lander.y)
        self.landing_distance = env.landing_distance()

        if done and not env.successful_landing():
            self.landing_on_site = env.landing_on_site()
            self.score = env.get_score()
            return False
        
        return True




