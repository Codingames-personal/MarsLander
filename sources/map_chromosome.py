##
#%%

##Linear Chromosome
#%%
from sources.chromosome import *
##
#%%
import numpy
import sys
import random


# x axes
length_ratio = 7000/(7000+3000)
# y axes
height_ratio = 3000/(7000+3000)
##
#%%
MAXIMAL_NUMBER_OF_STEP = 200

class MapVectorChromosome(Chromosome):
    starting_index = 0

    def random_action_power():
        return random.randint(-1, 1)
    
    def random_action_rotate():
        return random.randint(-15, 15)

    @staticmethod
    def generator(chromosome_size : int):
        x_scale = round(length_ratio*chromosome_size)
        y_scale = round(height_ratio*chromosome_size)

        vector_map_power = numpy.array([
            [MapVectorChromosome.random_action_power() for _ in range(x_scale)]
            for _ in range(y_scale)
        ])
        vector_map_rotate = numpy.array([
            [MapVectorChromosome.random_action_rotate() for _ in range(x_scale)]
            for _ in range(y_scale)
        ])

        return MapVectorChromosome(vector_map_power, vector_map_rotate)
    

    def __init__(self, vector_map_power_, vector_map_rotate_ ):
        self.vector_map_power = vector_map_power_
        self.vector_map_rotate = vector_map_rotate_
        self.y_scale, self.x_scale = numpy.shape(vector_map_power_)
        self.chromosome_size = self.y_scale * self.x_scale

    def function(self, lander):
        x = round(self.x_scale * lander.x/7000)
        y = round(self.y_scale * lander.y/3000)

        dpower = self.vector_map_power[y, x]
        drotate = self.vector_map_rotate[y, x]
        return Action(drotate, dpower)
    
    def use(self, env):
        
        for _ in range(MAXIMAL_NUMBER_OF_STEP):
            action = self.function(env.lander)
            if env.step(action):
                break
            
        self.landing_distance = env.landing_distance()

        if not env.successful_landing():
            self.landing_on_site = env.landing_on_site()
            self.landing_point = Point(env.lander.x, env.lander.y)
            self.score = env.get_score()
            return False
        return True
    
    def mutation(self, probability):
        if random.random() < probability:
            x = random.randint(0, self.x_scale)
            y = random.randint(0, self.y_scale)
            self.vector_map_power[y, x] = MapVectorChromosome.random_action_power()
            self.vector_map_rotate[y, x] = MapVectorChromosome.random_action_rotate()
        
    def crossover(self, other : object):
        random_percent = random.random()
        c0_vector_map_power = numpy.round(random_percent*self.vector_map_power + (1-random_percent)*other.vector_map_power)
        c1_vector_map_power = numpy.round(random_percent*other.vector_map_power + (1-random_percent)*self.vector_map_power)
        c0_vector_map_rotate = numpy.round(random_percent*self.vector_map_rotate + (1-random_percent)*other.vector_map_rotate)
        c1_vector_map_rotate = numpy.round(random_percent*other.vector_map_rotate + (1-random_percent)*self.vector_map_rotate)
    
        return (
            MapVectorChromosome(c0_vector_map_power, c0_vector_map_rotate),
            MapVectorChromosome(c1_vector_map_power, c1_vector_map_rotate)
        )
# %%
