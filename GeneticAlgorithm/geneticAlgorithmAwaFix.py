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
        np.random.shuffle(new_cube.flat)
        cubes.append(new_cube)
    return cubes

#ngitung fitness
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

#crossover
def crossover(parent1, parent2, idx1, idx2):
    n = len(parent1)
    child1, child2 = parent1.copy(), parent2.copy()
    i1, j1, k1 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)
    i2, j2, k2 = random.randint(0, n-1), random.randint(0, n-1), random.randint(0, n-1)

    child1[i1, j1, k1], child2[i2, j2, k2] = parent1[i2, j2, k2], parent2[i1, j1, k1]
    child2[i1, j1, k1], child1[i2, j2, k2] = parent2[i2, j2, k2], parent1[i1, j1, k1]
    print(f"Crossover antara kubus indeks {idx1} (parent1) dan {idx2} (parent2) di posisi ({i1}, {j1}, {k1}) dan ({i2}, {j2}, {k2}).")
    return child1, child2

#mutation
def mutation(cube, mutation_rate=0.05):
    num_swaps = int(125 * mutation_rate)
    for _ in range(num_swaps):
        i1, j1, k1 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        i2, j2, k2 = random.randint(0, 4), random.randint(0, 4), random.randint(0, 4)
        cube[i1, j1, k1], cube[i2, j2, k2] = cube[i2, j2, k2], cube[i1, j1, k1]
        print(f"Mutasi pada kubus di posisi ({i1}, {j1}, {k1}) ditukar dengan posisi ({i2}, {j2}, {k2})")
    return cube

def run_genetic_algorithm(num_iterations=100):
    cube = create_cube()
    different_cubes = generate_different_cubes(cube, num_cubes=100)
    priority_queue = [(fitness(c), idx) for idx, c in enumerate(different_cubes)]
    heapq.heapify(priority_queue)

    for i in range(num_iterations):
        elite_cubes = heapq.nsmallest(6, priority_queue)
        unique_elite_indices = set(cube[1] for cube in elite_cubes)
        print(f"Iterasi {i+1}: Kubus yang diambil sebagai elitisme (tanpa pengulangan): {unique_elite_indices}")
        
        num_crossover = len(priority_queue) // 2
        num_mutation = len(priority_queue) - num_crossover

        chosen_indices = choose_cube_by_random(num_crossover * 2, priority_queue)
        crossed_indices = set() 

        for j in range(0, len(chosen_indices), 2):
            idx1, idx2 = chosen_indices[j], chosen_indices[j + 1]
            cube1, cube2 = different_cubes[idx1], different_cubes[idx2]
            child1, child2 = crossover(cube1, cube2, idx1, idx2)

            different_cubes.append(child1)
            different_cubes.append(child2)

            child1_idx = len(different_cubes) - 2
            child2_idx = len(different_cubes) - 1

            crossed_indices.update([child1_idx, child2_idx])

            heapq.heappush(priority_queue, (fitness(child1), child1_idx))
            heapq.heappush(priority_queue, (fitness(child2), child2_idx))

        available_indices = [idx for idx in range(len(different_cubes)) if idx not in crossed_indices]
        mutate_indices = random.sample(available_indices, num_mutation)

        for idx in mutate_indices:
            print(f"Mutasi dilakukan pada kubus dengan indeks {idx}")
            different_cubes[idx] = mutation(different_cubes[idx])
            heapq.heappush(priority_queue, (fitness(different_cubes[idx]), idx))

        unique_priority_queue = {cube[1]: cube for cube in heapq.nsmallest(44, priority_queue)}
        unique_priority_queue.update({idx: cube for cube, idx in elite_cubes if idx not in unique_priority_queue})

        priority_queue = list(unique_priority_queue.values())
        heapq.heapify(priority_queue)

        current_generation_indices = [cube[1] for cube in priority_queue]
        print(f"Iterasi {i+1}: Fitness terbaik saat ini = {priority_queue[0][0]}")
        print(f"Indeks kubus di generasi {i+1}: {current_generation_indices}")

    best_fitness, best_idx = priority_queue[0]
    return different_cubes[best_idx], best_fitness

best_cube, best_fitness = run_genetic_algorithm(100)
print("\nKubus Terbaik:")
print(best_cube)
print("Nilai Fitness Terbaik:", best_fitness)