import numpy as np
import random
import heapq

def create_cube():
    numbers = list(map(int, input("Masukkan 125 angka (dipisahkan spasi) :\n").split()))
    if len(numbers) != 125:
        raise ValueError("Masukkan 125 angka")
    cube = np.array(numbers).reshape((5, 5, 5))
    return cube

def generate_different_cubes(cube, num_cubes=100):
    cubes = []
    for _ in range(num_cubes):
        new_cube = cube.copy()
        i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        new_cube[i1, j1, k1], new_cube[i2, j2, k2] = new_cube[i2, j2, k2], new_cube[i1, j1, k1]
        cubes.append(new_cube)
    return cubes

def fitness(cube, magic_number=315):
    total_difference = 0
    for i in range(5):
        for j in range(5):
            total_difference += abs(np.sum(cube[i, j, :]) - magic_number) 
            total_difference += abs(np.sum(cube[i, :, j]) - magic_number) 
            total_difference += abs(np.sum(cube[:, i, j]) - magic_number) 

    for i in range(5):
        total_difference += abs(np.sum([cube[i, j, j] for j in range(5)]) - magic_number) 
        total_difference += abs(np.sum([cube[j, j, i] for j in range(5)]) - magic_number) 
        total_difference += abs(np.sum([cube[j, i, j] for j in range(5)]) - magic_number) 

    total_difference += abs(np.sum([cube[j, j, j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[j, j, 5 - 1 - j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[j, 5 - 1 - j, j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[5 - 1 - j, j, j] for j in range(5)]) - magic_number)

    return total_difference

def choose_cube_by_random(num_select, priority_queue):
    fitness_values = [1 / (item[0] + 1e-6) for item in priority_queue]
    total_fitness = sum(fitness_values)
    probabilities = [f / total_fitness for f in fitness_values]
    chosen_indices = np.random.choice(len(priority_queue), size=num_select, p=probabilities, replace=False)

    return chosen_indices.tolist()

def find_number_in_cube(cube, number):
    for i in range(5):
        for j in range(5):
            for k in range(5):
                if cube[i, j, k] == number:
                    return (i, j, k)
    return None

def valid_position(i1, j1, k1, i2, j2, k2):
    # Check if they are in the same row, column, or pillar
    if i1 == i2 or j1 == j2 or k1 == k2:
        return False

    # Check if they are on the same plane diagonal
    if (i1 == j1 == k1 and i2 == j2 == k2) or (i1 == j1 and i2 == j2 and k1 + k2 == 4) or \
       (i1 == k1 and i2 == k2 and j1 + j2 == 4) or (j1 == k1 and j2 == k2 and i1 + i2 == 4):
        return False

    return True

def crossover(parent1, parent2):
    n = len(parent1)  
    child1, child2 = parent1.copy(), parent2.copy()
    
    random_number = random.randint(1, 125)
    
    i1, j1, k1 = find_number_in_cube(child1, random_number)
    i2, j2, k2 = find_number_in_cube(child2, random_number)

    while not valid_position(i1, j1, k1, i2, j2, k2):
        random_number = random.randint(1, 125)
        i1, j1, k1 = find_number_in_cube(child1, random_number)
        i2, j2, k2 = find_number_in_cube(child2, random_number)
    
    
    child1[i1, j1, k1], child2[i2, j2, k2] = child2[i2, j2, k2], child1[i1, j1, k1]
    print(f"Crossover: [{i1}, {j1}, {k1}] in child1 swapped with [{i2}, {j2}, {k2}] in child2")

    return child1, child2


def mutation(cube, mutation_rate=0.05):
    num_swaps = int(125 * mutation_rate)
    for _ in range(num_swaps):
        i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        cube[i1, j1, k1], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i1, j1, k1]
    return cube

def run_genetic_algorithm(num_iterations=100):
    cube = create_cube()
    different_cubes = generate_different_cubes(cube, num_cubes=100)
    priority_queue = [(fitness(c), idx) for idx, c in enumerate(different_cubes)]
    heapq.heapify(priority_queue)

    for i in range(num_iterations):
        chosen_indices = choose_cube_by_random(50, priority_queue)

        for j in range(0, len(chosen_indices) - 1, 2):
            idx1, idx2 = chosen_indices[j], chosen_indices[j + 1]
            cube1, cube2 = different_cubes[idx1], different_cubes[idx2]
            child1, child2 = crossover(cube1, cube2)
            child1 = mutation(child1)
            child2 = mutation(child2)
            new_fitness1 = fitness(child1)
            new_fitness2 = fitness(child2)
            different_cubes[idx1], different_cubes[idx2] = child1, child2
            heapq.heappush(priority_queue, (new_fitness1, idx1))
            heapq.heappush(priority_queue, (new_fitness2, idx2))

        priority_queue = heapq.nsmallest(50, priority_queue)
        heapq.heapify(priority_queue)

        best_fitness, best_idx = priority_queue[0]
        print(f"Iterasi {i+1}: Fitness terbaik saat ini = {best_fitness}")

    return different_cubes[best_idx], best_fitness

best_cube, best_fitness = run_genetic_algorithm(100)
print("\nKubus Terbaik:")
print(best_cube)
print("Nilai Fitness Terbaik:", best_fitness)