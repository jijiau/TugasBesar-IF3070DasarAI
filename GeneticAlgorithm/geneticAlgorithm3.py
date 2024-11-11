import numpy as np
import random

def initial_population(fitness, total_fitness):
    return fitness / total_fitness

#fitness
def fitness(cube, magic_number=315):
    CUBE_SIZE = 5
    total_difference = 0

    for i in range(CUBE_SIZE):
        for j in range(CUBE_SIZE):
            row_sum = np.sum(cube[i, j, :]) 
            col_sum = np.sum(cube[i, :, j])     
            pillar_sum = np.sum(cube[:, i, j]) 
            
            total_difference += (row_sum - magic_number) ** 2
            total_difference += (col_sum - magic_number) ** 2
            total_difference += (pillar_sum - magic_number) ** 2

    for i in range(CUBE_SIZE):
        diag_xy_sum = np.sum([cube[i, j, j] for j in range(CUBE_SIZE)])  
        diag_yz_sum = np.sum([cube[j, j, i] for j in range(CUBE_SIZE)]) 
        diag_xz_sum = np.sum([cube[j, i, j] for j in range(CUBE_SIZE)])  
        
        total_difference += (diag_xy_sum - magic_number) ** 2
        total_difference += (diag_yz_sum - magic_number) ** 2
        total_difference += (diag_xz_sum - magic_number) ** 2

    diag_3d_1 = np.sum([cube[j, j, j] for j in range(CUBE_SIZE)])        
    diag_3d_2 = np.sum([cube[j, j, CUBE_SIZE - 1 - j] for j in range(CUBE_SIZE)])     
    diag_3d_3 = np.sum([cube[j, CUBE_SIZE - 1 - j, j] for j in range(CUBE_SIZE)])     
    diag_3d_4 = np.sum([cube[CUBE_SIZE - 1 - j, j, j] for j in range(CUBE_SIZE)])    

    total_difference += (diag_3d_1 - magic_number) ** 2
    total_difference += (diag_3d_2 - magic_number) ** 2
    total_difference += (diag_3d_3 - magic_number) ** 2
    total_difference += (diag_3d_4 - magic_number) ** 2

    return total_difference

#random cube
def choose_cube_by_random(randomize_count, fitness_values, total_fitness):
    ranges = []
    lower_bound = 1
    for fitness in fitness_values:
        percentage = (fitness / total_fitness) * 100
        upper_bound = lower_bound + round(percentage) - 1
        ranges.append((lower_bound, upper_bound))
        lower_bound = upper_bound + 1

    chosen_cubes = []
    for _ in range(randomize_count):
        rand_number = random.randint(1, 100)
        for idx, (lower, upper) in enumerate(ranges):
            if lower <= rand_number <= upper:
                chosen_cubes.append(idx)
                break
                
    return chosen_cubes

#crossover
def crossover(parent1, parent2):
    n = len(parent1) 
    child1, child2 = parent1.copy(), parent2.copy()

    def valid_position(i, j, k, x, y, z):
        return (i != x) and (j != y) and (k != z)

    attempts = 0
    while attempts < 10:
        i1, j1, k1 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
        i2, j2, k2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)

        if valid_position(i1, j1, k1, i2, j2, k2):
            child1[i1, j1, k1], child2[i2, j2, k2] = parent2[i2, j2, k2], parent1[i1, j1, k1]
            break
        attempts += 1

    parent1_fitness = fitness(parent1)
    parent2_fitness = fitness(parent2)
    child1_fitness = fitness(child1)
    child2_fitness = fitness(child2)


    result_child1 = child1 if child1_fitness < parent1_fitness else parent1
    result_child2 = child2 if child2_fitness < parent2_fitness else parent2

    return result_child1, result_child2

# Mutation
def mutation(cube, mutation_rate=0.05):
    n = cube.shape[0]  

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if random.random() < mutation_rate:
                    cube[i, j, k] = random.randint(1, n**3)  

    return cube

cubes = []
fitness_values = []
total_fitness = 0

for i in range(3):
    numbers = random.sample(range(1, 126), 125)
    cube_5x5x5 = np.array(numbers).reshape((5, 5, 5))
    cubes.append(cube_5x5x5)
    
    fitness_value = fitness(cube_5x5x5, 315)
    fitness_values.append(fitness_value)
    total_fitness += fitness_value


population2 = []


chosen_indices = choose_cube_by_random(4, fitness_values, total_fitness)
parent1, parent2 = cubes[chosen_indices[0]], cubes[chosen_indices[1]]

for idx, (cube, fit) in enumerate(zip(cubes, fitness_values), 1):
    percent = (fit / total_fitness) * 100
    print(f"Cube {idx}:\n{cube}\nFitness: {fit}\nPercent {percent:.2f}%\n")

print("\nRandomly chosen cubes based on percentage ranges:")
for choice in chosen_indices:
    print(choice)

child1, child2 = crossover(parent1, parent2)

child1 = mutation(child1)
child2 = mutation(child2)

population2.append(child1)
population2.append(child2)

# Print results

print("Parent1 Fitness:", fitness(parent1))
print("Parent2 Fitness:", fitness(parent2))
print("Child1 Fitness:", fitness(child1))
print("Child2 Fitness:", fitness(child2))

print("\nParent1:\n", parent1)
print("Parent2:\n", parent2)
print("Child1:\n", child1)
print("Child2:\n", child2)