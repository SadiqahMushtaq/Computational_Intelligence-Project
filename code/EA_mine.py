# EA_mine.py
from turtle_mine import TurtleInterpreter
from lsystem_mine import L_System
from operator import itemgetter
from fitness_mine import *
from rule_Generator import *
from visualizer_mine import *
import random
import matplotlib.pyplot as plt
import numpy as np 

class Evolution:

    def __init__(self, population_size, generations, mutation_rate, offspring_count, substitute_order, seed, weight_a, weight_b, weight_c, weight_d, weight_e, PatternType):
        # Initialize class attributes
        self.PatternType = PatternType
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.offspring_count = offspring_count
        self.substitute_order = substitute_order

        # Set fitness weights
        self.weight_a = weight_a
        self.weight_b = weight_b
        self.weight_c = weight_c
        self.weight_d = weight_d
        self.weight_e = weight_e

        # Generate initial population
        initial_pop = L_System(population_size, seed)
        self.population = initial_pop.seed_population

        # Perform substitution on initial population
        self.Substitutions, self.combined_fitness = self.Substitute(self.population)

        # Generate turtle interpretation
        if PatternType == 'Tree':
            self.angle = 30
        elif PatternType == 'Serpinski':
            self.angle = 120
        elif PatternType == 'Dragon':
            self.angle = 90
        interpreter = TurtleInterpreter(self.Substitutions, self.angle)
        interpreter.interpret_string()
        self.Path_Array = interpreter.Path_Array

        # Calculate fitness
        fitness_calc = FitnessEvaluator(self.Path_Array, self.Substitutions, self.combined_fitness, weight_a, weight_b, weight_c, weight_d, weight_e)
        self.fitness, self.Vertical_fitness_array, self.symmetry_fitness_array, self.Photon_fitness_array, self.stability_fitness_array, self.branching_fitness_array = fitness_calc.FitnessFunction()


    def Substitute(self, population):
        substitutedList = []
        dict = {}
        for i in population:
            bigchromosome = Substitution_init(i, self.substitute_order)
            substitutedList.append(bigchromosome)
            dict[bigchromosome] = i
        return (substitutedList, dict)

    def ExtractPop(self, survival_fit):
        updated_Pop = []
        for i in survival_fit:
            updated_Pop.append(i[1])
        return updated_Pop


    # PARENT SELECTION -------------------------------------------------------------------------------------------------------

    def Parent_truncation_selection(self, fit_population):
        selected_parents_1 = []
        selected_parents_2 = []

        fitness_values = [individual[0] for individual in fit_population]
        sorted_population = sorted(fit_population, key=lambda x: x[0], reverse=True)

        if len(sorted_population) == 0:
            return ([], [])

        # Select parents based on the top 10% of the population
        selection_size = max(1, int(len(sorted_population) * 0.1))  # Ensure at least one parent is selected
        selected_parents = sorted_population[:selection_size]

        # Randomly pair selected parents
        random.shuffle(selected_parents)
        for i in range(0, len(selected_parents), 2):
            selected_parents_1.append(selected_parents[i][1])
            selected_parents_2.append(selected_parents[i+1][1])

        return (selected_parents_1, selected_parents_2)


    # RANDOM SELECTION -----------------------------------------------------------------------------------------------

    def Parent_randomSelection(self, fitpopulation):
        print("Fit Population before selection:", fitpopulation)

        parentonelist = []
        parenttwolist = []

        loopsize = int(self.offspring_count / 2)

        for _ in range(loopsize):
            # Perform random selection for the first parent
            parent1 = random.choice(fitpopulation)
            parentonelist.append(parent1[1])

            # Perform random selection for the second parent
            parent2 = random.choice(fitpopulation)
            parenttwolist.append(parent2[1])

        return (parentonelist, parenttwolist)

    # RANK BASED SELECTION --------------------------------------------------------------------------------------------

    def Parent_rankBasedSelection(self, fitpopulation):
        print("Fit Population before selection:", fitpopulation)

        parentonelist = []
        parenttwolist = []

        loopsize = int(self.offspring_count/ 2)

        # Calculate cumulative probabilities based on ranks
        total_ranks = sum(range(1, len(fitpopulation) + 1))
        probabilities = [rank / total_ranks for rank in range(1, len(fitpopulation) + 1)]

        for _ in range(loopsize):
            # Perform rank-based selection for the first parent
            index1 = random.choices(range(len(fitpopulation)), weights=probabilities)[0]
            parentonelist.append(fitpopulation[index1][1])

            # Perform rank-based selection for the second parent
            index2 = random.choices(range(len(fitpopulation)), weights=probabilities)[0]
            parenttwolist.append(fitpopulation[index2][1])

        return (parentonelist, parenttwolist)

    # FITNESS PROPORTION-------------------------------------------------------------------------------------

    def Parent_fitness_proportion(self, fit_population):
        selected_parents_1 = []
        selected_parents_2 = []

        fitness_values = [individual[0] for individual in fit_population]
        total_fitness = sum(fitness_values)

        if total_fitness == 0:
            return ([], [])

        normalized_fitness = [fitness / total_fitness for fitness in fitness_values]
        cumulative_probabilities = [sum(normalized_fitness[:i+1]) for i in range(len(normalized_fitness))]

        offspring_count = int(self.offspring_count / 2)
        for _ in range(offspring_count):
            rand_num1 = random.random()
            rand_num2 = random.random()

            parent_index_1 = next(i for i, prob in enumerate(cumulative_probabilities) if prob >= rand_num1)
            selected_parents_1.append(fit_population[parent_index_1][1])

            parent_index_2 = next(i for i, prob in enumerate(cumulative_probabilities) if prob >= rand_num2)
            selected_parents_2.append(fit_population[parent_index_2][1])

        return (selected_parents_1, selected_parents_2)

    # TOURNAMENT SELECTION ----------------------------------------------------------------------------------------

    def Parent_tournamentSelection(self, fitpopulation):

        parentonelist = []
        parenttwolist = []

        loopsize = int(self.offspring_count/ 2)

        for _ in range(loopsize):
            # Perform tournament selection for the first parent
            tournament_size = min(3, len(fitpopulation))
            tournament1 = random.sample(fitpopulation, tournament_size)
            winner1 = max(tournament1, key=lambda x: x[0])
            parentonelist.append(winner1[1])

            # Perform tournament selection for the second parent
            tournament2 = random.sample(fitpopulation, tournament_size)
            winner2 = max(tournament2, key=lambda x: x[0])
            parenttwolist.append(winner2[1])

        print(" ")

        return (parentonelist, parenttwolist)

    # SURVIVOR SELECTION -------------------------------------------------------------------------------------------

    def Survivor_binarytournament(self, fitness, Vertical, symmetry, Photon, stability, proportion):
        survivors = []
        survivors2 = []
        while len(survivors) != self.population_size:
            a, b = random.sample(range(0, (self.population_size-1)), 2)
            parent_list = [fitness[a][0], fitness[a][1], Vertical[a], symmetry[a], Photon[a], stability[a], proportion[a]] if fitness[a][0] >= fitness[b][0] else [fitness[b][0], fitness[b][1], Vertical[b], symmetry[b], Photon[b], stability[b], proportion[b]]
            survivors2.append(parent_list)
            parent_one_list = parent_list[:2]
            survivors.append(parent_one_list)

        # Sort the survivors based on fitness
        return sorted(survivors, key=itemgetter(0), reverse=True), sorted(survivors2, key=itemgetter(0), reverse=True)


    def Survivor_truncation(self, fitness, Vertical, symmetry, Photon, stability, proportion):
        # print("Length of fitness:" , len(fitness))
        # Calculate the number of individuals to keep based on the truncation rate
        num_to_keep = self.population_size
        # print("Num to keep:", num_to_keep)

        # Combine fitness values with other attributes into one list
        combined_fitness = [(fitness[i][0], fitness[i][1], Vertical[i], symmetry[i], Photon[i], stability[i], proportion[i]) for i in range(len(fitness))]

        # Sort the combined list based on fitness
        sorted_combined_fitness = sorted(combined_fitness, key=itemgetter(0), reverse=True)

        # Select the top individuals up to the calculated number to keep
        survivors = sorted_combined_fitness[:num_to_keep]

        # Extract only the chromosome and fitness values for the output
        survivors_chromosome_fitness = [(individual[0], individual[1]) for individual in survivors]

        return survivors_chromosome_fitness, survivors

    def Survivor_fitness_proportional(self, fitness, Vertical, symmetry, Photon, stability, proportion):
        # Combine fitness values with other attributes into one list
        combined_fitness = [(fitness[i][0], fitness[i][1], Vertical[i], symmetry[i], Photon[i], stability[i], proportion[i]) for i in range(len(fitness))]

        # Calculate total fitness
        total_fitness = sum(individual[0] for individual in combined_fitness)

        # Calculate selection probabilities for each individual
        selection_probabilities = [(individual[0] / total_fitness) for individual in combined_fitness]

        # Select individuals based on their selection probabilities
        num_to_keep = self.population_size
        selected_indices = np.random.choice(range(len(combined_fitness)), size=num_to_keep, p=selection_probabilities, replace=False)
        survivors = [combined_fitness[idx] for idx in selected_indices]

        # Extract only the chromosome and fitness values for the output
        survivors_chromosome_fitness = [(individual[0], individual[1]) for individual in survivors]

        return survivors_chromosome_fitness, survivors
    
    def Survivor_rank_based(self, fitness, Vertical, symmetry, Photon, stability, proportion):
        # Create a list of tuples containing indices and fitness values
        fitness_with_indices = [(idx, fit) for idx, fit in enumerate(fitness)]

        # Sort the list of tuples based on fitness values
        sorted_fitness = sorted(fitness_with_indices, key=itemgetter(1), reverse=True)

        # Assign ranks to individuals based on their position in the sorted list
        ranks = {idx: rank for rank, (idx, _) in enumerate(sorted_fitness, start=1)}

        survivors = []
        survivors2 = []

        while len(survivors) != self.population_size:
            # Select two random indices
            a, b = random.sample(range(self.population_size), 2)

            # Get the ranks of the selected individuals
            rank_a = ranks[a]
            rank_b = ranks[b]

            # Select the individual with the higher rank
            if rank_a <= rank_b:
                idx = a
            else:
                idx = b

            # Append the selected individual to the survivors list
            survivor_list = [fitness[idx][0], fitness[idx][1], Vertical[idx], symmetry[idx], Photon[idx], stability[idx], proportion[idx]]
            survivors2.append(survivor_list)
            parent_one_list = survivor_list[:2]
            survivors.append(parent_one_list)

        return sorted(survivors, key=itemgetter(0), reverse=True), sorted(survivors2, key=itemgetter(0), reverse=True)




    # CROSSOVER --------------------------------------------------------------------------------------------------

    def perform_crossover(self, parent1, parent2):
        offspring_list = []
        while len(offspring_list) < 2:
            parent1_index, parent1_end_index = sorted(random.sample(range(len(parent1)), 2))
            parent2_index, parent2_end_index = sorted(random.sample(range(len(parent2)), 2))

            offspring1 = list(parent1)
            offspring2 = list(parent2)
            offspring1[parent1_index:parent1_end_index], offspring2[parent2_index:parent2_end_index] = offspring2[parent2_index:parent2_end_index], offspring1[parent1_index:parent1_end_index]

            if validChromosome(offspring1) and len(offspring_list) < 2:
                offspring_list.append("".join(offspring1))
            if validChromosome(offspring2) and len(offspring_list) < 2:
                offspring_list.append("".join(offspring2))
        return offspring_list

    def crossover(self, parents1_list, parents2_list):
        children = []
        for parent1, parent2 in zip(parents1_list, parents2_list):
            children.extend(self.perform_crossover(parent1, parent2))
        return children



    # MUTATION ----------------------------------------------------------------------------------------------------

    def Block_Mutation(self, children):
        for idx in range(len(children)):
            mutation_chance = random.random()
            if mutation_chance < self.mutation_rate:
                start_idx = random.randint(0, len(children[idx])-1)
                end_idx = random.randint(start_idx, len(children[idx])-1)
                selected_substring = children[idx][start_idx:end_idx+1]

                # Retry if the selected substring is not a valid chromosome
                while not validChromosome(selected_substring):
                    start_idx = random.randint(0, len(children[idx])-1)
                    end_idx = random.randint(start_idx, len(children[idx])-1)
                    selected_substring = children[idx][start_idx:end_idx+1]

                # Generate a substitution rule between 2 to 3 characters
                substitution_rule = generateRule(2, 3)

                # Avoid single-character substitutions being '[' or ']'
                while substitution_rule == '[' or substitution_rule == ']':
                    substitution_rule = generateRule(2, 3)

                # Apply mutation
                children[idx] = children[idx][:start_idx] + substitution_rule + children[idx][end_idx+1:]
        return children

    def Symbol_Mutation(self, children):
        index = 0
        for child in children:
            random_index = random.randint(0, len(child) - 1)
            symbol = child[random_index]

            while symbol in ("[", "]"):
                random_index = random.randint(0, len(child) - 1)
                symbol = child[random_index]

            substitution = generateRule(1, 2)
            if len(substitution) == 1:
                while substitution in ("[", "]"):
                    substitution = generateRule(1, 2)
            substitution = str(substitution)

            initial = child[:random_index]
            later = child[random_index + 1:]
            child = initial + substitution + later

            children[index] = child
            index += 1
        return children



    #  EVOLUTION ----------------------------------------------------------------------------------------------

    def run_evolution(self):
        generation_indices = []
        average_fitness_history = []
        average_Vertical_fitness_history = []
        average_symmetry_fitness_history = []
        average_Photon_fitness_history = []
        average_stability_fitness_history = []
        average_branching_fitness_history = []

        
        for gen_num in range(self.generations):
            generation_indices.append(gen_num)
            print("Gen", gen_num)
            
            # Parent selection
            parent1, parent2 = self.Parent_fitness_proportion(self.fitness)
            
            # Crossover
            children = self.crossover(parent1, parent2)
            
            # Mutation
            mutated_children = self.Block_Mutation(children)
            
            # Generating new population
            new_population = self.population + mutated_children
            
            # Substitution
            substitutions, combined_fitness = self.Substitute(new_population)
            
            # Calculating fitness of new population
            new_interpretation = TurtleInterpreter(substitutions, self.angle)
            new_interpretation.interpret_string()
            new_Path_Array = new_interpretation.Path_Array
            new_fitness = FitnessEvaluator(new_Path_Array, substitutions, combined_fitness, 
                                self.weight_a, self.weight_b, self.weight_c, self.weight_d, self.weight_e)
            survival_fitness, survival_Vertical, survival_symmetry, survival_Photon, survival_stability, survival_proportion = new_fitness.FitnessFunction()

            
            # Survivor selection
            self.fitness, fitness_all = self.Survivor_rank_based(survival_fitness, survival_Vertical, survival_symmetry, survival_Photon, survival_stability, survival_proportion)
            self.population = self.ExtractPop(self.fitness)
            
            # Calculating average fitness for this generation
            total_fitness = sum(avg[0] for avg in self.fitness)
            average_fitness = total_fitness / self.population_size
            print("Average Fitness:", average_fitness)
            average_fitness_history.append(average_fitness)

            # Calculating average fitness for each type
            total_Vertical_fitness = sum(avg[2]*self.weight_a for avg in fitness_all)
            average_Vertical_fitness = total_Vertical_fitness / self.population_size
            average_Vertical_fitness_history.append(average_Vertical_fitness)
            print("Average Vertical Fitness:", average_Vertical_fitness)

            total_symmetry_fitness = sum(avg[3]*self.weight_b for avg in fitness_all)
            average_symmetry_fitness = total_symmetry_fitness / self.population_size
            average_symmetry_fitness_history.append(average_symmetry_fitness)
            print("Average Symmetry Fitness:", average_symmetry_fitness)

            total_Photon_fitness = sum(avg[4]*self.weight_c for avg in fitness_all)
            average_Photon_fitness = total_Photon_fitness / self.population_size
            average_Photon_fitness_history.append(average_Photon_fitness)
            print("Average Photon Fitness:", average_Photon_fitness)

            total_stability_fitness = sum(avg[5]*self.weight_d for avg in fitness_all)
            average_stability_fitness = total_stability_fitness / self.population_size
            print("Average Stability Fitness:", average_stability_fitness)
            average_stability_fitness_history.append(average_stability_fitness)

            total_branching_fitness = sum(avg[6]*self.weight_e for avg in fitness_all)
            average_branching_fitness = total_branching_fitness / self.population_size
            average_branching_fitness_history.append(average_branching_fitness)
            print("Average Branching Fitness:", average_branching_fitness)

            # Plotting
            
            print("")

        # Plotting average fitness history against generations
        plt.figure(figsize=(10, 5))
        plt.plot(generation_indices, average_fitness_history)
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Avg Fitness History - Parent: Proportionate, Survivor: Truncation, Mutation rate: 0.3')
        plt.show()
        

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(generation_indices, average_Vertical_fitness_history, label='Vertical')
        plt.plot(generation_indices, average_symmetry_fitness_history, label='Symmetry')
        plt.plot(generation_indices, average_Photon_fitness_history, label='Photon')
        plt.plot(generation_indices, average_stability_fitness_history, label='Stability')
        plt.plot(generation_indices, average_branching_fitness_history, label='Branching')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Average Fitness of Each Type Over Generations')
        plt.legend()
        plt.grid(True)
        plt.show()

        return self.fitness
    













    # ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<