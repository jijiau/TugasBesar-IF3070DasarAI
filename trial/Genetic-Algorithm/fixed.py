import numpy as np
import random

# Parameter variasi dan iterasi
population_sizes = [10, 20, 30]
iterations = [100, 200, 300]
num_trials = 3

# Fungsi untuk memperbaiki kubus agar tidak ada angka yang berulang
def make_unique(cube):
    n = cube.shape[0]
    all_numbers = set(range(1, n**3 + 1))
    used_numbers = set(cube.flatten())
    missing_numbers = list(all_numbers - used_numbers)

    if missing_numbers:
        duplicates = [num for num in used_numbers if list(cube.flatten()).count(num) > 1]
        for duplicate in duplicates:
            pos = np.argwhere(cube == duplicate)
            for p in pos[1:]:
                cube[tuple(p)] = missing_numbers.pop(0)
                if not missing_numbers:
                    break
    return cube

# Fungsi Fitness
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
        diag_xy_sum = np.sum([cube[i, j, j] for j in range(CUBE_SIZE)])  
        diag_yz_sum = np.sum([cube[j, j, i] for j in range(CUBE_SIZE)])  
        diag_xz_sum = np.sum([cube[j, i, j] for j in range(CUBE_SIZE)])  
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

# Seleksi dengan Tournament
def tournament_selection(cubes, fitness_values, k=3):
    selected = []
    for _ in range(2):
        tournament = random.sample(list(zip(cubes, fitness_values)), k)
        winner = min(tournament, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected

# Uniform Crossover
def uniform_crossover(parent1, parent2):
    child1, child2 = parent1.copy(), parent2.copy()
    for i in range(child1.shape[0]):
        for j in range(child1.shape[1]):
            for k in range(child1.shape[2]):
                if random.random() < 0.5:
                    child1[i, j, k], child2[i, j, k] = child2[i, j, k], child1[i, j, k]
    return make_unique(child1), make_unique(child2)

# Mutasi dengan Laju Dinamis
def mutation(cube, mutation_rate=0.1):
    n = cube.shape[0]
    for i in range(n):
        if random.random() < mutation_rate:
            row, col = random.randint(0, n - 1), random.randint(0, n - 1)
            np.random.shuffle(cube[row, col, :])
    return make_unique(cube)

# Fungsi utama algoritma genetika
def run_genetic_algorithm(population_size, num_iterations):
    cubes = initial_population(population_size)
    best_cube = None
    best_fitness = float('inf')

    for iteration in range(num_iterations):
        fitness_values = [fitness(cube) for cube in cubes]

        for cube, fit_value in zip(cubes, fitness_values):
            if fit_value < best_fitness:
                best_fitness = fit_value
                best_cube = cube
        if best_fitness == 0:
            break

        # Dinamis Mutasi: Turunkan mutation rate jika mendekati solusi
        mutation_rate = max(0.01, 0.1 * (1 - (iteration / num_iterations)))

        # Populasi baru
        new_population = [best_cube]  
        for _ in range(population_size // 2):
            parent1, parent2 = tournament_selection(cubes, fitness_values)
            child1, child2 = uniform_crossover(parent1, parent2)
            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        cubes = new_population[:population_size]

    return best_cube, best_fitness

# Eksperimen dengan berbagai konfigurasi
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
