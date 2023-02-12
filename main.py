##
#%%

import random
import math

sign = lambda x : (x>0) - (x<0)
round_up = math.ceil
input_codingames = lambda : list(map(int,input().split()))


GRADED_RETAIN_PERCENT = 0.2    # percentage of retained best fitting individuals
NONGRADED_RETAIN_PERCENT = 0.2  # percentage of retained remaining individuals (randomly selected)
MUTATION_PROBABILITY = 0.01

sigmoid = lambda x : math.exp(-x)

class Action:
    """Action of the lander
        rotate : [-15,15]
            action of rotation
        power : {-1,1}
            action of power
    """

    @staticmethod
    def generator():
        action = Action(0,0)
        action.mutation()
        return action

    def __init__(self,rotate : int, power : int):
        self.rotate = rotate
        self.power = power

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def __eq__(self, other) -> bool:
        return self.rotate == other.rotate and self.power == other.power

    def mutation(self) -> None:
        """ Set up the action with random setings"""
        self.rotate = random.randint(-15,15)
        self.power = random.choice([-1, 0, 0, 0, 1, 1, 1, 1])

    def last_action(self,rotate,v_speed):
        """Choose the best action to choose"""
        if abs(v_speed) <= 4:
            self.power = 1
        self.rotate = -rotate
                    
##
#%% ------------------ENVIRONMENT------------------------------

class EnvironmentError(Exception):
    pass

class Point:
    """Define point of space
        x : [0, 6999]
        y : [0, 2999]
    """
    def __init__(self, x : int, y : int):
        self.x = min(6999,max(0,x))
        self.y = min(2999,max(0,y))

    def __str__(self):
        return f"{self.x} {self.y}"

    def __eq__(self, other) -> bool:
        return (self.x == other.x and self.y == other.y)

    def distance(self, other) -> float:
        """Calcul the distance between two points"""
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2 )

class Line:
    """Define a segment in space
        point_a : Point
        point_b : Point
    """
    @staticmethod
    def ccw(A : Point, B : Point, C : Point) -> bool:
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

    def __init__(self, point_a : Point, point_b : Point ):
        self.point_a = point_a
        self.point_b = point_b
    
    def __iter__(self):
        return iter([self.point_a,self.point_b])

    def __next__(self):
        return next(self)

    def __eq__(self, other)  -> bool:
        return self.point_a == other.point_a and self.point_b == other.point_b

    def __str__(self) -> str:
        return f"{self.point_a} | {self.point_b}"

    def lenght(self):
        return self.point_a.distance(self.point_b)

    def collision(self,point_c,point_d):
        """Look if the segment self and [point_c, point_d] segment's intersect"""
        return Line.ccw(self.point_a,point_c,point_d) != Line.ccw(self.point_b, point_c, point_d) \
            and Line.ccw(self.point_a, self.point_b, point_c) != Line.ccw(self.point_a, self.point_b, point_d)
    
class Lander:
    """Define the lander
        x : [0, 6999]
            Coordinate on the horizontal axe
        y : [0, 2999]
            Coordinate on the vertical axe
        h_speed : [-499, 499] 
            horizontal speed
        v_speed : [-499, 499] 
            vertical speed
        fuel : [0, 2000] 
            fuel that remains
        rotate : [-90, 90] 
            angle of the lander with 0 deg at the zenith
        power : [0, 4]
            power of the engine 
        """
    def __str__(self):
        try:
            return f"{self.x} {self.y} {self.h_speed} {self.v_speed} {self.fuel} {self.rotate} {self.power}"
        except AttributeError :
            return "Lander not yiet initialized"
        
    def copy(self,other):
        """Copy other into self"""
        self.update(
            other.x, 
            other.y,
            other.h_speed, 
            other.v_speed, 
            other.fuel, 
            other.rotate, 
            other.power
        )
    def update(self,x ,y ,h_speed ,v_speed ,fuel ,rotate ,power):
        """Update the caracteristics of the lander"""
        self.x = x
        self.y = y
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.fuel = fuel
        self.rotate = rotate
        self.power = power
        
class Surface:
    """Define the shape of the surface
        lands : [Point]
    """
    def __init__(self,lands=[]):
        self.lands = lands
        self.find_landing_site()
        self.find_distance_maximum()

    def __iter__(self):
        return iter(self.lands)
    
    def __next__(self):
        return next(self)

    def lines(self):
        """Generator of lines"""
        point_a = self.lands[0]
        for point_b in self.lands[1:]:
            yield Line(point_a,point_b)
            point_a = point_b
    
    def find_distance_maximum(self):
        """Find the maximal distance by walk of the landing"""
        distance = 0
        for line in self.lines():
            if line == self.landing_site:
                distance_left = distance
                distance = 0
            else:
                distance += line.lenght()
        self.distance_maximum = max(distance_left, distance)

    def find_landing_site(self) -> None:
        """Find the landing site, the only flat ground of the surface"""
        for line in self.lines():
            if line.point_a.y == line.point_b.y:
                self.landing_site = line
                return None
        raise EnvironmentError()

    def collision(self,point_a,point_b) -> bool:
        """Find out if there was a collision when the lander went from point_a to point_b"""
        for line in self.lines():
            if line.collision(point_a,point_b):
                self.collision_line = line
                return True
        return False

class EnvMarsLander:
    """ Environment of the Mars Lander puzzle of CodinGames"""
    GRAVITY = - 3.711 # gravity on Mars m.s-2

    def __init__(self, lands : list, initial_state : list):
        self.lands = lands
        self.initial_state = initial_state
        self.lander = Lander()
        self.previous_lander = Lander()
        self.surface = Surface(
            list(map(lambda obs : Point(obs[0],obs[1]), self.lands))
        )
        self.landing_site_point = Point(
            self.surface.landing_site.point_b.x - self.surface.landing_site.point_b.x,
            self.surface.landing_site.point_b.y - self.surface.landing_site.point_b.y
        )

    def __str__(self) -> str:
        score_info = f"Score : {self.get_score()}"
        coord_info = f"Coords : x {self.lander.x} | y {self.lander.y}"
        speed_info = f"Speed : h_speed {self.lander.h_speed} | v_speed {self.lander.v_speed}"
        rotate_info = f"Rotate {self.lander.rotate}"
        fuel_info = f"Fuel : {self.lander.fuel}"

        return "\n".join([score_info,coord_info,speed_info,rotate_info,fuel_info])

    def distance(self):
        """ Calculate the distance by "walke" of the collision to the landing site"""
        if self.landing_on_site():
            return 0 
        point_lander = Point(self.lander.x,self.lander.y)
        run = False
        distance = 0
        for point in self.surface:
            if not run :
                if point == self.surface.collision_line.point_a: # from left to the right 
                    point_from = point
                    point_to = self.surface.collision_line.point_b
                    point_final = self.surface.landing_site.point_a
                    distance = point_lander.distance(self.surface.collision_line.point_b)
                    run = True

                elif point == self.surface.landing_site.point_b: # from right to the left
                    point_from = self.surface.landing_site.point_a
                    point_to = point
                    point_final = self.surface.collision_line.point_a
                    distance = self.surface.collision_line.point_a.distance(point_lander)
                    run = True
                    
            else:
                point_from, point_to = point_to, point
                distance += point_from.distance(point_to)
                if point == point_final:
                    break
        return distance

    def reset(self):
        """Reset the lander"""
        self.lander.update(*self.initial_state)
        self.score = 0

    def exit_zone(self) -> bool:
        return not (0<= self.lander.x < 7000 and 0<= self.lander.y < 3000)

    def landing_on_site(self) -> bool:
        return self.surface.landing_site.collision(
            self.point_lander_before,
            self.point_lander_now   
        )

    def landing_angle(self) -> bool:
        return self.lander.rotate == 0

    def landing_vertical_speed(self) -> bool:
        return abs(self.lander.v_speed) <= 40

    def landing_horizontal_speed(self) -> bool:
        return abs(self.lander.h_speed) <= 20

    def successful_landing(self) -> bool:
        """For a landing to be successful, the ship must:
            - land on flat ground
            - land in a vertical position (tilt angle = 0°)
            - vertical speed must be limited ( ≤ 40m/s in absolute value)
            - horizontal speed must be limited ( ≤ 20m/s in absolute value)
        """
        return (\
            self.landing_on_site() and\
            self.landing_angle() and\
            self.landing_vertical_speed() and\
            self.landing_horizontal_speed()
            )

    def get_score_distance(self):
        if self.landing_on_site():
            return 200
        return round(100*(1 - self.distance()/self.surface.distance_maximum))

    def get_score_speed(self):
        if self.landing_on_site():
            score = min(0, 40 - abs(self.lander.v_speed))
            score += min(0, 20 - abs(self.lander.h_speed))
        else:
            abs_speed = math.sqrt(self.lander.v_speed**2 + self.lander.h_speed**2)
            score = min(0, round(20*(- abs_speed/150))) # 150 : max speed estimated
            score = 0
        return score

    def get_score_angle(self):
        return round(20*(1 - abs(self.lander.rotate)/90))

    def get_score(self):
        if self.exit_zone():
            return 0
        score = self.get_score_distance() + self.get_score_speed()
        if self.landing_on_site():
            self.score = max(100,min(200,score))
            if 180<=self.score:
                self.score += self.get_score_angle()
        else:
            self.score = max(0,min(100,score))

        return self.score
        

    def next_dynamics_parameters(self, rotate, power):
        h_accel = - int(math.sin(rotate*math.pi/180) * power)
        v_accel = int(EnvMarsLander.GRAVITY + math.cos(rotate*math.pi/180) * power)

        h_speed = self.lander.h_speed + h_accel
        v_speed = self.lander.v_speed + v_accel

        x = self.lander.x + h_speed
        y = self.lander.y + v_speed

        return x, y, h_speed, v_speed

    def step(self,action : Action) -> bool:
        """        
        -rotate is the desired rotation angle for Mars Lander. 
        Please note that for each turn the actual value of the angle 
        is limited to the value of the previous turn +/- 15°.
        
        - power is the desired thrust power. 
        0 = off. 4 = maximum power. 
        Please note that for each turn the value of the actuaNl power 
        is limited to the value of the previous turn +/- 1.
        """
        
        rotate = max(-90, min(
            90,
            self.lander.rotate + action.rotate
        )) 

        power = max(0, min(
            4,
            self.lander.power + action.power
        ))

        fuel = self.lander.fuel - power

        x, y, h_speed, v_speed = self.next_dynamics_parameters(rotate, power)

        self.point_lander_before = Point(self.lander.x,self.lander.y)
        self.point_lander_now = Point(x, y)

        collision = self.surface.collision(
            self.point_lander_before,
            self.point_lander_now
        )
        done = (fuel <= 0
            or not 0 <= x < 7000 \
            or  not 0 <= y < 3000 \
        )

        if collision and 0<abs(self.lander.rotate)<=15 :
            rotate = 0
            x, y, h_speed, v_speed = self.next_dynamics_parameters(rotate, power)

            
        self.lander.update(x, y, h_speed, v_speed, fuel, rotate, power)
        return done or collision

class Codingames:
    def __init__(self,initial_state):
        self.rotate = initial_state[-2]
        self.power = initial_state[-1]

    def step(self,action):
        rotate = action.rotate + self.rotate
        power = action.power + self.power
        self.rotate = max(-90, min(90, rotate))
        self.power = max(0, min(4, power))
        print(self.rotate, self.power)   
        obs = input().split()
        self.rotate = obs[-2]
        self.power = obs[-1]
        return False

class Chromosome:
    
    @staticmethod
    def score(chromosome):
        return chromosome.score

    @staticmethod
    def generator(gene_size : int):
        actions = [Action.generator() for _ in range(gene_size)]
        chromosome = Chromosome(actions)
        return chromosome

    def __init__(self, actions=[]):
        self.actions = actions
        self.score = 0

    def __str__(self) -> str:
        return "|".join(map(str,self.actions))

    def __iter__(self):
        return iter(self.actions)
    
    def __next__(self):
        return next(self)

    def __eq__(self, other) -> bool:
        for g0,g1 in zip(self, other):
            if not g0 == g1:
                return False
        return True

    def add(self,action : Action):
        self.actions.append(action)

    def size(self):
        return len(self.actions)

    def mutation(self,epsilon=1):
        self.score = 0
        for action in self:
            if random.random() > epsilon:
                action.mutation()
        
    def crossover(self,other):
        random_percent = random.random()
        child0,child1 = [], []
        for g0,g1 in zip(self,other):
            rotate0 = round(random_percent * g0.rotate + (1-random_percent) * g1.rotate)
            rotate1 = round(random_percent * g1.rotate + (1-random_percent) * g0.rotate)
            power0 = round(random_percent * g0.power + (1-random_percent) * g1.power)
            power1 = round(random_percent * g1.power + (1-random_percent) * g0.power)
            child0.append(Action(rotate0,power0))
            child1.append(Action(rotate1,power1))
        return Chromosome(child0), Chromosome(child1)
    
    def use(self,env):
        done = False
        self.score = 0
        for gene in self:
            done = env.step(gene)
            if done:
                break

        if not env.successful_landing():
            self.score = env.get_score()
            if not done:
                print("Not enough action")
            return False
        return True
            
class Population:
    @staticmethod
    def generator(population_size, gene_size):
        chromosomes = [Chromosome().generator(gene_size) for _ in range(population_size)]
        population = Population(chromosomes)
        population.population_size = population_size
        return population

    def __init__(self,chromosomes = []):
        self.chromosomes = chromosomes
        self.population_size = len(chromosomes)
        

    def __str__(self) -> str:
        return "\n".join(map(str, self.chromosomes))

    def __iter__(self):
        return iter(self.chromosomes)

    def __next__(self):
        return next(self)

    def sorted_score(self):
        return sorted(
            self.chromosomes, key=Chromosome.score, reverse=True
        )
    
    def add(self, chromosome : Chromosome):
        for chromosome0 in self:
            if chromosome0 == chromosome:
                return False
        self.chromosomes.append(chromosome)
        return True

    def size(self):
        return len(self.chromosomes)

    def roulette_wheel_cumulative(self):
        size_nongraded_retain = int((1 - GRADED_RETAIN_PERCENT) * self.population_size)
        total_score = sum(map(Chromosome.score, self.chromosomes))

        scores = list(
            map(
                lambda chromosome : [chromosome.score/total_score,chromosome],
                self.chromosomes
            ))
        cumulative_sum = 0
        
        for i in range(len(scores)):
            cumulative_sum += scores[i][0] 
            scores[i][0] = cumulative_sum 

        #chromosome_couple = [[i] for i in range(len(self.chromosomes))]
        chromosome_selection = []
        paired = False
        for _ in range(size_nongraded_retain):
            random_percent = random.random()
            i = 0
            if not paired:
                while scores[i][0] < random_percent : i+=1
                index_parent = i
                chromosome_parent0 = scores[i][1]
                paired = True
            else:
                while scores[i][0] < random_percent : i+=1
                #chromosome_couple[index_parent].append(i)
                #chromosome_couple[i].append(index_parent)
                couple = [chromosome_parent0,scores[i][1]]
                chromosome_selection.append(couple)
                paired = False
        return chromosome_selection

    def roulette_wheel(self):
        paired = False
        chromosome_tree = [[i] for i in range(len(self.chromosomes))]
        for chromosome in random.choices(
            self.chromosomes,
            weights=map(Chromosome.score, self.chromosomes),
            k = self.population_size):
            if not paired:
                parent0 = chromosome
                paired = True
            else:
                yield [parent0, chromosome]
                paired = False
    
        
    def selection(self):
        """ Do the population go trought a selection process
        - Take a part of the population by the score
        - Choose in the leftover randomly some chromosome
        """
        #Size of the population
        size_graded_retain = int(GRADED_RETAIN_PERCENT * self.size()) 

        #Extract the population sorted by score of each chromosome
        self.chromosomes = list(
            sorted(self.chromosomes, key=Chromosome.score)
        )
        #Take the size_skipped best
        self.parents = self.roulette_wheel_cumulative()
        self.chromosomes = self.chromosomes[-size_graded_retain:]

        #print(f"Best score : {bests_list[0].score} | Worse score : {leftover[-1].score}")
        return self.chromosomes[-1]
        
    def mutation(self):
        for parent0, parent1 in self.parents:        
            child0,child1 = parent0.crossover(parent1)
            while not self.add(child0): child0.mutation(MUTATION_PROBABILITY)
            while not self.add(child1): child1.mutation(MUTATION_PROBABILITY)
            if len(self.chromosomes) >= self.population_size:
                break


    def average_score(self):
        return sum(map(lambda x : x.score, self))/len(self.chromosomes)



    def number_of_collision(self):
        already_seen = [0]*len(self.chromosomes)
        nb_collision= 0
        for i,c0 in enumerate(self):
            if not already_seen[i]:
                for j,c1 in enumerate(self.chromosomes[i+1:]):
                    if c0 == c1:
                        nb_collision+= 1
                        already_seen[j] = True
                already_seen[i] = True
        return nb_collision


evolution_number = 200
population_size = 100
gene_size = 400


def main():

    number_point = int(input())
    lands = []
    for _ in range(number_points):
        lands.append(input_codingames()[:2])
    initial_state = input_codingames()[:7]
    env = EnvMarsLander(lands,initial_state)
    env.reset()
    population = Population.generator(population_size,gene_size)
    done = False
    while not done:
        for chromosome in population:
            if chromosome.use(env):
                chromosome.use(Codingames(initial_state))
                done = True

            env.reset()

        population.selection()
        
        population.mutation()



# %%
