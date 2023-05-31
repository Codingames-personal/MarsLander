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


WEIGHTS_POWER = [1, 1, 1, 1, 4]
WEIGHTS_ROTATION = [1]*45 + [5]*16 + [1]*45

class MapGradChromosome(Chromosome):
    starting_index = 0

    def random_power():
        return random.choices([0, 1, 2, 3, 4], WEIGHTS_POWER)[0]
    
    def random_rotate():
        return random.randint(-90, 90)

    @staticmethod
    def generator(chromosome_size : int):
        x_scale = round(length_ratio*chromosome_size)
        y_scale = round(height_ratio*chromosome_size)

        vector_map_power = numpy.array([
            [MapGradChromosome.random_power() for _ in range(x_scale)]
            for _ in range(y_scale)
        ])
        vector_map_rotate = numpy.array([
            [MapGradChromosome.random_rotate() for _ in range(x_scale)]
            for _ in range(y_scale)
        ])

        return MapGradChromosome(vector_map_power, vector_map_rotate)
    

    def __init__(self, vector_map_power_, vector_map_rotate_ ):
        self.vector_map_power = vector_map_power_
        self.vector_map_rotate = vector_map_rotate_
        self.y_scale, self.x_scale = numpy.shape(vector_map_power_)
        self.chromosome_size = self.y_scale * self.x_scale

    def create_action(self, env):
        x = round(self.x_scale * env.lander.x/7000)
        y = round(self.y_scale * env.lander.y/3000)

        if not (0<= x < self.x_scale) or not (0<= y < self.y_scale):
            return Action(0, 0)
        grad_power = self.vector_map_power[y, x]
        power = max(
            -1,
            min(
                1,
                grad_power - env.lander.power
            )

        )
        grad_rotate = self.vector_map_rotate[y, x]
        rotate = max(
            -15,
            min(
                15,
                grad_rotate - env.lander.rotate
            )
        )

        
        return Action(rotate, power)
    
    
    def mutation(self, probability):
        if random.random() < probability:
            x = random.randint(0, self.x_scale-1)
            y = random.randint(0, self.y_scale-1)
            self.vector_map_power[y, x] = MapGradChromosome.random_power()
            self.vector_map_rotate[y, x] = MapGradChromosome.random_rotate()
        
    def crossover(self, other : object):
        random_percent = random.random()
        c0_vector_map_power = random_percent*self.vector_map_power + (1-random_percent)*other.vector_map_power
        c1_vector_map_power = random_percent*other.vector_map_power + (1-random_percent)*self.vector_map_power
        c0_vector_map_rotate = random_percent*self.vector_map_rotate + (1-random_percent)*other.vector_map_rotate
        c1_vector_map_rotate = random_percent*other.vector_map_rotate + (1-random_percent)*self.vector_map_rotate
    
        return (
            MapGradChromosome(c0_vector_map_power, c0_vector_map_rotate),
            MapGradChromosome(c1_vector_map_power, c1_vector_map_rotate)
        )
# %%
