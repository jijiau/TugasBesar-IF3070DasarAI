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
    inverted_fitness_values = [1 / item[0] for item in priority_queue] 
    total_inverted_fitness = sum(inverted_fitness_values)

    ranges = []
    lower_bound = 0
    for inverted_fitness in inverted_fitness_values:
        percentage = (inverted_fitness / total_inverted_fitness) * 100
        upper_bound = lower_bound + percentage
        ranges.append((lower_bound, upper_bound))
        lower_bound = upper_bound

    chosen_indices = []
    for _ in range(randomize_count):
        rand_number = random.uniform(0, 100)
        for idx, (lower, upper) in enumerate(ranges):
            if lower <= rand_number <= upper:
                chosen_indices.append(idx) 
                break

    return chosen_indices

def run_genetic_algorithm(num_iterations=100):
    priority_queue = []
    cube = create_cube()
    different_cubes = generate_different_cubes(cube, num_cubes=100)

    # for idx, c in enumerate(different_cubes, 1):
    #     print(f"\nKubus {idx}:")
    #     print(c) 

    for idx, c in enumerate(different_cubes):
        fit = fitness(c)
        heapq.heappush(priority_queue, (fit, c)) 

        # print("Priority queue: ")
        # print(priority_queue)
    
        for i in range(num_iterations):
            fitness_values = [item[0] for item in priority_queue]
            total_fitness = sum(fitness_values)

            chosen_indices = choose_cube_by_random(100, priority_queue)
        
        print("Chosen indices: ")
        print(chosen_indices)

        for j in range(0, len(chosen_indices) - 1, 2):
            idx1, idx2 = chosen_indices[j], chosen_indices[j + 1]
            fitness1, cube1 = priority_queue[idx1]
            fitness2, cube2 = priority_queue[idx2]

            random_val1 = random.choice(cube1.flatten())
            random_val2 = random.choice(cube2.flatten())

            # Cari posisi kedua angka di dalam kubus
            pos1 = np.argwhere(cube1 == random_val1)[0]
            pos2 = np.argwhere(cube2 == random_val2)[0]

            # Lakukan pertukaran posisi
            cube1[tuple(pos1)], cube2[tuple(pos2)] = cube2[tuple(pos2)], cube1[tuple(pos1)]

            # Hitung fitness baru dan masukkan kembali ke priority queue
            new_fitness1 = fitness(cube1)
            new_fitness2 = fitness(cube2)

            # Update priority queue dengan nilai fitness baru
            priority_queue[idx1] = (new_fitness1, cube1)
            priority_queue[idx2] = (new_fitness2, cube2)

        # Ambil 50 kubus terbaik dari generasi sebelumnya
        best_cubes_from_last_gen = heapq.nsmallest(50, priority_queue)

        # Gabungkan generasi baru dengan 50 kubus terbaik
        priority_queue = best_cubes_from_last_gen + priority_queue[len(best_cubes_from_last_gen):]

        # Atur ulang priority queue
        heapq.heapify(priority_queue)

        best_fitness, best_cube = priority_queue[0]
        print(f"Iterasi {i+1}: Fitness terbaik saat ini = {best_fitness}")

    return best_cube, best_fitness


    for i in range(num_iterations):
        best_fitness, best_cube = heapq.heappop(priority_queue)
        print(f"Iterasi {i+1}: Fitness terbaik saat ini = {best_fitness}")
        

        
        heapq.heappush(priority_queue, (best_fitness, best_cube))  

    return best_cube, best_fitness


best_cube, best_fitness = run_genetic_algorithm()
print("\nKubus Terbaik:")
print(best_cube)
print("Nilai Fitness Terbaik:", best_fitness)
