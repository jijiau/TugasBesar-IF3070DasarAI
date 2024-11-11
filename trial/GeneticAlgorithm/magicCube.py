import random
import numpy as np

#nyimpen magic number
def calculate_magic_number(n):
    return (n**4 + n) // 2

#nentuin fitness
def fitness(cube, magic_number):
    n = len(cube)
    fitness_score = 0

    for i in range(n):
        for j in range(n):
            if sum(cube[i][j, :]) == magic_number:
                fitness_score += 1
            if sum(cube[i, :, j]) == magic_number:
                fitness_score += 1
            if sum(cube[:, i, j]) == magic_number:
                fitness_score += 1

    if sum(cube[i, i, i] for i in range(n)) == magic_number:
        fitness_score += 1
    if sum(cube[i, i, n-i-1] for i in range(n)) == magic_number:
        fitness_score += 1
    if sum(cube[i, n-i-1, i] for i in range(n)) == magic_number:
        fitness_score += 1
    if sum(cube[n-i-1, i, i] for i in range(n)) == magic_number:
        fitness_score += 1

    return fitness_score

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

def genetic_algorithm(population_size, mutation_rate, max_generations, n=5):
    magic_number = calculate_magic_number(n)
    
    population = []
    for _ in range(population_size):
        cube = np.arange(1, n**3 + 1)
        np.random.shuffle(cube)
        population.append(cube.reshape((n, n, n)))

    for i in range(max_generations):
        fitness_scores = [fitness(cube, magic_number) for cube in population]
        
        selected_population = [population[i] for i in np.argsort(fitness_scores)[-population_size//2:]]
        
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child = crossover(parent1, parent2)
            
            if random.random() < mutation_rate:
                child = mutation(child)
            
            new_population.append(child)
        
        population = new_population
        
        max_fitness = max(fitness_scores)
        best_individual = population[fitness_scores.index(max_fitness)]
        if max_fitness == 4 * (n**2) + 4: 
            print(f"Solusi ditemukan di generasi {i + 1} dengan fitness = {max_fitness}")
            return best_individual 
    
    return best_individual

# Menjalankan algoritma
population_size = int(input("Ukuran populasi : "))
mutation_rate = float(input("Tingkat mutasi (0-1) : "))
max_generations = int(input("Maksimum generasi : "))

best_solution = genetic_algorithm(population_size, mutation_rate, max_generations)
print("Solusi terbaik : \n", best_solution)
