##
#%%
from main import * 
import pygame
import os
import sys


ENV_HEIGHT = 3000
ENV_WIDTH = 7000

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1200

FRAMES_PER_SECOND = 1

fx = lambda x : int(WINDOW_WIDTH * x / ENV_WIDTH)
fy = lambda y : WINDOW_HEIGHT - int(WINDOW_HEIGHT * y / ENV_HEIGHT)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

image_directory_path = "/home/smaug/Documents/CodingGames/MarsLander/image/"

test_input = [
    [[0, 1500],[1000, 2000], [2000, 500], [3500, 500], [5000, 1500], [6999, 1000]],
    [5000, 2500, 0, 0, 1000, 0, 0]
]
test_grotte = [
    [[0, 450], [300, 750], [1000, 450], [1500, 650], [1800, 850], [2000, 1950], [2200, 1850], [2400, 2000], [3100, 1800], [3150, 1550], [2500, 1600], [2200, 1550], [2100, 750], [2200, 150], [3200, 150], [3500, 450], [4000, 950], [4500, 1450], [5000, 1550], [5500, 1500], [6000, 950], [6999, 1750]],
    [6500, 2600, -20, 0, 10001, 45, 0]
]

test_grotte_inv = [
    [[0, 1800], [300, 1200], [1000, 1550], [2000, 1200], [2500, 1650], [3700, 220], [4700, 220], [4750, 1000], [4700, 1650], [4000, 1700], [3700, 1600], [3750, 1900], [4000, 2100], [4900, 2050], [5100, 1000], [5500, 500], [6200, 800], [6999, 600]],
    [6500, 2000, 0, 0, 12001, 0, 0]
]

class EnvRender(EnvMarsLander):
    def __init__(self,lands : list, initial_state : list):
        super().__init__(lands, initial_state)
        self.env_id = 0
        pygame.init()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        
        #self.lander_image = pygame.image.load(image_directory_path+"lander.png").convert()

    def screen_reset(self):
        self.display.fill(BLACK)
        self.draw_surface()
        
    def reset(self):
        super().reset()
        self.trajectory = []

    def render_reset(self):
        self.env_id +=1
        self.screen_reset()
        id_text = self.font.render("Population : " + str(self.env_id), True, (255, 255, 255))
        self.display.blit(id_text, (100, 100))

    def draw_surface(self):
        for line in self.surface.lines():
            pygame.draw.line(
                self.display, 
                RED, 
                [fx(line.point_a.x), fy(line.point_a.y)],
                [fx(line.point_b.x), fy(line.point_b.y)]
            )

    def step(self,action):
        done = super().step(action)
        self.trajectory.append([self.lander.x,self.lander.y])
        #pygame.transform.rotate(self.lander_image,self.rotate)
        
        if done :
            if self.successful_landing():
                self.env_id -=1
                self.render_reset()
                color = GREEN
                width_ = 5

            else:
                color = BLUE
                width_ = 1
            x_, y_ = self.trajectory[0]
            for x,y in self.trajectory[1:]:
                pygame.draw.line(
                    self.display, 
                    color, 
                    [fx(x_), fy(y_)],
                    [fx(x), fy(y)],
                    width=width_
                )
                x_, y_ = x, y

        return done
      

    
# %%

evolution_number = 200
population_size = 100
gene_size = 400

env = EnvRender(*test_input)
env.reset()
env.render_reset()
population = Population.generator(population_size, gene_size)

while True:
    success = False
    for chromosome in population:
        
        if chromosome.use(env):
            print("------SUCCESS------")
            print(f"Population {env.env_id}")
            print(env)
            success = True
            break
        env.reset()
    

    c = population.selection()
    
    population.mutation()
    pygame.display.flip()
    pygame.event.wait()

    while True:
        event = pygame.event.wait()
        if success:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
               break
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                break
        
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    env.render_reset()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()







# %%
