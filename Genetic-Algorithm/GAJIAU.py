import numpy as np
import random

# parameter variasi dan iterasi
population_sizes = [10, 20, 30] 
iterations = [50, 100, 150]     
num_trials = 3                  

# fitness function
def fitness(cube, magic_number=315):
    CUBE_SIZE = 5
    total_difference = 0

    # baris, kolom, tiang
    for i in range(CUBE_SIZE):
        for j in range(CUBE_SIZE):
            row_sum = np.sum(cube[i, j, :])       # baris
            col_sum = np.sum(cube[i, :, j])       # kolom
            pillar_sum = np.sum(cube[:, i, j])    # tiang
            total_difference += (row_sum - magic_number) ** 2
            total_difference += (col_sum - magic_number) ** 2
            total_difference += (pillar_sum - magic_number) ** 2

    # diagonal bidang
    for i in range(CUBE_SIZE):
        diag_xy_sum = np.sum([cube[i, j, j] for j in range(CUBE_SIZE)])  # XY
        diag_yz_sum = np.sum([cube[j, j, i] for j in range(CUBE_SIZE)])  # YZ
        diag_xz_sum = np.sum([cube[j, i, j] for j in range(CUBE_SIZE)])  # XZ
        total_difference += (diag_xy_sum - magic_number) ** 2
        total_difference += (diag_yz_sum - magic_number) ** 2
        total_difference += (diag_xz_sum - magic_number) ** 2

    # diagonal ruang
    diag_3d_1 = np.sum([cube[j, j, j] for j in range(CUBE_SIZE)])                      
    diag_3d_2 = np.sum([cube[j, j, CUBE_SIZE - 1 - j] for j in range(CUBE_SIZE)])  
    diag_3d_3 = np.sum([cube[j, CUBE_SIZE - 1 - j, j] for j in range(CUBE_SIZE)]) 
    diag_3d_4 = np.sum([cube[CUBE_SIZE - 1 - j, j, j] for j in range(CUBE_SIZE)])    
    total_difference += (diag_3d_1 - magic_number) ** 2
    total_difference += (diag_3d_2 - magic_number) ** 2
    total_difference += (diag_3d_3 - magic_number) ** 2
    total_difference += (diag_3d_4 - magic_number) ** 2

    return total_difference

# population initialization with unique permutation
def initial_population(population_size):
    cubes = []
    numbers = list(range(1, 126))
    for _ in range(population_size):
        random.shuffle(numbers)
        cube = np.array(numbers).reshape((5, 5, 5))
        cubes.append(cube)
    return cubes

# random cube selection with probabilistic weight
def choose_cube_by_random(fitness_values, total_fitness, randomize_count=2):
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

# crossover with row or column swapping
# def crossover(parent1, parent2):
#     n = len(parent1)
#     child1, child2 = parent1.copy(), parent2.copy()
#     axis = random.choice([0, 1])  # 0 for row, 1 for column
#     idx = random.randint(0, n-1)
    
#     if axis == 0:  # row swapping
#         child1[idx, :, :], child2[idx, :, :] = parent2[idx, :, :].copy(), parent1[idx, :, :].copy()
#     else:  # column swapping
#         child1[:, idx, :], child2[:, idx, :] = parent2[:, idx, :].copy(), parent1[:, idx, :].copy()
    
#     return child1, child2

def valid_position(i, j, k, x, y, z):
    # Pastikan koordinat tidak berada pada baris, kolom, atau tiang yang sama
    if i == x or j == y or k == z:
        return False
    
    # Pastikan koordinat tidak berada pada diagonal bidang yang sama
    # Diagonal pada bidang XY
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

#crossover
def crossover(parent1, parent2):
    n = len(parent1)  # Size of the cube
    child1, child2 = parent1.copy(), parent2.copy()

    i1, j1, k1 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    i2, j2, k2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)

    while (not valid_position(i1, j1, k1, i2, j2, k2) and (child1[i1, j1, k1] != child2[i2, j2, k2])):
        i1, j1, k1 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
        i2, j2, k2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    
    child1[i1, j1, k1], child2[i2, j2, k2] = parent2[i2, j2, k2], parent1[i1, j1, k1]
    return child1, child2

# mutation with swapping two random elements
def mutation(cube):
    i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
    i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)

    cube[i1, j1, k1], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i1, j1, k1]

    return cube

# main genetic algorithm function
def run_genetic_algorithm(population_size, num_iterations):
    # Inisialisasi populasi awal
    cubes = initial_population(population_size)
    best_cube = None
    best_fitness = float('inf')

    for _ in range(num_iterations):
        # Hitung fitness untuk seluruh populasi
        fitness_values = [fitness(cube) for cube in cubes]
        
        # Cari kubus dengan fitness terbaik
        for cube, fit_value in zip(cubes, fitness_values):
            if fit_value < best_fitness:
                best_fitness = fit_value
                best_cube = cube
        
        # Cek kriteria berhenti jika solusi optimal ditemukan
        if best_fitness == 0:
            break

        # Buat populasi baru dengan anak-anak hasil crossover
        new_population = []
        for i in range(0, population_size, 2):
            # Pasangkan dua parent secara berurutan
            parent1, parent2 = cubes[i], cubes[i + 1]
            
            # Lakukan crossover untuk menghasilkan dua anak
            child1, child2 = crossover(parent1, parent2)
            
            # Terapkan mutasi pada anak-anak
            child1 = mutation(child1)
            child2 = mutation(child2)
            
            # Tambahkan anak-anak ke populasi baru
            new_population.extend([child1, child2])

        # Gantikan populasi lama dengan populasi baru
        cubes = new_population

    return best_cube, best_fitness


# Running with various configurations
global_best_cube = None
global_best_fitness = float('inf')

for pop_size in population_sizes:
    for _ in range(num_trials):
        for num_iter in iterations:
            best_cube, best_fitness = run_genetic_algorithm(pop_size, num_iter)
            if best_fitness < global_best_fitness:
                global_best_fitness = best_fitness
                global_best_cube = best_cube

print("Global Best Cube:\n", global_best_cube)
print("Global Best Fitness Value:", global_best_fitness)
