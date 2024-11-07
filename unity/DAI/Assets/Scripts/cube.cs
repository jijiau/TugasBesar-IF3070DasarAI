using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.Serialization;
using Random = UnityEngine.Random;

public class cube : MonoBehaviour {
    public GameObject digit;
    public TextMeshPro[,,] Digits;
    public int[,,] Values;
    public int scale = 100;
    public int basis;

    private List<int[]> _sequence;
    private int _seqIdx = 0;

    public GameObject counterObject;
    private TextMeshProUGUI _counter;
    void Start() {
        Digits = new TextMeshPro[5,5,5];
        Values = new int[5, 5, 5];
        basis = (-scale * 2);
        for (int i = 0; i < 5; ++i) {
            for (int j = 0; j < 5; ++j) {
                for (int k = 0; k < 5; ++k) {
                    GameObject temp = Instantiate(digit, new Vector3(basis + (i * scale), basis + (j * scale), basis + (k * scale)), Quaternion.identity, transform);
                    Digits[i, j, k] = temp.GetComponent<TextMeshPro>();
                }
            }
        }

        Randomize();
        _sequence = new List<int[]>();
        _counter = counterObject.GetComponent<TextMeshProUGUI>();
        
        // testing
        List<int[]> tempx = new List<int[]>();
        tempx.Add(new int[] {0, 0, 0, 4, 4, 4});
        SetSequence(tempx);
    }

    public void Randomize() {
        int[] randomized = GenerateRandomPermutation(125);
        int idx = 0;
        for (int i = 0; i < 5; ++i) {
            for (int j = 0; j < 5; ++j) {
                for (int k = 0; k < 5; ++k) {
                    Values[i, j, k] = randomized[idx];
                    Digits[i, j, k].text = Values[i, j, k].ToString();
                    idx++;
                }
            }
        }
    }
    
    int[] GenerateRandomPermutation(int n)
    {
        // Step 1: Create an array of numbers from 1 to n
        int[] array = new int[n];
        for (int i = 0; i < n; i++)
        {
            array[i] = i + 1;
        }

        // Step 2: Shuffle the array
        for (int i = 0; i < n; i++)
        {
            int randomIndex = Random.Range(i, n); // Get a random index from i to n - 1
            // Swap elements at i and randomIndex
            (array[i], array[randomIndex]) = (array[randomIndex], array[i]);
        }

        return array;
    }


    public void SetSequence(List<int[]> seq) {
        _sequence = new List<int[]>();
        _seqIdx = 0;
        foreach (int[] arr in seq) {
            _sequence.Add(new int[6]);
            for (int i = 0; i < 6; ++i) {
                _sequence.Last()[i] = arr[i];
            }
        }
    }

    void Swap(int i0, int j0, int k0, int i1, int j1, int k1) {
        (Values[i0, j0, k0], Values[i1, j1, k1]) = (Values[i1, j1, k1], Values[i0, j0, k0]);
        Digits[i0, j0, k0].text = Values[i0, j0, k0].ToString();
        Digits[i1, j1, k1].text = Values[i1, j1, k1].ToString();
        Digits[i0, j0, k0].color = Color.green;
        Digits[i1, j1, k1].color = Color.green;
    }

    public void NextSeq() {
        if (_seqIdx < _sequence.Count) {
            int i0, j0, k0, i1, j1, k1;
            int[] currentSeq = _sequence[_seqIdx];
            i0 = currentSeq[0]; j0 = currentSeq[1]; k0 = currentSeq[2];
            i1 = currentSeq[3]; j1 = currentSeq[4]; k1 = currentSeq[5];
            
            Swap(i0, j0, k0, i1, j1, k1);
            _seqIdx++;
        }
        _counter.text = _seqIdx.ToString();
    }

    public void PrevSeq() {
        if (_seqIdx > 0) {
            _seqIdx--;
            int i0, j0, k0, i1, j1, k1;
            int[] currentSeq = _sequence[_seqIdx];
            i0 = currentSeq[0]; j0 = currentSeq[1]; k0 = currentSeq[2];
            i1 = currentSeq[3]; j1 = currentSeq[4]; k1 = currentSeq[5];
            Swap(i0, j0, k0, i1, j1, k1);
        }
        _counter.text = _seqIdx.ToString();
    }
}
