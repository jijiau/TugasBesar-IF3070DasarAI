using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class algo_sideway : MonoBehaviour {
    private static int MN = main.MN;
    private static int SIZE = main.SIZE;
    private static int SIZE3 = main.SIZE3;

    public static int SwapCost(int[,,] values, int i0, int j0, int k0, int i1, int j1, int k1) {
        int[,,] clone = (int[,,])values.Clone();

        // Swapping the element
        int temp = clone[i0, j0, k0];
        clone[i0, j0, k0] = values[i1, j1, k1];
        clone[i1, j1, k1] = temp;

        // Calculating the difference
        return main.ObjectiveFunction(clone);
    }
    
    public static List<int[]> Run(int[,,] values) {
        List<int[]> sequences = new List<int[]>();
        int previousScore = 0;
        bool running = true;
        int t = 0;
        int stuck = 0;
        int stuckLimit = 10;

        // Objective Function
        while (running) {
            t++;
            int i0 = 0, j0 = 0, k0 = 0;
            int i1 = 0, j1 = 0, k1 = 0;
            int minV = int.MaxValue;
            for (int di = 0; di < SIZE; ++di) {
                for (int dj = 0; dj < SIZE; ++dj) {
                    for (int dk = 0; dk < SIZE; ++dk) {
                        for (int ni = 0; ni < SIZE; ++ni) {
                            for (int nj = 0; nj < SIZE; ++nj) {
                                for (int nk = 0; nk < SIZE; ++nk) {
                                    if (ni != di || nj != dj || nk != dk) {
                                        int v = SwapCost(values,  di, dj, dk, ni, nj, nk);
                                        if (v <= minV) {
                                            minV = v;
                                            i0 = di;
                                            j0 = dj;
                                            k0 = dk;
                                            i1 = ni;
                                            j1 = nj;
                                            k1 = nk;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            // Swapping the elements
            (values[i0, j0, k0], values[i1, j1, k1]) = (values[i1, j1, k1], values[i0, j0, k0]);
            sequences.Add(new int[] {i0, j0, k0, i1, j1, k1, minV});

            if (previousScore == main.ObjectiveFunction(values)) {
                stuck++;
            }
            else {
                stuck = 0;
            }
            previousScore = main.ObjectiveFunction(values);

            if (stuck > stuckLimit) {
                running = false;
            }
        }

        return sequences;
    }
}
