import random
import numpy
from sources.chromosome import Chromosome
from sources.tools.point import Point

GRADED_RETAIN_PERCENT = 0.1    # percentage of retained best fitting individuals
NONGRADED_RETAIN_PERCENT = 0.2  # percentage of retained remaining individuals (randomly selected)
MUTATION_PROBABILITY = 0.01

class Population:

    fitness_power_max = 0
    fitness_rotate_max = 0
    fitness_power_min = 1e8
    fitness_rotate_min = 1e8
    evolution_number = 0
    final_chromosome = Chromosome()
    landing_site_found = False
    

    def __init__(self, population_size, chromosome_size, chromosome_type = Chromosome):
        self.chromosomes = [
            chromosome_type.generator(chromosome_size) for _ in range(population_size)
        ]
        self.new_chromosomes = []
        self.population_size = population_size
        self.chromosome_size = chromosome_size

        
    def __str__(self) -> str:
        return "\n".join(map(str, self.chromosomes))

    def __iter__(self):
        return iter(self.chromosomes)

    def __next__(self):
        return next(self)

    def sorted_score(self):
        return sorted(
            self.chromosomes, key=Chromosome.get_score, reverse=True
        )
    
    def add(self, chromosome : Chromosome):
        for current_chromosome in self:
            if chromosome is current_chromosome:
                return False
        self.chromosomes.append(chromosome)
        return True

    def size(self):
        return len(self.chromosomes)

    def check_landing_site(self):
        for chromosome in self:
            if chromosome.landing_on_site:
                self.landing_site_found = True
                return

    def avg_landing_point(self):
        x_avg, y_avg = 0, 0
        l=0
        for chromosome in self:
            if not chromosome.landing_point is None:
                l+=1
                x_avg += chromosome.landing_point.x
                y_avg += chromosome.landing_point.y
        return Point(round(x_avg/l), round(y_avg/l))
    
    def generate_score_diversity_avg(self):
        self.check_landing_site()
        if self.landing_site_found: return 
        avg_point = self.avg_landing_point()
        reference_distance = 0
        for chromosome in self:
            if not chromosome.landing_on_site:
                reference_distance = max(
                    reference_distance,
                    avg_point.distance(chromosome.landing_point)
                )


        for chromosome in self:
            if not chromosome.landing_on_site:
                dist_min = 10000
                if not chromosome.landing_point is None:
                    dist_min = min(
                        dist_min,
                        avg_point.distance(chromosome.landing_point)
                    )
                chromosome.score += 20 * dist_min / reference_distance 
            else:
                chromosome.score += 100

    def generate_score_diversity(self):
        reference_distance = 0 #Maximal distance between a landing point and the landing site
        
        for chromosome in self:
            if chromosome.landing_distance is None:
                reference_distance = max(reference_distance, chromosome.landing_distance)

        for i in range(len(self.chromosomes)):
            dist_min = 10000
            for j in range(len(self.chromosomes)):
                
                if not i == j:
                    dist_min = min(
                        dist_min,
                        self.chromosomes[i].landing_point.distance(self.chromosomes[j].landing_point)
                    )
            if chromosome.landing_on_site:
                score = 0
            else:
                score = round(100 * dist_min / reference_distance)
            chromosome.score += score

    def generate_score(self):
        self.generate_score_diversity_avg()


    def selection(self):
        """ Do the population go trought a selection process
        - Take a part of the population by the score
        - Choose in the leftover randomly some chromosome
        """

        #Extract the population sorted by score of each chromosome
        self.chromosomes = list(
            sorted(self.chromosomes, key=Chromosome.get_score)
        )
        #Take the size_skipped best
        best_chromosome = self.chromosomes[-1]

        size_graded_retain = int(GRADED_RETAIN_PERCENT * self.size()) 
        self.new_chromosomes = self.chromosomes[-size_graded_retain:] 

        return best_chromosome

    
    def cumulative_wheel(self, initial_index, final_index):
        total_score = sum(map(Chromosome.get_score, self.chromosomes))
        cumulative_scores = list()
        cumulative_score = 0
        for chromosome in self:
            cumulative_score += chromosome.score / total_score 
            cumulative_scores.append(cumulative_score)
            
        paired = False
        
        while initial_index < final_index:
                random_percent = min(0.999, random.random() + cumulative_scores[initial_index])
                i = initial_index
                while cumulative_scores[i] < random_percent : i+=1
                if not paired:
                    chromosome_parent0 = self.chromosomes[i]
                    paired = True
                else:
                    yield [chromosome_parent0, self.chromosomes[i]]
                    initial_index+=2
                    paired = False

    def mutation(self):
        final_index = int(self.population_size*(1 - GRADED_RETAIN_PERCENT))
        i0, i1 = 0, 1
        for parent0, parent1 in self.cumulative_wheel(0, final_index):               
            child0, child1 = parent0.crossover(parent1)
            child0.mutation(MUTATION_PROBABILITY)
            child1.mutation(MUTATION_PROBABILITY)
            self.chromosomes[i0] = child0
            self.chromosomes[i1] = child1 
            i0 +=1
            i1 +=1

    def population_switch(self):
        self.chromosomes = [
            c for c in self.new_chromosomes
        ]
        self.new_chromosomes = []

    def evolution(self):
        #self.generate_score()
        best_chromosome = self.selection()
        self.mutation()
        #self.population_switch()
        self.evolution_number += 1
        return best_chromosome

    def right_shift(self, offset : int):
        for chromosome in self:
            chromosome.starting_index +=offset

    def play(self, env):
        done = False
        while not done:
            for chromosome in self:
                env.reset()
                if chromosome.use(env):
                    return chromosome
            self.evolution()
            yield True
            



