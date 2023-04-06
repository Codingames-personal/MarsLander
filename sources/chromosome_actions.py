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
        actions = [Action.generator() for _ in range(chromosome_size)]
        chromosome = Chromosome(actions)
        chromosome.chromosome_size = chromosome_size
        return chromosome

    def __init__(self, actions=[]):
        self.chromosome_size = len(actions)
        self.actions = actions


    def __str__(self) -> str:
        return "|".join(map(str, self.actions))

    def __iter__(self):
        self.i = self.starting_index
        return self
    
    def __next__(self):
        if self.i < len(self.actions):
            self.i+=1
            return self.actions[self.i-1]
        else:
            raise StopIteration

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __eq__(self, other) -> bool:
        for g0,g1 in zip(self, other):
            if not g0 == g1:
                return False
        return True

    def add(self, action : Action):
        self.actions.append(action)

    def extend(self, actions : list):
        for action in actions:
            self.add(action)

    def size(self):
        return len(self.actions)

    def mutation(self, probability):
        #probability = max(probability, 0.03*(1-self.score/200))
        self.score = 0
        for gene in self:
            if random.random() < probability:
                gene.mutate()
        
    def crossover(self,other):
        random_percent = random.random()
        child0,child1 = [], []

        for g0,g1 in zip(self.actions, other.actions):
            rotate0 = round(random_percent * g0.rotate + (1-random_percent) * g1.rotate)
            rotate1 = round(random_percent * g1.rotate + (1-random_percent) * g0.rotate)
            power0 = round(random_percent * g0.power + (1-random_percent) * g1.power)
            power1 = round(random_percent * g1.power + (1-random_percent) * g0.power)
            child0.append(Action(rotate0, power0))
            child1.append(Action(rotate1, power1))

        return Chromosome(child0), Chromosome(child1)
    
    def use(self, env : EnvMarsLander, step = 1000):
        done = False
        self.score = 0
        for gene, _ in zip(self.actions, range(step)):
            done = env.step(gene)
            if done:
                gene.last_action(env.lander.rotate)
                self.landing_distance = env.landing_distance()
                break

        self.landing_point = Point(env.lander.x, env.lander.y)
        if done and not env.successful_landing(): 
            self.landing_on_site = env.landing_on_site()
            self.score = env.get_score()
            return False
        
        return done



