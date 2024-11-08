import numpy as np
import random

#parameter variasi dan iterasi
population_sizes = [10, 20, 30] 
iterations = [50, 100, 150]     
num_trials = 3                  

#population
def initial_population(fitness, total_fitness):
    return fitness / total_fitness

#fitness
def fitness(cube, magic_number=315):
    CUBE_SIZE = 5
    total_difference = 0

    #baris, kolom, tiang
    for i in range(CUBE_SIZE):
        for j in range(CUBE_SIZE):
            row_sum = np.sum(cube[i, j, :])       #baris
            col_sum = np.sum(cube[i, :, j])       #kolom
            pillar_sum = np.sum(cube[:, i, j])    #tiang
            total_difference += (row_sum - magic_number) ** 2
            total_difference += (col_sum - magic_number) ** 2
            total_difference += (pillar_sum - magic_number) ** 2

    #diagonal bidang
    for i in range(CUBE_SIZE):
        diag_xy_sum = np.sum([cube[i, j, j] for j in range(CUBE_SIZE)])  #XY
        diag_yz_sum = np.sum([cube[j, j, i] for j in range(CUBE_SIZE)])  #YZ
        diag_xz_sum = np.sum([cube[j, i, j] for j in range(CUBE_SIZE)])  #XZ
        total_difference += (diag_xy_sum - magic_number) ** 2
        total_difference += (diag_yz_sum - magic_number) ** 2
        total_difference += (diag_xz_sum - magic_number) ** 2

    #diagonal ruang
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
    n = len(parent1)  # Size of the cube
    child1, child2 = parent1.copy(), parent2.copy()

    def valid_position(i, j, k, x, y, z):
        if (i == x) or (j == y) or (k == z):
            return False
        if (i == j == k) or (x == y == z): 
            return False
        if (i == j and x == y) or (i == k and x == z) or (j == k and y == z):
            return False
        if (i + j == n - 1 and x + y == n - 1) or (i + k == n - 1 and x + z == n - 1) or (j + k == n - 1 and y + z == n - 1):
            return False
        
        return True

    attempts = 0
    while attempts < 10:
        i1, j1, k1 = random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)
        i2, j2, k2 = random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)

        if valid_position(i1, j1, k1, i2, j2, k2):
            child1[i1, j1, k1], child2[i2, j2, k2] = parent2[i2, j2, k2], parent1[i1, j1, k1]
            break
        attempts += 1

    return child1, child2

#mutation
def mutation(cube, mutation_rate=0.05):
    n = cube.shape[0]  
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if random.random() < mutation_rate:
                    i2, j2, k2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
                    cube[i, j, k], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i, j, k]
    return cube

def run_genetic_algorithm(population_size, num_iterations):
    cubes = []
    fitness_values = []
    total_fitness = 0

    #smallest fitness (best cube)
    best_cube = None
    best_fitness = float('inf')

    for _ in range(population_size):
        numbers = random.sample(range(1, 126), 125)
        cube = np.array(numbers).reshape((5, 5, 5))
        cubes.append(cube)
        fit_value = fitness(cube)
        fitness_values.append(fit_value)
        total_fitness += fit_value

        if fit_value < best_fitness:
            best_fitness = fit_value
            best_cube = cube

    for _ in range(num_iterations):
        chosen_indices = choose_cube_by_random(2, fitness_values, total_fitness)
        if len(chosen_indices) < 2:
            continue

        parent1, parent2 = cubes[chosen_indices[0]], cubes[chosen_indices[1]]

        #crossover & mutation
        child1, child2 = crossover(parent1, parent2)
        child1 = mutation(child1)
        child2 = mutation(child2)

        #update best child
        for child in [child1, child2]:
            child_fitness = fitness(child)
            if child_fitness < best_fitness:
                best_fitness = child_fitness
                best_cube = child

    return best_cube, best_fitness

#global best cube & fitness
global_best_cube = None
global_best_fitness = float('inf')

for pop_size in population_sizes:
    for _ in range(num_trials):
        for num_iter in iterations:
            print(f"\nRunning GA with Population Size: {pop_size}, Iterations: {num_iter}")
            best_cube, best_fitness = run_genetic_algorithm(pop_size, num_iter)
            print("\nBest cube found in this run:")
            print(best_cube)
            print("Best fitness value:", best_fitness)

            if best_fitness < global_best_fitness:
                global_best_fitness = best_fitness
                global_best_cube = best_cube

print("\nGlobal Best Result")
print("Global Best Cube:\n", global_best_cube)
print("Global Best Fitness Value:", global_best_fitness)