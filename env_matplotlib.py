##
#%%
from main import * 
import matplotlib.pyplot as plt
      
ENV_HEIGHT = 3000      
ENV_WIDTH = 7000

test_input = [
    [[0, 1500],[1000, 2000], [2000, 500], [3500, 500], [5000, 1500], [6999, 1000]],
    [5000, 2500, -50, 0, 1000, 90, 0]
]

test_input2 = [
    [[0, 1500], [1000, 2000], [2000, 500], [3500, 500], [5000, 1500], [6999, 1000]],
    [5000, 2500, 0, 0, 500, 0, 0]
]

class EnvRender(EnvMarsLander):
    def __init__(self,lands,initial_state):
        super().__init__(lands,initial_state)
        self.number_state = 0

    def reset(self):
        super().reset()
        self.draw_surface()
        self.number_state = 0
        self.trajectory = [[],[]]
    
    def draw_surface(self):
        for line in self.surface.lines():
            plt.plot([line.point_a.x,line.point_b.x],[line.point_a.y,line.point_b.y],"-r")

    def step(self,action):
        self.number_state +=1
        done = super().step(action)
        self.trajectory[0].append(self.lander.x)
        self.trajectory[1].append(self.lander.y)
        """
        color = str(abs(self.lander.rotate)/90)
        plt.plot(self.lander.x,self.lander.y, 
            marker = "o",
            markersize=4,
            markerfacecolor=(color),
            markeredgecolor=(color)
        )"""

        if done:
            plt.plot(self.trajectory[0],self.trajectory[1], '-b')
        return done
      
##
#%%
evolution_number = 200
population_size = 80
gene_size = 200

def main():
    
    env = EnvMarsLander(test_input2[0],test_input2[1])
    env_render = EnvRender(test_input2[0],test_input2[1])
    env.reset()
    env_render.reset()
    population = Population.generator(population_size,gene_size)

    for i in range(evolution_number):
        for chromosome in population:
            if chromosome.use(env):
                print("------SUCCESS------")
                print(f"With {i} evolution")
                chromosome.use(env_render)
                print(f"Fuel : {env.lander.fuel}")
                print(f"Speed : vertical {env.lander.v_speed} | horizontal {env.lander.h_speed}")
                print(f"Coords : {env.lander.x} {env.lander.y}")
                print(f"Angle : {env.lander.rotate}")
                return chromosome

            env.reset()

        chromosome = population.selection()
        population.mutation()
        env.reset()
        chromosome.use(env_render)
        env_render.reset()
        
        if i%50 == 0:
            chromosome.use(env)
            
            print(f"Best score {chromosome.score}")
            print(f"Speed : vertical {env.lander.v_speed} | horizontal {env.lander.h_speed}")
            print(f"Coords : {env.lander.x} {env.lander.y}")
            print(f"Angle : {env.lander.rotate}")
            env.reset()
    
    print("Last one")
    chromosome.use(env)
    #chromosome.use(env_render)
    print(f"Population size {population.size()}")
    print(f"Best score {chromosome.score}")
    print(f"Fuel : {env.lander.fuel}")
    print(f"Speed : vertical {env.lander.v_speed} | horizontal {env.lander.h_speed}")
    print(f"Coords : {env.lander.x} {env.lander.y}")
    print(f"Angle : {env.lander.rotate}")
    plt.show()
   
chromosome = main()

# %%
