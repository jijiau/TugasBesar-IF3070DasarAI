import numpy as np
import random

# Parameter variasi dan iterasi
population_sizes = [10, 20, 30]
iterations = [100, 200, 300]
num_trials = 3

# Fungsi Fitness untuk menghitung perbedaan dari magic number
def fitness(cube, magic_number=315):
    CUBE_SIZE = 5
    total_difference = 0

    # Baris, Kolom, Tiang
    for i in range(CUBE_SIZE):
        for j in range(CUBE_SIZE):
            row_sum = np.sum(cube[i, j, :])
            col_sum = np.sum(cube[i, :, j])
            pillar_sum = np.sum(cube[:, i, j])
            total_difference += (row_sum - magic_number) ** 2
            total_difference += (col_sum - magic_number) ** 2
            total_difference += (pillar_sum - magic_number) ** 2

    # Diagonal bidang
    for i in range(CUBE_SIZE):
        diag_xy_sum = np.sum([cube[i, j, j] for j in range(CUBE_SIZE)])  # XY
        diag_yz_sum = np.sum([cube[j, j, i] for j in range(CUBE_SIZE)])  # YZ
        diag_xz_sum = np.sum([cube[j, i, j] for j in range(CUBE_SIZE)])  # XZ
        total_difference += (diag_xy_sum - magic_number) ** 2
        total_difference += (diag_yz_sum - magic_number) ** 2
        total_difference += (diag_xz_sum - magic_number) ** 2

    # Diagonal ruang
    diag_3d_1 = np.sum([cube[j, j, j] for j in range(CUBE_SIZE)])                      
    diag_3d_2 = np.sum([cube[j, j, CUBE_SIZE - 1 - j] for j in range(CUBE_SIZE)])  
    diag_3d_3 = np.sum([cube[j, CUBE_SIZE - 1 - j, j] for j in range(CUBE_SIZE)]) 
    diag_3d_4 = np.sum([cube[CUBE_SIZE - 1 - j, j, j] for j in range(CUBE_SIZE)])    
    total_difference += (diag_3d_1 - magic_number) ** 2
    total_difference += (diag_3d_2 - magic_number) ** 2
    total_difference += (diag_3d_3 - magic_number) ** 2
    total_difference += (diag_3d_4 - magic_number) ** 2

    return total_difference

# Inisialisasi populasi awal
def initial_population(population_size):
    cubes = []
    numbers = list(range(1, 126))
    for _ in range(population_size):
        random.shuffle(numbers)
        cube = np.array(numbers).reshape((5, 5, 5))
        cubes.append(cube)
    return cubes

# Seleksi dengan Roulette Wheel
def roulette_wheel_selection(cubes, fitness_values, k=3):
    selected = []
    for _ in range(2):
        tournament = random.sample(list(zip(cubes, fitness_values)), k)
        winner = min(tournament, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected

# Partially Matched Crossover (PMX)
def partially_matched_crossover(parent1, parent2):
    n = parent1.shape[0]
    child1, child2 = parent1.copy(), parent2.copy()
    
    # Tentukan rentang crossover
    start, end = sorted(random.sample(range(n * n * n), 2))
    
    # Peta pasangan untuk menjaga kesamaan posisi
    mapping1, mapping2 = {}, {}
    for i in range(start, end + 1):
        idx = np.unravel_index(i, parent1.shape)
        child1[idx], child2[idx] = parent2[idx], parent1[idx]
        mapping1[child1[idx]] = child2[idx]
        mapping2[child2[idx]] = child1[idx]
    
    # Memastikan konsistensi berdasarkan peta pasangan
    for i in range(n * n * n):
        if not (start <= i <= end):
            idx = np.unravel_index(i, parent1.shape)
            while child1[idx] in mapping1:
                child1[idx] = mapping1[child1[idx]]
            while child2[idx] in mapping2:
                child2[idx] = mapping2[child2[idx]]
    
    return child1, child2

# Swap Mutation
def swap_mutation(cube, mutation_rate=0.1):
    n = cube.shape[0]
    for _ in range(int(n * n * n * mutation_rate)):
        i1, j1, k1 = random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)
        i2, j2, k2 = random.randint(0, n - 1), random.randint(0, n - 1), random.randint(0, n - 1)
        cube[i1, j1, k1], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i1, j1, k1]
    return cube

# Fungsi utama algoritma genetika
def run_genetic_algorithm(population_size, num_iterations):
    cubes = initial_population(population_size)
    best_cube = None
    best_fitness = float('inf')

    for _ in range(num_iterations):
        # Evaluasi fitness
        fitness_values = [fitness(cube) for cube in cubes]
        
        # Simpan individu terbaik
        for cube, fit_value in zip(cubes, fitness_values):
            if fit_value < best_fitness:
                best_fitness = fit_value
                best_cube = cube
        if best_fitness == 0:
            break

        # Membuat populasi baru dengan crossover dan mutasi
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = roulette_wheel_selection(cubes, fitness_values)
            child1, child2 = partially_matched_crossover(parent1, parent2)
            child1 = swap_mutation(child1)
            child2 = swap_mutation(child2)
            new_population.extend([child1, child2])

        # Perbarui populasi
        cubes = new_population[:population_size]

    return best_cube, best_fitness

# Menjalankan eksperimen dengan berbagai konfigurasi
global_best_cube = None
global_best_fitness = float('inf')

for pop_size in population_sizes:
    for num_iter in iterations:
        best_cube, best_fitness = run_genetic_algorithm(pop_size, num_iter)
        print(f"Populasi: {pop_size}, Iterasi: {num_iter}, Fitness Terbaik: {best_fitness}")

        if best_fitness < global_best_fitness:
            global_best_fitness = best_fitness
            global_best_cube = best_cube

print("\nGlobal Best Cube:\n", global_best_cube)
print("Global Best Fitness Value:", global_best_fitness)
