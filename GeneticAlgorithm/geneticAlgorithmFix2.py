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
def choose_cube_by_random(randomize_count, priority_queue):
    inverted_fitness_values = [float(1 / item[0]) for item in priority_queue]
    total_inverted_fitness_values = sum(inverted_fitness_values)

    ranges = []
    lower_bound = 0

    # print("inverted")
    # print(inverted_fitness_values)

    for inverted_fitness in inverted_fitness_values:
        percentage = (inverted_fitness / total_inverted_fitness_values) * 100
        upper_bound = lower_bound + round(percentage) - 1
        ranges.append((lower_bound, upper_bound))
        lower_bound = upper_bound
    
    

    chosen_indices = []
    for _ in range(randomize_count):
        rand_number = random.uniform(0, 100)
        
        for idx, (lower, upper) in enumerate(ranges):
            if lower <= rand_number <= upper:
                chosen_indices.append(idx) 
                break

    # print(rand_number)
    print("Chosen indices: ")
    print(chosen_indices)

    return chosen_indices
        (i1, j1, k1, ji2, 2, k2):
    if i == x or j == y or k == z:
        return False

    if i == j and x == y:
        return False
    if i == (5 - 1 - j) and x == (5 - 1 - y):  # Diagonal berlawanan pada bidang XY
        return False
    # Diagonal pada bidang YZ
    if j == k and y == z:
        return False
    if j == (5 - 1 - k) and y == (5 - 1 - z):  # Diagonal berlawanan pada bidang YZ
        return False
    # Diagonal pada bidang XZ
    if i == k and x == z:
        return False
    if i == (5 - 1 - k) and x == (5 - 1 - z):  # Diagonal berlawanan pada bidang XZ
        return False

    # Pastikan koordinat tidak berada pada diagonal ruang yang sama
    if (i == j == k) and (x == y == z):  # Diagonal utama (dari sudut ke sudut berlawanan)
        return False
    if (i == j == (5 - 1 - k)) and (x == y == (5 - 1 - z)):  # Diagonal melintang
        return False
    if (i == (5 - 1 - j) == k) and (x == (5 - 1 - y) == z):  # Diagonal lainnya
        return False
    if (i == (5 - 1 - j) == (5 - 1 - k)) and (x == (5 - 1 - y) == (5 - 1 - z)):  # Diagonal ruang melintang berlawanan
        return False

    return True

def find_number_in_cube(parent, x):
    n = parent.shape[0]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if parent[i, j, k] == x:
                    return (i, j, k) 
    return None

# Fungsi crossover
def crossover(parent1, parent2):
    n = len(parent1)  
    child1, child2 = parent1.copy(), parent2.copy()
    random_number = random.randint(1, 125)

    i1, j1, k1 = find_number_in_cube(parent1, random_number)
    i2, j2, k2 = find_number_in_cube(parent2, random_number)

    while (not valid_position(i1, j1, k1, i2, j2, k2)):
        random_number = random.randint(1, 125)

        i1, j1, k1 = find_number_in_cube(parent1, random_number)
        i2, j2, k2 = find_number_in_cube(parent2, random_number)

    val1 = child1[i1, j1, k1]
    val2 = child2[i1, j1, k1]
    child1[i1, j1, k1], child2[i1, j1, k1] = child1[i2, j2, k2], child2[i2, j2, k2]      
    child1[i2, j2, k2], child2[i2, j2, k2] = val1, val2

    print(f"[{i1}, {j1}, {k1}] ditukar dengan [{i2}, {j2}, {k2}]")

    return child1, child2

def run_genetic_algorithm(num_iterations=100):
    cube = create_cube()
    different_cubes = generate_different_cubes(cube, num_cubes=100)
    priority_queue = [(fitness(c), idx) for idx, c in enumerate(different_cubes)]
    heapq.heapify(priority_queue)

    for i in range(num_iterations):
        chosen_indices = choose_cube_by_random(100, priority_queue)
        for j in range(0, len(chosen_indices) - 1, 2):
            idx1, idx2 = chosen_indices[j], chosen_indices[j + 1]
            cube1, cube2 = different_cubes[idx1], different_cubes[idx2]
            child1, child2 = crossover(cube1, cube2)
            new_fitness1 = fitness(child1)
            new_fitness2 = fitness(child2)
            different_cubes[idx1], different_cubes[idx2] = child1, child2
            heapq.heappush(priority_queue, (new_fitness1, idx1))
            heapq.heappush(priority_queue, (new_fitness2, idx2))
        
        for j in range(0, 50, 2):
            if j + 1 >= len(chosen_indices):
                break
            idx1, idx2 = chosen_indices[j], chosen_indices[j + 1]
            cube1, cube2 = different_cubes[idx1], different_cubes[idx2]
            mutated_cube1 = mutation(cube1)
            mutated_cube2 = mutation(cube2)
            new_fitness1 = fitness(mutated_cube1)
            new_fitness2 = fitness(mutated_cube2)
            different_cubes[idx1], different_cubes[idx2] = mutated_cube1, mutated_cube2
            heapq.heappush(priority_queue, (new_fitness1, idx1))
            heapq.heappush(priority_queue, (new_fitness2, idx2))

        priority_queue = heapq.nsmallest(6, priority_queue) + priority_queue[6:]
        heapq.heapify(priority_queue)
        best_fitness, best_idx = priority_queue[0]
        print(f"Iterasi {i+1}: Fitness terbaik saat ini = {best_fitness}")

    return different_cubes[best_idx], best_fitness

# def run_genetic_algorithm(num_iterations=100):
#     priority_queue = []
#     cube = create_cube()
#     different_cubes = generate_different_cubes(cube, num_cubes=100)
#     priority_queue_new = []

#     for c in different_cubes:
#         fit = fitness(c)
#         heapq.heappush(priority_queue, (fit, c))

#     for i in range(num_iterations):
#         fitness_values = [item[0] for item in priority_queue]
#         total_fitness = sum(fitness_values)

#         chosen_indices = choose_cube_by_random(10, priority_queue)

#         for j in range(0, (len(chosen_indices)/2) - 1, 2):
#             idx1, idx2 = chosen_indices[j], chosen_indices[j + 1]
#             fitness1, cube1 = priority_queue[idx1]
#             fitness2, cube2 = priority_queue[idx2]

#             child1, child2 = crossover(cube1, cube2)
#             child1 = mutation(cube1)
#             child2 = mutation(cube2)

#             new_fitness1 = fitness(cube1)
#             new_fitness2 = fitness(cube2)

#             heapq.heappush(priority_queue_new, (new_fitness1, cube1))
#             heapq.heappush(priority_queue_new, (new_fitness2, cube2))

#         best_cubes_from_last_gen = heapq.nsmallest(6, priority_queue)

#         priority_queue_new = best_cubes_from_last_gen + priority_queue[6:]
#         heapq.heapify(priority_queue_new)

#         priority_queue = priority_queue_new_gen

#         best_fitness, best_cube = priority_queue[0]
#         print(f"Iterasi {i+1}: Fitness terbaik saat ini = {best_fitness}")

    return best_cube, best_fitness


best_cube, best_fitness = run_genetic_algorithm(100)
print("\nKubus Terbaik:")
print(best_cube)
print("Nilai Fitness Terbaik:", best_fitness)
