##
#%%
from main import *

test_input = [
    [[0, 1500],[1000, 2000], [2000, 500], [3500, 500], [5000, 1500], [6999, 1000]],
    [5000, 2500, -50, 0, 1000, 90, 0],
    [4950, 2498, -51, -3, 999, 75, 1],
    [4898, 2493, -53, -6, 997, 60, 2]
]	
test_output = [
    [-45, 4],
    "-45 4",
    "-45 4"
]


class EnvTest(EnvMarsLander):
    def __init__(self,test_input):
        super().__init__(test_input[0],test_input[1])
        self.test_input = test_input

    def reset(self):
        self.lander.update(*self.test_input[1])



evolution_number = 10
population_size = 60
gene_size = 100
def main():
    env = EnvTest(test_input)
    env.reset()
    population = Population.generator(population_size,gene_size)
    for _ in range(evolution_number):
        for chromosome in population:
            if chromosome.use(env):
                
                input()    
            else:
                
                env.reset()
        print(population.average_score())
        population.selection()
        population.mutation()



# %%
