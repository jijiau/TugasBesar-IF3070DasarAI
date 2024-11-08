import random

#jumlah angka
def fitness(individual):
    return sum(individual)

#memilih individu dengan fitness paling besar
def weighted_random_choice(population, weights):
    total = sum(weights)
    pick = random.uniform(0, total)
    current = 0
    for i, weight in enumerate(weights):
        current += weight
        if current > pick:
            return population[i]

#crossover
def reproduce(parent1, parent2):
    n = len(parent1)
    c = random.randint(1, n - 1) 
    child = parent1[:c] + parent2[c:] 
    return child

#mutation
def mutate(child, mutation_rate=0.01):
    for i in range(len(child)):
        if random.random() < mutation_rate:
            child[i] = 1 - child[i]
    return child

def genetic_algorithm(population, fitness, mutation_rate=0.01, max_generations=100):
    for generation in range(max_generations):
        #ngitung bobot dari fitness
        weights = [fitness(individual) for individual in population]
        
        # Buat populasi baru
        new_population = []
        for _ in range(len(population)):
            #2 parents dengan bobot tertinggi
            parent1 = weighted_random_choice(population, weights)
            parent2 = weighted_random_choice(population, weights)
            
            #crossover
            child = reproduce(parent1, parent2)
            
            #mutation
            if random.random() < mutation_rate:
                child = mutate(child, mutation_rate)
            
            new_population.append(child)
        
        population = new_population

        #cek udah fit atau belum
        best_individual = max(population, key=fitness)
        if fitness(best_individual) >= max(weights):
            print(f"Generation {generation + 1}: Best fitness = {fitness(best_individual)}")
            return best_individual
    
    # kalau waktu abis, return populasi terbaik
    return max(population, key=fitness)

population_size = int(input())
chromosome_length = int(input())
mutation_rate = float(input())
max_generations = int(input())

population = [[random.randint(0, 1) for _ in range(chromosome_length)] for _ in range(population_size)]

best_individual = genetic_algorithm(population, fitness, mutation_rate, max_generations)
print("Best individual:", best_individual)
print("Fitness of best individual:", fitness(best_individual))

