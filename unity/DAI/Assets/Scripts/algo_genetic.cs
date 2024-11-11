using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Unity.VisualScripting;
using Random = System.Random;
using UnityEngine;

public class algo_genetic : MonoBehaviour {
    private class child {
        public int[,,] State { get; set; }
        public List<int[]> Sequence { get; set; }
        public int Heuristic;

        public child(int[,,] values) {
            this.State = values;
            this.Sequence = new List<int[]>();
            this.Heuristic = main.ObjectiveFunction(this.State);
        }

        public child(child copy) {
            this.State = copy.State;
            this.Sequence = CopySeq(copy.Sequence);
            this.Heuristic = copy.Heuristic;
        }

        public child(child before, int[] seq) {
            this.State = before.State;
            (this.State[seq[0], seq[1], seq[2]], this.State[seq[3], seq[4], seq[5]]) = 
                (this.State[seq[3], seq[4], seq[5]], this.State[seq[0], seq[1], seq[2]]);
            this.Heuristic = main.ObjectiveFunction(this.State);
            this.Sequence = CopySeq(before.Sequence);
            this.Sequence.Add(new int[] {seq[0], seq[1], seq[2], seq[3], seq[4], seq[5], this.Heuristic});
        }

        private List<int[]> CopySeq(List<int[]> seq) {
            List<int[]> ret = new List<int[]>();
            for (int i = 0; i < seq.Count; ++i) {
                ret.Add((int[])seq[i].Clone());
            }

            return ret;
        }
    }
    
    private static int MN = main.MN;
    private static int SIZE = main.SIZE;
    private static int SIZE3 = main.SIZE3;

    static child ChooseCubeByRandom(List<child> cubes) {
        List<int> ranges = new List<int>();
        int maxH = 0;
        for (int i = 0; i < cubes.Count; ++i) if (cubes[i].Heuristic > maxH) maxH = cubes[i].Heuristic;
        
        ranges.Add(maxH - cubes[0].Heuristic);
        for (int i = 1; i < cubes.Count; ++i) {
            ranges.Add(ranges[i - 1] + (maxH - cubes[0].Heuristic));
        }

        int maxval = ranges[cubes.Count - 1];
        Random rand = new Random();
        double val = rand.Next(maxval);

        for (int i = 0; i < cubes.Count(); ++i) {
            if (val <= ranges[i]) return cubes[i];
        }

        return cubes[0];
    }

    static (child, child) Crossover(child parent1, child parent2) {
        child child1 = new child(parent1, parent2.Sequence.Last());
        child child2 = new child(parent2, parent1.Sequence.Last());
        
        return (child1, child2);
    }

    static child Mutation(child cube) {
        Random rand = new Random();
        int i1 = rand.Next(5), j1 = rand.Next(5), k1 = rand.Next(5);
        int i2 = rand.Next(5), j2 = rand.Next(5), k2 = rand.Next(5);
        
        child ret = new child(cube, new[] { i1, j1, k1, i2, j2, k2 });
        return ret;
    }

    static List<child> Clone(List<child> source) {
        List<child> target = new List<child>();
        for (int i = 0; i < source.Count; ++i) {
            child childCopy = new child(source[i]);
            target.Add(childCopy);
        }
        return target;
    }

    public static List<int[]> Run(int[,,] values, int population = 100, int generation = 500) {
        List<child> lastPopulation = new List<child>();
        List<child> currentPopulation = new List<child>();
        child initial = new child(values);
        for (int i = 0; i < population; ++i) {
            lastPopulation.Add(Mutation(initial));
        }

        for (int g = 0; g < generation; ++g) {
            // Outputs 55% of the children
            for (int i = 0; i < Mathf.RoundToInt(population * 0.55f); ++i) {
                child current = Mutation(ChooseCubeByRandom(lastPopulation));
                currentPopulation.Add(current);
            }

            // Outputs 40% of the children
            for (int i = 0; i < Mathf.RoundToInt(population * 0.2f); ++i) {
                child parent1 = ChooseCubeByRandom(lastPopulation);
                child parent2 = ChooseCubeByRandom(lastPopulation);

                (child, child) children = Crossover(parent1, parent2);
                currentPopulation.Add(children.Item1);
                currentPopulation.Add(children.Item2);
            }
            
            // Outputs 5% of the children
            for (int i = 0; i < Mathf.RoundToInt(population * 0.05f); ++i) {
                child current = ChooseCubeByRandom(lastPopulation);
                currentPopulation.Add(current);
            }
            
            lastPopulation.Clear();
            lastPopulation = Clone(currentPopulation);
            currentPopulation.Clear();
        }

        int bestHeuristic = Int32.MaxValue;
        int bestIdx = 0;
        for (int i = 0; i < lastPopulation.Count; ++i) {
            if (lastPopulation[i].Heuristic < bestHeuristic) {
                bestHeuristic = lastPopulation[i].Heuristic;
                bestIdx = i;
            }
        }

        return lastPopulation[bestIdx].Sequence;
    }
}
