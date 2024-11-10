using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using Random = UnityEngine.Random;

public class main : MonoBehaviour
{
    public static int SIZE = 5;
    public static int SIZE3 = SIZE * SIZE * SIZE;
    public static int SUM = SIZE3 * (SIZE3 + 1) / 2;
    public static int MN = SUM / (SIZE3 / SIZE);

    public GameObject CubeGameObject;
    private cube _cube;
    
    public void Start() {
        _cube = CubeGameObject.GetComponent<cube>();
    }

    public static int ObjectiveFunction(int[,,] v) {
        int ret = 0;
        for (int i = 0; i < SIZE; ++i) {
            for (int j = 0; j < SIZE; ++j) {
                int temp1 = 0, temp2 = 0, temp3 = 0;
                for (int k = 0; k < SIZE; ++k) {
                    temp1 += v[i, j, k];
                    temp2 += v[i, k, j];
                    temp3 += v[k, i, j];
                }
                ret += Math.Abs(MN - temp1) + Math.Abs(MN - temp2) + Math.Abs(MN - temp3);
            }
        }

        // Plane Diagonal 1
        for (int i = 0; i < SIZE; ++i)
        {
            int temp1 = 0, temp2 = 0, temp3 = 0;
            for (int j = 0; j < SIZE; ++j)
            {
                temp1 += v[i, j, j];
                temp2 += v[j, j, i];
                temp3 += v[j, i, j];
            }
            ret += Math.Abs(MN - temp1) + Math.Abs(MN - temp2) + Math.Abs(MN - temp3);
        }

        // Plane Diagonal 2
        for (int i = 0; i < SIZE; ++i)
        {
            int temp1 = 0, temp2 = 0, temp3 = 0;
            for (int j = 0; j < SIZE; ++j)
            {
                temp1 += v[i, j, j];
                temp2 += v[j, j, i];
                temp3 += v[j, i, j];
            }
            ret += Math.Abs(MN - temp1) + Math.Abs(MN - temp2) + Math.Abs(MN - temp3);
        }

        // Cube Diagonal
        for (int i = 0; i < SIZE; ++i)
        {
            int temp1 = 0, temp2 = 0, temp3 = 0, temp4 = 0;
            for (int j = 0; j < SIZE; ++j)
            {
                temp1 += v[j, j, j];
                temp2 += v[j, j, SIZE - 1 - j];
                temp3 += v[j, SIZE - 1 - j, j];
                temp4 += v[SIZE - 1 - j, j, j];
            }
            ret += Math.Abs(MN - temp1) + Math.Abs(MN - temp2) + Math.Abs(MN - temp3) + Math.Abs(MN - temp4);
        }
        return ret;
    }

    public void ResetCube() {
        while (_cube.SeqIdx > 0) _cube.PrevSeq();
        _cube.Sequence.Clear();
    }
    
    public void RunSteepestAscent() {
        ResetCube();
        _cube.SetSequence(algo_sideway.Run(_cube.Values));
    }

    public void RunAnnealing() {
        ResetCube();
        _cube.SetSequence(algo_annealing.Run(_cube.Values));
    }
}