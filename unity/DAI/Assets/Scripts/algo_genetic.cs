using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Random = System.Random;
using UnityEngine;

public class algo_genetic : MonoBehaviour
{
    private static int MN = main.MN;
    private static int SIZE = main.SIZE;
    private static int SIZE3 = main.SIZE3;
    static List<int[,,]> GenerateDifferentCubes(int[,,] cube, int numCubes = 100) {
        List<int[,,]> cubes = new List<int[,,]>();
        Random rand = new Random();
        for (int n = 0; n < numCubes; n++) {
            int[,,] newCube = (int[,,])cube.Clone();
            var indices = Enumerable.Range(0, 125).OrderBy(x => rand.Next()).ToList();
            for (int i = 0; i < 125; i++)
                newCube[i / 25, (i / 5) % 5, i % 5] = cube[indices[i] / 25, (indices[i] / 5) % 5, indices[i] % 5];
            cubes.Add(newCube);
        }
        return cubes;
    }

    static List<int> ChooseCubeByRandom(int numSelect, List<(int fitness, int index)> priorityQueue) {
        var fitnessValues = priorityQueue.Select(x => 1.0 / (x.fitness + 1e-6)).ToArray();
        double totalFitness = fitnessValues.Sum();
        var probabilities = fitnessValues.Select(f => f / totalFitness).ToArray();
        var random = new Random();
        var chosenIndices = new List<int>();

        for (int i = 0; i < numSelect; i++) {
            double target = random.NextDouble();
            double cumulative = 0.0;
            for (int j = 0; j < probabilities.Length; j++) {
                cumulative += probabilities[j];
                if (target <= cumulative) {
                    chosenIndices.Add(j);
                    break;
                }
            }
        }
        return chosenIndices;
    }

    static (int[,,], int[,,]) Crossover(int[,,] parent1, int[,,] parent2, int idx1, int idx2) {
        Random rand = new Random();
        int i1 = rand.Next(5), j1 = rand.Next(5), k1 = rand.Next(5);
        int i2 = rand.Next(5), j2 = rand.Next(5), k2 = rand.Next(5);

        var child1 = (int[,,])parent1.Clone();
        var child2 = (int[,,])parent2.Clone();

        child1[i1, j1, k1] = parent2[i2, j2, k2];
        child2[i2, j2, k2] = parent1[i1, j1, k1];

        return (child1, child2);
    }

    static int[,,] Mutation(int[,,] cube, double mutationRate = 0.05) {
        Random rand = new Random();
        int numSwaps = (int)(125 * mutationRate);
        for (int i = 0; i < numSwaps; i++) {
            int i1 = rand.Next(5), j1 = rand.Next(5), k1 = rand.Next(5);
            int i2 = rand.Next(5), j2 = rand.Next(5), k2 = rand.Next(5);

            (cube[i1, j1, k1], cube[i2, j2, k2]) = (cube[i2, j2, k2], cube[i1, j1, k1]);
        }
        return cube;
    }

    static void RunGeneticAlgorithm(int numIterations = 100) {
        var differentCubes = GenerateDifferentCubes(cube, 100);
        var priorityQueue = new List<(int fitness, int index)>();

        for (int i = 0; i < differentCubes.Count; i++)
        {
            priorityQueue.Add((Fitness(differentCubes[i]), i));
        }
        priorityQueue = priorityQueue.OrderBy(x => x.fitness).ToList();

        for (int iteration = 1; iteration <= numIterations; iteration++)
        {
            var eliteCubes = priorityQueue.Take(6).ToList();
            var eliteIndices = eliteCubes.Select(c => c.index).ToHashSet();
            var chosenIndices = ChooseCubeByRandom(priorityQueue.Count / 2, priorityQueue);
            var crossedIndices = new HashSet<int>();

            for (int j = 0; j < chosenIndices.Count - 1; j += 2)
            {
                int idx1 = chosenIndices[j], idx2 = chosenIndices[j + 1];
                var (child1, child2) = Crossover(differentCubes[idx1], differentCubes[idx2], idx1, idx2);

                differentCubes.Add(child1);
                differentCubes.Add(child2);

                priorityQueue.Add((Fitness(child1), differentCubes.Count - 2));
                priorityQueue.Add((Fitness(child2), differentCubes.Count - 1));

                crossedIndices.Add(differentCubes.Count - 2);
                crossedIndices.Add(differentCubes.Count - 1);
            }

            var availableIndices = Enumerable.Range(0, differentCubes.Count).Where(idx => !crossedIndices.Contains(idx)).ToList();
            var mutateIndices = availableIndices.OrderBy(_ => rand.Next()).Take(priorityQueue.Count - crossedIndices.Count).ToList();

            foreach (int idx in mutateIndices)
            {
                Console.WriteLine($"Mutasi dilakukan pada kubus dengan indeks {idx}");
                differentCubes[idx] = Mutation(differentCubes[idx]);
                priorityQueue.Add((Fitness(differentCubes[idx]), idx));
            }

            priorityQueue = priorityQueue.OrderBy(x => x.fitness).Take(44).ToList();
            Console.WriteLine($"Iterasi {iteration}: Fitness terbaik saat ini = {priorityQueue.First().fitness}");
        }

        var best = priorityQueue.First();
        Console.WriteLine("\nKubus Terbaik:");
        PrintCube(differentCubes[best.index]);
        Console.WriteLine("Nilai Fitness Terbaik: " + best.fitness);
    }
}
