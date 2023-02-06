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
    
    def surface_initialisation(self, number_points: int) -> None:
        lands = [Point(x,y) for x,y in  test_input[0]]
        self.surface = Surface(lands)
        self.landing_site_point = Point(
            self.surface.landing_site.point_b.x - self.surface.landing_site.point_b.x,
            self.surface.landing_site.point_b.y - self.surface.landing_site.point_b.y
        )

    def reset(self):
        self.lander.update(*test_input[1])



evolution_number = 10
population_size = 60
gene_size = 100
def main():
    env = EnvTest()
    number_point = int(0)
    env.surface_initialisation(number_point)
    env.reset()
    population = Population.generator(population_size,gene_size)
    for _ in range(evolution_number):
        for chromosome in population:
            if chromosome.use(env):
                print("SUCCESS")
                input()    
            else:
                
                env.reset()
        print(population.average_score())
        population.selection()
        population.mutation()



# %%
env = EnvTest()
env.surface_initialisation(0)
env.reset()
chromosome = Chromosome.generator(100)
chromosome.use(env)
# %%
action = Action(-45, 6)
print(env.lander)
env.step(action)
print(env.lander)

# %%
main()
# %%
