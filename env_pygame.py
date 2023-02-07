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

image_directory_path = "/home/smaug/Documents/CodingGames/MarsLander/image/"

test_input = [
    [[0, 1500],[1000, 2000], [2000, 500], [3500, 500], [5000, 1500], [6999, 1000]],
    [5000, 2500, -50, 0, 1000, 90, 0]
]

class EnvRender(EnvMarsLander):
    def __init__(self):
        super().__init__()
        pygame.init()
        
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.lander_image = pygame.image.load(image_directory_path+"lander.png").convert()
        self.clock = pygame.time.Clock()

    def reset(self):
        self.lander.update(*test_input[1])
        self.trajectory = []
    
    def draw_text(self,string, x ,y , fontSize=1000 ): #Function to set text

        font = pygame.font.Font('freesansbold.ttf', fontSize)
        #(0, 0, 0) is black, to make black text
        text = font.render(string, True, WHITE) 
        textRect = text.get_rect()
        textRect.center = (x,y) 

    def draw_trajectory(self):
        for x,y in self.trajectory:
            self.display.set_at((fx(x), fy(y)), BLUE)

    def draw_surface(self):
        for line in self.surface.lines():
            pygame.draw.line(
                self.display, 
                RED, 
                [fx(line.point_a.x), fy(line.point_a.y)],
                [fx(line.point_b.x), fy(line.point_b.y)]
            )

    def render(self):
        self.display.fill(BLACK)
        self.draw_surface()
        self.draw_trajectory()
        self.draw_text(f"x : {self.lander.x}", fx(1000), fy(1000))
        self.draw_text(f"y : {self.lander.y}", fx(1000), fy(1200))
        """self.display.blit(
            self.lander_image,
            [fx(self.lander.x),fy(self.lander.y)]
        )"""
        pygame.display.flip()
        pygame.display.update()
        

    def surface_initialisation(self, number_points: int) -> None:
        lands = [Point(x,y) for x,y in test_input[0]]
        self.surface = Surface(lands)
        self.landing_site_point = Point(
            self.surface.landing_site.point_b.x - self.surface.landing_site.point_b.x,
            self.surface.landing_site.point_b.y - self.surface.landing_site.point_b.y
        )
        self.display.fill(BLACK)


    def step(self,action):
        done = super().step(action)
        self.trajectory.append([self.lander.x,self.lander.y])
        #pygame.transform.rotate(self.lander_image,self.rotate)
        self.render()
        self.clock.tick(1)
        if done :
            pygame.quit()
            sys.exit()
        return done
      

    
# %%
env = EnvRender()
env.surface_initialisation(0)
env.reset()
chromosome = Chromosome.generator(100)
chromosome.use(env)
# %%
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()