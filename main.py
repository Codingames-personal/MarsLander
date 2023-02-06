##
#%%
import numpy
import random

sign = lambda x : (x>0) - (x<0)


class Action:
    def __init__(self,rotate : int, power : int):
        self.rotate = sign(rotate)*max(15,abs(rotate))
        self.power = sign(power)

    def __str__(self):
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

    def distance(self, other) -> float:
        return numpy.sqrt((other.x - self.x)**2 + (other.y - self.y)**2 )

class Line:
    def __init__(self, point_a : Point, point_b : Point ):
        self.point_a = point_a
        self.point_b = point_b

    def collision(self,point_a,point_b) -> bool:
        return not(point_b.x <= self.point_a.x and \
            point_b.x <= self.point_b.x or \
            point_a.x >= self.point_a.x and \
            point_a.x >= self.point_b.x) and\
            not(point_b.y <= self.point_a.y and \
            point_b.y <= self.point_b.y or \
            point_a.y >= self.point_a.y and \
            point_a.y >= self.point_b.y)

class Lander:
    def update(self,x ,y ,h_speed ,v_speed ,fuel ,rotate ,power):
        self.x_before = self.x
        self.y_before = self.y
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
                break
        raise EnvironmentError()

    def collistion(self,point_a,point_b) -> bool:
        """Find out if there was a collision when the lander went from point_a to point_b"""
        for line in self.lines:
            if line.collision(point_a,point_b):
                return True
        return False

class EnvMarsLander:
    """ Environment of the Mars Lander puzzle of CodinGames"""
    GRAVITY = - 3,711 # gravity on Mars m.s-2

    def __init__(self):
        self.lander = Lander()

    def surface_initialisation(self,number_points : int) -> None:
        lands = []
        for _ in range(number_points):
            obs = list(map(int,input().split()))
            point = Point(obs[0],obs[1])
            lands.append(point)
        self.surface = Surface(lands)
        self.landing_site_point = Point(
            self.surface.landing_site.point_b.x - self.surface.landing_site.point_b.x,
            self.surface.landing_site.point_b.y - self.surface.landing_site.point_b.y
        )

    def landing_on_site(self) -> bool:
        return self.surface.landing_site.collision(
            self.point_lander_before,
            self.point_lander_now   
        )

    def landing_angle(self) -> bool:
        return self.lander.rotate == 0

    def landing_vertical_speed(self) -> bool:
        return self.lander.v_speed <= 40

    def landing_horizontal_speed(self) -> bool:
        return self.lander.h_speed <= 20

    def successful_landing(self) -> bool:
        """For a landing to be successful, the ship must:
            - land on flat ground
            - land in a vertical position (tilt angle = 0°)
            - vertical speed must be limited ( ≤ 40m/s in absolute value)
            - horizontal speed must be limited ( ≤ 20m/s in absolute value)
        """
        return \
            self.landing_on_site() and\
            self.landing_angle() and\
            self.landing_vertical_speed() and\
            self.landing_horizontal_speed()

    def get_score(self):
        score = 0
        WEIGHT_FUEL = 10
        score += (self.lander.fuel if self.lander.fuel >0 else -1)*WEIGHT_FUEL
        
        WEIGHT_ROTATE = 10
        score += -self.lander.rotate * WEIGHT_ROTATE

        WEIGHT_VERTICAL_SPEED = 10
        if self.landing_vertical_speed():
            vertical_speed_score = WEIGHT_VERTICAL_SPEED
        else:
            vertical_speed_score = - self.lander.v_speed*WEIGHT_VERTICAL_SPEED
        score += vertical_speed_score

        WEIGHT_HORIZONTAL_SPEED = 10
        if self.landing_horizontal_speed():
            horizontal_speed_score = WEIGHT_HORIZONTAL_SPEED
        else:
            horizontal_speed_score = - self.lander.h_speed*WEIGHT_HORIZONTAL_SPEED
        score += horizontal_speed_score
        
        WEIGHT_DISTANCE = 10
        if self.landing_on_site():
            score += WEIGHT_DISTANCE
        else:
            score -= self.point_lander_now.distance(self.landing_site_point)*WEIGHT_DISTANCE
        
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
        
        rotate_variation = self.lander.rotate + action.rotate
        rotate = sign(rotate_variation)*min(90,abs(rotate_variation)) 

        power = max(0, min(
            4,
            action.power + self.lander.power
        ))

        fuel = self.lander.fuel - power

        h_accel = - numpy.sin(rotate)*power
        v_accel = EnvMarsLander.GRAVITY + numpy.cos(rotate)*power

        h_speed = self.lander.h_speed + h_accel
        v_speed = self.lander.v_speed + v_accel

        x = self.lander.x + h_speed
        y = self.lander.y + v_speed

        self.update(x,y)

        done = (self.surface.collision(self.point_lander_before, self.point_lander_now)\
            and not 0 <= x < 7000 \
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


GRADED_RETAIN_PERCENT = 0.3     # percentage of retained best fitting individuals
NONGRADED_RETAIN_PERCENT = 0.2  # percentage of retained remaining individuals (randomly selected)

class Gene:
    @staticmethod
    def generator():
        gene = Gene()
        gene.mutation()
        return gene

    def __init__(self, action : Action):
        self.action = action
        
    def mutation(self, epsilon=1):
        if random.random() < epsilon: 
            self.action = random.randint(0,3)


class Chromosome:
    
    @staticmethod
    def score(chromosome):
        return chromosome.score

    @staticmethod
    def generator(gene_size):
        genes = [Gene.generator() for _ in range(gene_size)]
        chromosome = Chromosome(genes)
        chromosome.score = 0
        return chromosome

    def __init__(self, genes=[]):
        self.genes = genes

    def __iter__(self):
        return iter(self.genes)
    
    def __next__(self):
        return next(self)

    def size(self):
        return len(self.genes)

    def mutation(self,epsilon=1):
        i = random.randint(0,self.size()-1)
        self.genes[i].mutation(epsilon)

    def crossover(self,other):
        i = random.randint(0,self.size()-1)    
        genes = self.genes[:i] + other.genes[i:]
        return Chromosome(genes)
    
    def use(self,env):
        done = False
        while not done:
            for gene in self:
                if not env.step(gene.action):
                    break
        if not env.successful_landing():
            self.score = env.get_score()
            return False
        return True
            
class Population:
    @staticmethod
    def generator(population_size,gene_size):
        chromosomes = [Chromosome().generator(gene_size) for _ in range(population_size)]
        return Population(chromosomes)

    def __init__(self,chromosomes = []):
        self.chromosomes = chromosomes

    def __iter__(self):
        return iter(self.chromosomes)

    def __next__(self):
        return next(self)

    
    def add(self,chromosome : Chromosome):
        self.chromosomes.append(chromosome)

    def size(self):
        return len(self.chromosomes)


    def selection(self):
        SIZE_SKIPPED = int( (1-GRADED_RETAIN_PERCENT)*self.size() )
        SIZE_RANDOM = int(NONGRADED_RETAIN_PERCENT*SIZE_SKIPPED)
        population_sorted = list(sorted(self.chromosomes,key=Chromosome.score))
        bests_list = population_sorted[SIZE_SKIPPED:] 
        leftover = population_sorted[:SIZE_SKIPPED]
        random.shuffle(leftover)
        rdm_list = [chromosome for _,chromosome in zip(range(SIZE_RANDOM), leftover)]
        self = Population(bests_list + rdm_list)


    def mutation(self):
        population = Population([])
        while population.size()<self.size():
            chrom1,chrom2 = random.sample(self.chromosomes,2)
            new_chrom = chrom1.crossover(chrom2)
            new_chrom.mutation()
            population.add(new_chrom)
        self = population

    def average_score(self):
        return sum(map(lambda x : x.score, self))/len(self.chromosomes)


evolution_number = 10
population_size = 30
gene_size = 200



def main():
    env = EnvMarsLander()
    number_point = int(input())
    env.surface_initialisation(number_point)
    population = Population.generator(population_size,gene_size)
    for _ in range(evolution_number):
        for chromosome in population:
            if chromosome.use(env):
                final_chromosome = chromosome
                chromosome.use(Codingames())
                exit()
        print(population.average_score())
        population.selection()
        population.mutation()

    


# %%
