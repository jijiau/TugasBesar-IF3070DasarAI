using System;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using UnityEngine;
using Random = System.Random;

public class algo_annealing : MonoBehaviour {
    private static int MN = main.MN;
    private static int SIZE = main.SIZE;
    private static int SIZE3 = main.SIZE3;

    private static int[] _currentSeq;

    private static int[,,] GenerateRandomNeighbor(int[,,] state)
    {
        int[,,] neighbor = (int[,,])state.Clone();
        Random random = new Random();
        int i0 = random.Next(SIZE); int j0 = random.Next(SIZE); int k0 = random.Next(SIZE);
        int i1 = random.Next(SIZE); int j1 = random.Next(SIZE); int k1 = random.Next(SIZE);
        (neighbor[i0, j0, k0], neighbor[i1, j1, k1]) = (neighbor[i1, j1, k1], neighbor[i0, j0, k0]);
        
        _currentSeq = new[] { i0, j0, k0, i1, j1, k1, main.ObjectiveFunction(neighbor)};
        return neighbor;
    }

    public static List<int[]> Run(int[,,] values, double initialTemp = 1000, double coolingRate = 0.999,
        double minTemp = 0.001) {
        List<int[]> sequences = new List<int[]>();
        int[,,] currentState = (int[,,])values.Clone();
        double currentValue = main.ObjectiveFunction(currentState);
        double temperature = initialTemp;
        var random = new Random();

        while (temperature > minTemp) {
            int[,,] neighbor = GenerateRandomNeighbor(currentState);
            double neighborValue = main.ObjectiveFunction(neighbor);

            double deltaE = currentValue - neighborValue;
            if (deltaE > 0 || Math.Exp(Math.Min(deltaE / temperature, 700)) > random.NextDouble()) {
                currentState = neighbor;
                currentValue = neighborValue;
                sequences.Add(_currentSeq);
            }

            temperature *= coolingRate;
        }

        return sequences;
    }
}
