import numpy as np
import random
import matplotlib.pyplot as plt
import time

# Fungsi untuk membuat *magic cube* awal
def create_cube():
    numbers = list(range(1, 126))
    random.shuffle(numbers)
    cube = np.array(numbers).reshape((5, 5, 5))
    return cube

# Fungsi untuk mengukur *fitness* dari *cube*
def fitness(cube, magic_number=315):
    total_difference = 0
    for i in range(5):
        for j in range(5):
            total_difference += abs(np.sum(cube[i, j, :]) - magic_number)  # Row sum
            total_difference += abs(np.sum(cube[i, :, j]) - magic_number)  # Column sum
            total_difference += abs(np.sum(cube[:, i, j]) - magic_number)  # Pillar sum
    # Check diagonal sums
    for i in range(5):
        total_difference += abs(np.sum([cube[i, j, j] for j in range(5)]) - magic_number)
        total_difference += abs(np.sum([cube[j, j, i] for j in range(5)]) - magic_number)
        total_difference += abs(np.sum([cube[j, i, j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[j, j, j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[j, j, 5 - 1 - j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[j, 5 - 1 - j, j] for j in range(5)]) - magic_number)
    total_difference += abs(np.sum([cube[5 - 1 - j, j, j] for j in range(5)]) - magic_number)

    return total_difference

# Inisialisasi populasi awal
def generate_population(cube, population_size):
    population = []
    for _ in range(population_size):
        new_cube = cube.copy()
        i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        new_cube[i1, j1, k1], new_cube[i2, j2, k2] = new_cube[i2, j2, k2], new_cube[i1, j1, k1]
        population.append(new_cube)
    return population

# Fungsi crossover: Menukar dua angka secara acak antara dua parent terbaik
def crossover(parent1, parent2):
    child1, child2 = parent1.copy(), parent2.copy()
    indices = list(range(125))
    random.shuffle(indices)
    
    for idx in indices:
        i, j, k = np.unravel_index(idx, (5, 5, 5))
        if child1[i, j, k] != child2[i, j, k]:
            child1[i, j, k], child2[i, j, k] = child2[i, j, k], child1[i, j, k]
            # Pastikan setiap anak tetap unik
            if len(set(child1.flatten())) == 125 and len(set(child2.flatten())) == 125:
                break
            # Batalkan swap jika keunikan tidak terpenuhi
            child1[i, j, k], child2[i, j, k] = child2[i, j, k], child1[i, j, k]
    
    # Pastikan hasil akhir memiliki angka unik; jika tidak, ulangi
    if len(set(child1.flatten())) != 125 or len(set(child2.flatten())) != 125:
        return crossover(parent1, parent2)
    return child1 if fitness(child1) < fitness(child2) else child2

# Fungsi mutasi: Menukar dua angka secara acak di dalam cube
def mutation(cube, mutation_rate=0.05):
    num_swaps = int(125 * mutation_rate)
    mutated_cube = cube.copy()
    for _ in range(num_swaps):
        i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        # Swap hanya jika tidak menyebabkan duplikasi
        if mutated_cube[i1, j1, k1] != mutated_cube[i2, j2, k2]:
            mutated_cube[i1, j1, k1], mutated_cube[i2, j2, k2] = mutated_cube[i2, j2, k2], mutated_cube[i1, j1, k1]
    # Pastikan hasilnya unik
    if len(set(mutated_cube.flatten())) != 125:
        return mutation(cube, mutation_rate)  # Ulangi jika ada duplikasi
    return mutated_cube


# Fungsi utama algoritma genetika
def run_genetic_algorithm(cube, population_size, num_iterations, crossover_prob=0.8, mutation_prob=0.8):
    population = generate_population(cube, population_size)
    history = []
    start_time = time.time()

    for iteration in range(num_iterations):
        # Hitung fitness seluruh populasi
        population = sorted(population, key=fitness)
        best_fitness = fitness(population[0])
        avg_fitness = np.mean([fitness(ind) for ind in population])
        history.append((best_fitness, avg_fitness))

        # Tentukan 50% terbaik dan 50% terburuk
        top_half = population[:population_size // 2]
        bottom_half = population[population_size // 2:]

        # Crossover pada 50% terbaik dengan kemungkinan crossover
        new_population = []
        for i in range(0, len(top_half) - 1, 2):
            parent1, parent2 = top_half[i], top_half[i + 1]
            # Hanya lakukan crossover berdasarkan probabilitas yang ditentukan
            if random.random() < crossover_prob:
                child = crossover(parent1, parent2)
                new_population.append(child)
            else:
                # Jika tidak crossover, pertahankan parent asli
                new_population.extend([parent1, parent2])

        # Mutasi pada 50% terburuk dengan kemungkinan mutasi
        for individual in bottom_half:
            # Hanya lakukan mutasi berdasarkan probabilitas yang ditentukan
            if random.random() < mutation_prob:
                mutated_individual = mutation(individual.copy())
                new_population.append(mutated_individual)
            else:
                new_population.append(individual)

        # Jika populasi baru kurang dari ukuran yang diharapkan, tambahkan dari populasi terbaik
        while len(new_population) < population_size:
            new_population.append(population[len(new_population) % len(population)].copy())

        # Memastikan ukuran populasi tidak lebih dari kapasitas awal
        population = new_population[:population_size]

        print(f"Iterasi {iteration + 1}: Fitness Terbaik = {best_fitness}")

    end_time = time.time()
    duration = end_time - start_time
    return population[0], best_fitness, history, duration

# Menjalankan eksperimen dengan berbagai parameter
def run_experiments():
    initial_cube = create_cube()
    population_variations = [4, 6, 8]
    iteration_variations = [10, 20, 30]
    num_trials = 3  # Jumlah trial

    all_results = []
    for pop_size in population_variations:
        for num_iter in iteration_variations:
            for trial in range(num_trials):
                print(f"\nPopulasi: {pop_size}, Iterasi: {num_iter}, Trial: {trial + 1}")
                best_cube, best_fitness, history, duration = run_genetic_algorithm(initial_cube, pop_size, num_iter)
                all_results.append((pop_size, num_iter, best_fitness, best_cube, history, duration))

                # Pengecekan apakah kubus terbaik memiliki angka unik
                if len(set(best_cube.flatten())) != 125:
                    print("Kubus terbaik memiliki duplikasi angka. Perbaiki mekanisme crossover atau mutasi.")
                else:
                    print("Kubus terbaik tidak memiliki angka duplikat.")

                # Plot nilai fitness
                history_best, history_avg = zip(*history)
                plt.plot(range(len(history_best)), history_best, label="Fitness Terbaik")
                plt.plot(range(len(history_avg)), history_avg, label="Fitness Rata-rata")
                plt.xlabel("Iterasi")
                plt.ylabel("Nilai Fitness")
                plt.title(f"Populasi: {pop_size}, Iterasi: {num_iter}")
                plt.legend()
                # plt.show()  # Uncomment if you want to show each plot immediately

    return all_results

# Menjalankan eksperimen
results = run_experiments()
