import matplotlib.pyplot as plt
from turtle_mine import TurtleInterpreter
from collections import defaultdict

class FitnessEvaluator:
    def __init__(self, Path_Array, substitutions, combined_fitness, weight_a, weight_b, weight_c, weight_d, weight_e):
        """
        Initialize the FitnessEvaluator class.

        Args:
        - Path_Array: List of paths for substitutions
        - substitutions: List of substitution strings
        - combined_fitness: Dictionary containing combined fitness scores for substitutions
        - weight_a: Weight for Vertical fitness component
        - weight_b: Weight for bilateral symmetry fitness component
        - weight_c: Weight for Photon gathering ability fitness component
        - weight_d: Weight for structural stability fitness component
        - weight_e: Weight for proportion of branching points fitness component
        """
        self.Path_Array = Path_Array
        self.substitutions = substitutions
        self.combined_fitness = combined_fitness
        self.weight_a = weight_a
        self.weight_b = weight_b
        self.weight_c = weight_c
        self.weight_d = weight_d
        self.weight_e = weight_e

        # Initialize dictionaries to store fitness components
        self.Vertical_fit = {}
        self.symmetry_fit = {}
        self.Photon_gathering_fit = {}
        self.stability_fit = {}
        self.branching_fit = {}

    def FitnessFunction(self):
        """
        Calculate the fitness values for each substitution based on different fitness components.

        Returns:
        - fitness: List of lists containing phenotype and genotype fitness values for each substitution
        - Vertical_fitness_array: List of Vertical fitness values for each substitution
        - symmetry_fitness_array: List of bilateral symmetry fitness values for each substitution
        - Photon_gathering_fitness_array: List of Photon gathering ability fitness values for each substitution
        - stability_fitness_array: List of structural stability fitness values for each substitution
        - branching_fitness_array: List of proportion of branching points fitness values for each substitution
        """
        # Calculate fitness components
        self.PositiveVertical()
        self.BilateralSymmetry()
        self.PhotonGatheringAbility()
        self.StructuralStability()
        self.ProportionOfBranchingPoints()

        # Initialize lists to store fitness values for each component
        fitness = []
        Vertical_fitness_array = []
        symmetry_fitness_array = []
        Photon_gathering_fitness_array = []
        stability_fitness_array = []
        branching_fitness_array = []

        # Calculate overall fitness for each substitution and collect fitness values for each component
        for i in self.substitutions:
            weighted_fitness = sum([
                self.weight_a * self.Vertical_fit[i],
                self.weight_b * self.symmetry_fit[i],
                self.weight_c * self.Photon_gathering_fit[i],
                self.weight_d * self.stability_fit[i],
                self.weight_e * self.branching_fit[i]
            ])

            # Calculate Phenotype and Genotype values
            Phenotype = weighted_fitness / (self.weight_a + self.weight_b + self.weight_c + self.weight_d + self.weight_e)
            Genotype = self.combined_fitness[i]
            fitness.append([Phenotype, Genotype])

            # Append to fitness lists for each component
            Vertical_fitness_array.append(self.Vertical_fit[i])
            symmetry_fitness_array.append(self.symmetry_fit[i])
            Photon_gathering_fitness_array.append(self.Photon_gathering_fit[i])
            stability_fitness_array.append(self.stability_fit[i])
            branching_fitness_array.append(self.branching_fit[i])

        return fitness, Vertical_fitness_array, symmetry_fitness_array, Photon_gathering_fitness_array, stability_fitness_array, branching_fitness_array

    def calculate_unique_index(self, sorted_items):
        """
        Calculate a dictionary containing unique score values and their corresponding substitutions.

        Args:
        - sorted_items: List of tuples containing substitutions and their scores, sorted by score

        Returns:
        - unique_index: Dictionary containing unique score values and their corresponding substitutions
        """
        unique_index = defaultdict(list)
        for key, val in sorted_items:
            unique_index.setdefault(val, []).append(key)
        return unique_index

    def calculate_fit(self, sorted_scores, fitness_type):
        """
        Calculate fitness values based on sorted scores and fitness type.

        Args:
        - sorted_scores: Dictionary containing substitutions and their scores, sorted by score
        - fitness_type: Type of fitness being calculated

        Returns:
        - test_fit: Dictionary containing substitutions and their fitness values based on the fitness type
        """
        if fitness_type == 'stability':
            unique_scores = sorted(set(sorted_scores.values()), reverse=True)
        else:
            unique_scores = sorted(set(sorted_scores.values()))
        unique_index = self.calculate_unique_index(sorted_scores.items())
        rewards = TurtleInterpreter.calculate_rewards(self, len(unique_index))
        value_map = {val: rewards[i] for i, val in enumerate(unique_scores)}
        test_fit = {k: value_map.get(v, v) for k, v in sorted_scores.items()}
        return test_fit

    def BilateralSymmetry(self):
        """
        Calculate fitness scores based on bilateral symmetry for each substitution.

        Returns:
        - symmetry_fit: Dictionary containing substitutions and their fitness scores based on bilateral symmetry
        """
        symmetry_scores = {}
        for path, substitution in zip(self.Path_Array, self.substitutions):
            left_side_sum = sum(abs(x[0]) for x in path if x[0] < 0)
            right_side_sum = sum(abs(x[0]) for x in path if x[0] > 0)
            ratio = left_side_sum / right_side_sum if right_side_sum != 0 else 0.0
            symmetry_scores[substitution] = ratio

        symmetry_scores_sorted = dict(sorted(symmetry_scores.items(), key=lambda x: x[1], reverse=False))
        self.symmetry_fit = self.calculate_fit(symmetry_scores_sorted, 'symmetry')
        return self.symmetry_fit

    def PositiveVertical(self):
        """
        Calculate fitness scores based on positive Vertical for each substitution.

        Returns:
        - Vertical_fit: Dictionary containing substitutions and their fitness scores based on positive Vertical
        """
        max_coords = {sub: max(path, key=lambda x: x[1])[1] for sub, path in zip(self.substitutions, self.Path_Array)}
        max_coords_sorted = dict(sorted(max_coords.items(), key=lambda x: x[1], reverse=False))
        self.Vertical_fit = self.calculate_fit(max_coords_sorted, 'Vertical')
        return self.Vertical_fit

    def StructuralStability(self):
        """
        Calculate fitness scores based on structural stability for each substitution.

        Returns:
        - stability_fit: Dictionary containing substitutions and their fitness scores based on structural stability
        """
        stability_scores = {}
        for path, sub in zip(self.Path_Array, self.substitutions):
            point_scores = {}
            for point_idx in range(len(path) - 1):
                current_point, next_point = path[point_idx], path[point_idx + 1]
                if current_point not in point_scores:
                    point_scores[current_point] = 0
                if next_point not in point_scores and current_point[2] != next_point[2]:
                    point_scores[current_point] += 1
                else:
                    point_scores[current_point] += 0
            if not point_scores:
                stability_scores[sub] = 0
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                continue
            else:
                max_score = max(point_scores.values())
                count_max_score = sum(1 for score in point_scores.values() if score == max_score)
                stability_scores[sub] = count_max_score * max_score

        stability_scores_sorted = dict(sorted(stability_scores.items(), key=lambda x: x[1], reverse=True))
        self.stability_fit = self.calculate_fit(stability_scores_sorted, 'stability')
        return self.stability_fit

    def ProportionOfBranchingPoints(self):
        """
        Calculate fitness scores based on proportion of branching points for each substitution.

        Returns:
        - branching_fit: Dictionary containing substitutions and their fitness scores based on proportion of branching points
        """
        proportion = {}
        for path, sub in zip(self.Path_Array, self.substitutions):
            point_scores = {}
            for point_idx in range(len(path) - 1):
                current_point, next_point = path[point_idx], path[point_idx + 1]
                if current_point not in point_scores:
                    point_scores[current_point] = 0
                if next_point not in point_scores and current_point[2] != next_point[2]:
                    point_scores[current_point] += 1
            num_branching_points = sum(1 for count in point_scores.values() if count >= 1)
            proportion[sub] = num_branching_points

        proportion_scores_sorted = dict(sorted(proportion.items(), key=lambda x: x[1], reverse=False))
        self.branching_fit = self.calculate_fit(proportion_scores_sorted, 'branching')
        return self.branching_fit

    def PhotonGatheringAbility(self):
        """
        Calculate fitness scores based on Photon gathering ability for each substitution.

        Returns:
        - Photon_gathering_fit: Dictionary containing substitutions and their fitness scores based on Photon gathering ability
        """
        max_coords = {sub: max(path, key=lambda x: abs(x[0]))[1] for sub, path in zip(self.substitutions, self.Path_Array)}
        max_coords_sorted = dict(sorted(max_coords.items(), key=lambda x: x[0], reverse=False))
        self.Photon_gathering_fit = self.calculate_fit(max_coords_sorted, 'Photon_gathering')
        return self.Photon_gathering_fit
