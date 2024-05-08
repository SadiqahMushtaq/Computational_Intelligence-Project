import random
from rule_Generator import generateRule

MAX_CHROMOSOME_LENGTH = 30
MIN_CHROMOSOME_LENGTH = 8

class L_System:

    def __init__(self, population_size, seed):
        self.population_size = population_size
        # self.seed = seed

        if seed == False:
                self.seed_population = []
                self.generate_seed_population()
        else:
            self.population = seed
            self.generate_seed_population()


    def generate_seed_population(self):
        self.seed_population = []
        for _ in range(self.population_size):
            chromosome = generateRule(MIN_CHROMOSOME_LENGTH, MAX_CHROMOSOME_LENGTH)
            self.seed_population.append(chromosome)
        return self.seed_population



    # def generate_random_chromosome(self, length):
    #     return ''.join(random.choice(['F', '+', '-']) for _ in range(length))

        
# # Example usage:
# MAX_CHROMOSOME_LENGTH = 30
# MIN_CHROMOSOME_LENGTH = 8
# population_size = 10
# num_of_generations = 100
# mutation_rate = 0.1
# num_of_offsprings = 2
# seed = None  # You can provide a specific seed here if needed

# l_system = L_System(population_size, seed)
# seed_population = l_system.generate_seed_population()
# print("Seed population:")
# for chromosome in seed_population:
#     print(chromosome)