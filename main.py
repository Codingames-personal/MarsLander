##
#%%

import random
import math

sign = lambda x : (x>0) - (x<0)
round_up = math.ceil
input_codingames = lambda : list(map(int,input().split()))

GRADED_RETAIN_PERCENT = 0.4     # percentage of retained best fitting individuals
NONGRADED_RETAIN_PERCENT = 0.01  # percentage of retained remaining individuals (randomly selected)
MUTATION_PROBABILITY = 0.05

class Action:
    @staticmethod
    def generator():
        return Action(
            random.randint(-15,15),
            (-1)**random.randint(0,1)
        )

    def __init__(self,rotate : int, power : int):
        self.rotate = rotate
        self.power = power

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def random_generate(self) -> None:
        """ Set up the action with random setings"""
        self.rotate = random.randint(-15,15)
        self.power = (-1)**random.randint(0,1)

##
#%% ------------------ENVIRONMENT------------------------------

class EnvironmentError(Exception):
    pass

class Point:
    def __init__(self, x : int, y : int):
        self.x = min(6999,max(0,x))
        self.y = min(2999,max(0,y))

    def __str__(self):
        return f"{self.x} {self.y}"
    def distance(self, other) -> float:
        return math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2 )

class Line:
    @staticmethod
    def ccw(A : Point, B : Point, C : Point):
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

    def __init__(self, point_a : Point, point_b : Point ):
        self.point_a = point_a
        self.point_b = point_b

    def __str__(self) -> str:
        return f"{self.point_a} | {self.point_b}"

    def collision(self,point_c,point_d):
        return Line.ccw(self.point_a,point_c,point_d) != Line.ccw(self.point_b, point_c, point_d) \
            and Line.ccw(self.point_a, self.point_b, point_c) != Line.ccw(self.point_a, self.point_b, point_d)
    
class Lander:

    def __str__(self):
        try:
            return f"{self.x} {self.y} {self.h_speed} {self.v_speed} {self.fuel} {self.rotate} {self.power}"
        except AttributeError :
            return "Lander not yiet initialized"
        
    def update(self,x ,y ,h_speed ,v_speed ,fuel ,rotate ,power):
        self.x = x
        self.y = y
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.fuel = fuel
        self.rotate = rotate
        self.power = power
        
class Surface:
    def __init__(self,lands=[]):
        self.lands = lands
        self.find_landing_site()

    def lines(self):
        """Generator of lines"""
        point_a = self.lands[0]
        for point_b in self.lands[1:]:
            yield Line(point_a,point_b)
            point_a = point_b
    
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
                return True
        return False

class EnvMarsLander:
    """ Environment of the Mars Lander puzzle of CodinGames"""
    GRAVITY = - 3.711 # gravity on Mars m.s-2

    def __init__(self,lands : list, initial_state : list):
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

    def reset(self):
        self.lander.update(*self.initial_state)

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
        return \
            (self.landing_on_site() and\
            self.landing_angle() and\
            self.landing_vertical_speed() and\
            self.landing_horizontal_speed())

    def get_score_action(self):
        score = 0

        WEIGHT_SPEED_VERTICAL = 100
        if self.landing_vertical_speed():
            vertical_speed_score = 1
        else:
            vertical_speed_score = 1 - abs(self.lander.v_speed)/WEIGHT_SPEED_VERTICAL
        score += vertical_speed_score

        WEIGHT_SPEED_HORIZONTAL = 50
        if self.landing_horizontal_speed():
            horizontal_speed_score = 1
        else:
            horizontal_speed_score = 1 - abs(self.lander.h_speed)/WEIGHT_SPEED_HORIZONTAL
            
        score += horizontal_speed_score
        return score

    def get_score_landing(self) -> float:
        """Calcul the score of the landing"""
        score = 0
        #WEIGHT_FUEL = 2000
        #score += self.lander.fuel / WEIGHT_FUEL
        """score += self.lander.rotate == 0
        score += self.landing_horizontal_speed()
        score += self.landing_vertical_speed()
        score += self.landing_on_site()"""
        
        WEIGHT_ROTATE = 90
        score += 1 - abs(self.lander.rotate)/WEIGHT_ROTATE
        
        WEIGHT_SPEED_VERTICAL = 500
        if self.landing_vertical_speed():
            vertical_speed_score = 2
        else:
            vertical_speed_score = 1 - abs(self.lander.v_speed)/WEIGHT_SPEED_VERTICAL
        score += vertical_speed_score

        WEIGHT_SPEED_HORIZONTAL = 500
        if self.landing_horizontal_speed():
            horizontal_speed_score = 2
        else:
            horizontal_speed_score = 1 - abs(self.lander.h_speed)/WEIGHT_SPEED_HORIZONTAL
            
        score += horizontal_speed_score
        
        WEIGHT_DISTANCE = 2000
        if self.landing_on_site():
            distance_score = 1
        elif not (0 <= self.lander.x < 7000):
            distance_score = 0
        else:
            distance_score = 1 - self.point_lander_now.distance(self.landing_site_point)/WEIGHT_DISTANCE
        score+=distance_score
    
        return score

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
            self.lander.power + action.rotate
        ))

        fuel = self.lander.fuel - power

        h_accel = - round_up(math.sin(rotate)*power)
        v_accel = round_up(EnvMarsLander.GRAVITY + math.cos(rotate)*power)

        h_speed = self.lander.h_speed + h_accel
        v_speed = self.lander.v_speed + v_accel

        x = self.lander.x + h_speed
        y = self.lander.y + v_speed

        self.update(x,y)

        done = (self.surface.collision(self.point_lander_before, self.point_lander_now)\
            or not 0 <= x < 7000 \
            or  not 0 <= y < 3000 \
            or fuel == 0)
        
        self.lander.update(x, y, h_speed, v_speed, fuel, rotate, power)

        return done
        
    def update(self,x,y):
        self.point_lander_now = Point(x, y)
        self.point_lander_before = Point(self.lander.x,self.lander.y)
        
class Codingames:
    def step(self,action):
        print(action)   
        obs = input().split()




class Gene:
    @staticmethod
    def generator():
        return Gene(Action.generator())

    def __init__(self, action : Action):
        self.action = action

    def __str__(self) -> str:
        return str(self.action)
        
    def mutation(self, epsilon):
        if random.random() < epsilon: 
            self.action.random_generate()


class Chromosome:
    
    @staticmethod
    def score(chromosome):
        return chromosome.score

    @staticmethod
    def generator(gene_size : int):
        genes = [Gene.generator() for _ in range(gene_size)]
        chromosome = Chromosome(genes)
        return chromosome
    

    def __init__(self, genes=[]):
        self.genes = genes
        self.score = 0

    def __str__(self) -> str:
        return "|".join(map(str,self.genes))

    def __iter__(self):
        return iter(self.genes)
    
    def __next__(self):
        return next(self)

    
    def add(self,gene : Gene):
        self.genes.append(gene)

    def size(self):
        return len(self.genes)

    def mutation(self,epsilon=1):
        for gene in self:
            gene.mutation(epsilon)
        
    def crossover(self,other):
        random_percent = random.random()
        child0,child1 = [], []
        for g0,g1 in zip(self,other):
            rotate0 = int(random_percent * g0.action.rotate + (1-random_percent) * g1.action.rotate)
            rotate1 = int(random_percent * g1.action.rotate + (1-random_percent) * g0.action.rotate)
            power0 =  int(random_percent * g0.action.power + (1-random_percent) * g1.action.power)
            power1 =  int(random_percent * g1.action.power + (1-random_percent) * g0.action.power)
            child0.append(Gene(Action(rotate0,power0)))
            child1.append(Gene(Action(rotate1,power1)))
        return Chromosome(child0), Chromosome(child1)
    
    def use(self,env):
        done = False
        for gene in self:
            if env.step(gene.action):
                done = True
                break
            #self.score += env.get_score_action()
        if not done:
            print("Not enough action")
            
        elif not env.successful_landing():
            self.score += env.get_score_landing()
            return False
        return True
            
class Population:
    @staticmethod
    def generator(population_size,gene_size):
        chromosomes = [Chromosome().generator(gene_size) for _ in range(population_size)]
        population = Population(chromosomes)
        population.population_size = population_size
        return population

    def __init__(self,chromosomes = []):
        self.chromosomes = chromosomes

    def __str__(self) -> str:
        return "\n".join(map(str,self.chromosomes))

    def __iter__(self):
        return iter(self.chromosomes)

    def __next__(self):
        return next(self)

    def sorted_score(self):
        return sorted(
            self.chromosomes,key=Chromosome.score,reverse=True
        )
    
    def add(self,chromosome : Chromosome):
        self.chromosomes.append(chromosome)

    def size(self):
        return len(self.chromosomes)

    def score_harmonize(self,chromosomes):
        total_score = sum(map(Chromosome.score,chromosomes))
        return list(map(
            lambda chromosome : chromosome.score/total_score,
            chromosomes
        ))

    def selection(self):
        """ Do the population go trought a selection process
        - Take a part of the population by the score
        - Choose in the leftover randomly some chromosome
        """
        #Size of the population
        size_graded_retain = int(GRADED_RETAIN_PERCENT * self.size()) 
        size_random_retain = int((1- GRADED_RETAIN_PERCENT)*NONGRADED_RETAIN_PERCENT * self.size())
        #size_new_chromosom = self.size() - size_graded_retain - size_random_retain
        #Extract the population sorted by score of each chromosome
        population_sorted = list(
            sorted(self.chromosomes,key=Chromosome.score,reverse=True)
        )
        
        #Take the size_skipped best
        bests_list = population_sorted[:size_graded_retain]

        #
        leftover = population_sorted[size_graded_retain:]
        rdm_list = random.sample(leftover,size_random_retain)
        
        # New random part of the population
        #fully_new = [Chromosome for _ in range(size_new_chromosom)]

        # Change the population
        self.chromosomes = bests_list

        #print(f"Best score : {bests_list[0].score} | Worse score : {leftover[-1].score}")
        return bests_list[0]
        

    def mutation(self):
        new_chromosomes = []
        while len(new_chromosomes) < self.population_size:
            parent0,parent1 = random.sample(self.chromosomes, 2)
            child0,child1 = parent0.crossover(parent1)
            child0.mutation(MUTATION_PROBABILITY)
            child1.mutation(MUTATION_PROBABILITY)
            new_chromosomes.append(child0)
            new_chromosomes.append(child1)
        self.chromosomes = new_chromosomes

    def average_score(self):
        return sum(map(lambda x : x.score, self))/len(self.chromosomes)


evolution_number = 10
population_size = 30
gene_size = 200



def main():

    number_point = int(input())
    lands = input_codingames()
    initial_state = input_codingames()
    env = EnvMarsLander(lands,initial_state)
    env.reset()
    population = Population.generator(population_size,gene_size)
    for _ in range(evolution_number):
        for chromosome in population:
            if chromosome.use(env):
                chromosome.use(Codingames())
                exit()
            env.reset()
        print(population.average_score())
        population.selection()
        
        population.mutation()

    


# %%
