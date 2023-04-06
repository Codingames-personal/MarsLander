##Linear Chromosome
#%%
from sources.chromosome import *
##
#%%
import numpy
import sys
import random

dimension = 3

def random_array(shape):
    return numpy.array([[
        random.random() for _ in range(shape[1])
    ] for _ in range(shape[0])
    ])

def random_vector(shape):
    return random_array((shape,1))

def random_diagonal(shape):
    return numpy.random.randn(shape)*numpy.identity(shape)

unit_vetcor = numpy.ones(3)

sigmoid = lambda x : 1 / (1 + numpy.exp(-x))

class ProbabilyLaw:
    def __init__(self, random_array_func_) -> None:
        self.random_array_func = random_array_func_

    def random_array(self, shape):
        return self.random_array_func(*shape)

    def random_diag(self, shape):
        return self.random_array_func(shape)*numpy.identity(shape)


uniform = ProbabilyLaw(numpy.random.rand)

gaussien = ProbabilyLaw(numpy.random.randn)

##
#%%
MAXIMAL_NUMBER_OF_STEP = 200

class LinearChromosome(Chromosome):
    starting_index = 0
    function_power_max = 0
    function_rotate_max = 0
    function_power_min = 1e8
    function_rotate_min = 1e8

    @staticmethod
    def generator(chromosome_size : int, probability_law = uniform):
        
        chromosome_shape = (chromosome_size, dimension)
        weights_power = numpy.random.randn(*chromosome_shape)
        weights_rotate = numpy.random.randn(*chromosome_shape)
        bias_power = random_diagonal(dimension)
        bias_rotate = random_diagonal(dimension)
        chromosome = LinearChromosome(
            weights_power, weights_rotate, bias_power, bias_rotate
        )
        """for i in range(chromosome_size):
            number_of_weights = max(7, i*7*(i*7+1)/2)
    
            chromosome.weights_power.extend(
                [random.random() for _ in range(number_of_weights)]
            )
            chromosome.weights_rotate.extend(
                [random.random() for _ in range(number_of_weights)]
            )"""

        chromosome.chromosome_size = chromosome_size
        return chromosome
    

    def __init__(self, weights_power, weights_rotate, bias_power, bias_rotate):
        self.weights_power = weights_power
        self.weights_rotate = weights_rotate
        self.bias_power = bias_power
        self.bias_rotate = bias_rotate
        self.chromosome_size = len(weights_power)

 
    def __iter__(self):
        return iter(zip(self.weights_power, self.weights_rotate))
    
    def __next__(self):
        return next(self)
    
    def features_extract(self, env):
        coarse_map = env.coarse_mapping(self.chromosome_size)
        coarse_speed, coarse_action = env.coarse_obs(self.chromosome_size)
        return numpy.array([
            coarse_map,
            coarse_speed,
            coarse_action
        ])
    
    def function_uniforme(self, x):
        function_power = numpy.trace(numpy.dot(x, self.weights_power) + self.bias_power)/(4*self.chromosome_size + 1)
        function_rotate = numpy.trace(numpy.dot(x, self.weights_rotate) + self.bias_rotate)/(4*self.chromosome_size + 1)
        return function_power, function_rotate


    def function_sigmoid(self, x):
        function_power = numpy.trace(numpy.dot(x, self.weights_power) + self.bias_power)
        function_rotate = numpy.trace(numpy.dot(x, self.weights_rotate) + self.bias_rotate)
        return sigmoid(function_power), sigmoid(function_rotate)
    

    def linear_predictor(self, x):  
        power_percent, rotate_percent = self.function_sigmoid(x)
        power = round(power_percent*4)
        rotate = round(rotate_percent*30 -15)
        return Action(rotate, power)

    def use(self, env):

        for _ in range(MAXIMAL_NUMBER_OF_STEP):
            x = self.features_extract(env)
            action = self.linear_predictor(x)

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
        for w_index in range(self.chromosome_size):
            if random.random() < probability:
                self.weights_power[w_index] = random.random()
            if random.random() < probability:
                self.weights_rotate[w_index] = random.random()
            
        
    def crossover(self, other):
        
        random_percent = random.random()
        c0_weights_power = random_percent*self.weights_power + (1 - random_percent)*other.weights_power
        c1_weights_power = random_percent*other.weights_power + (1 - random_percent)*self.weights_power
        c0_weights_rotate = random_percent*self.weights_rotate + (1 - random_percent)*other.weights_rotate
        c1_weights_rotate = random_percent*other.weights_rotate + (1 - random_percent)*self.weights_rotate
        c0_bias_power = random_percent*self.bias_power + (1 - random_percent)*other.bias_power
        c1_bias_power = random_percent*other.bias_power + (1 - random_percent)*self.bias_power
        c0_bias_rotate = random_percent*self.bias_rotate + (1 - random_percent)*other.bias_rotate
        c1_bias_rotate = random_percent*other.bias_rotate + (1 - random_percent)*self.bias_rotate
        
    
        return (
            LinearChromosome(c0_weights_power, c0_weights_rotate, c0_bias_power, c0_bias_rotate),
            LinearChromosome(c1_weights_power, c1_weights_rotate, c1_bias_power, c1_bias_rotate)
        )

# %%
