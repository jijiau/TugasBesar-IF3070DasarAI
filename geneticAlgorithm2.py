import numpy as np
import random

def initial_population(fitness, total_fitness):
    return fitness / total_fitness

#calculate fitness
def fitness(cube, magic_number=315):
    CUBE_SIZE = 5
    total_difference = 0

    # Calculate differences for rows, columns, and pillars
    for i in range(CUBE_SIZE):
        for j in range(CUBE_SIZE):
            row_sum = np.sum(cube[i, j, :])       # Sum for row
            col_sum = np.sum(cube[i, :, j])       # Sum for column
            pillar_sum = np.sum(cube[:, i, j])    # Sum for pillar
            
            # Calculate and add squared differences
            total_difference += (row_sum - magic_number) ** 2
            total_difference += (col_sum - magic_number) ** 2
            total_difference += (pillar_sum - magic_number) ** 2

    # Calculate differences for plane diagonals
    for i in range(CUBE_SIZE):
        diag_xy_sum = np.sum([cube[i, j, j] for j in range(CUBE_SIZE)])  # Diagonal on XY plane
        diag_yz_sum = np.sum([cube[j, j, i] for j in range(CUBE_SIZE)])  # Diagonal on YZ plane
        diag_xz_sum = np.sum([cube[j, i, j] for j in range(CUBE_SIZE)])  # Diagonal on XZ plane
        
        # Add squared differences for each diagonal
        total_difference += (diag_xy_sum - magic_number) ** 2
        total_difference += (diag_yz_sum - magic_number) ** 2
        total_difference += (diag_xz_sum - magic_number) ** 2

    # Calculate differences for space (3D) diagonals
    diag_3d_1 = np.sum([cube[j, j, j] for j in range(CUBE_SIZE)])                       # Diagonal from (0,0,0) to (4,4,4)
    diag_3d_2 = np.sum([cube[j, j, CUBE_SIZE - 1 - j] for j in range(CUBE_SIZE)])       # Diagonal from (0,0,4) to (4,4,0)
    diag_3d_3 = np.sum([cube[j, CUBE_SIZE - 1 - j, j] for j in range(CUBE_SIZE)])       # Diagonal from (0,4,0) to (4,0,4)
    diag_3d_4 = np.sum([cube[CUBE_SIZE - 1 - j, j, j] for j in range(CUBE_SIZE)])       # Diagonal from (4,0,0) to (0,4,4)

    # Add squared differences for each 3D diagonal
    total_difference += (diag_3d_1 - magic_number) ** 2
    total_difference += (diag_3d_2 - magic_number) ** 2
    total_difference += (diag_3d_3 - magic_number) ** 2
    total_difference += (diag_3d_4 - magic_number) ** 2

    return total_difference

#random selection
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
        print(rand_number)
        for idx, (lower, upper) in enumerate(ranges):
            if lower <= rand_number <= upper:
                chosen_cubes.append(f"Cube {idx + 1}")
                break
                
    return chosen_cubes

#crossover
def crossover(parent1, parent2):
    n = len(parent1)
    child = parent1.copy()

    dimension = random.randint(0, 2)
    divide = random.randint(0, n - 1)

    if dimension == 0:
        child[:divide, :, :] = parent2[:divide, :, :]
    elif dimension == 1:
        child[:, :divide, :] = parent2[:, :divide, :]
    else:
        child[:, :, :divide] = parent2[:, :, :divide]

    return child

#mutation
def mutation(cube):
    n = len(cube)

    idx1 = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
    idx2 = (random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1))
    cube[idx1], cube[idx2] = cube[idx2], cube[idx1]
    return cube

# Generate 3 random cubes and calculate their fitness
cubes = []
fitness_values = []
total_fitness = 0

for i in range(3):
    # Generate a list of unique random numbers from 1 to 125
    numbers = random.sample(range(1, 126), 125)
    
    # Reshape the list into a 5x5x5 cube
    cube_5x5x5 = np.array(numbers).reshape((5, 5, 5))
    cubes.append(cube_5x5x5)
    
    # Calculate and store the fitness for each cube
    fitness_value = fitness(cube_5x5x5, 315)
    fitness_values.append(fitness_value)
    total_fitness += fitness_value

# Print each cube, its fitness, and its percentage range
for idx, (cube, fit) in enumerate(zip(cubes, fitness_values), 1):
    percent = (fit / total_fitness) * 100
    print(f"Cube {idx}:\n{cube}\nFitness: {fit}\nPercent {percent:.2f}%\n")

# Choose cubes based on random numbers
randomize_count = 4  # Number of times to randomize
chosen_cubes = choose_cube_by_random(randomize_count, fitness_values, total_fitness)

# Print results
print("\nRandomly chosen cubes based on percentage ranges:")
for choice in chosen_cubes:
    print(choice)