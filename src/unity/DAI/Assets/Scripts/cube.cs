using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using TMPro;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Serialization;
using Random = UnityEngine.Random;

public class cube : MonoBehaviour {
    public GameObject digit;
    public TextMeshPro[,,] Digits;
    public int[,,] Values;
    public int scale = 100;
    public int basis;

    public List<int[]> Sequence;
    [FormerlySerializedAs("_seqIdx")] public int SeqIdx = 0;

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
        Sequence = new List<int[]>();
        _counter = counterObject.GetComponent<TextMeshProUGUI>();
        
        // testing
        List<int[]> tempx = new List<int[]>();
        tempx.Add(new int[] {0, 0, 0, 4, 4, 4, 1000});
        tempx.Add(new int[] {0, 1, 0, 2, 4, 4, 1001});
        tempx.Add(new int[] {0, 4, 0, 3, 4, 4, 1002});
        tempx.Add(new int[] {0, 0, 2, 0, 4, 0, 1003});
        tempx.Add(new int[] {1, 0, 0, 4, 4, 2, 1004});
        tempx.Add(new int[] {3, 0, 0, 2, 4, 4, 1005});
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
        int[] array = new int[n];
        for (int i = 0; i < n; i++) {
            array[i] = i + 1;
        }

        for (int i = 0; i < n; i++) {
            int randomIndex = Random.Range(i, n);
            (array[i], array[randomIndex]) = (array[randomIndex], array[i]);
        }

        return array;
    }

    public void SetSequence(List<int[]> seq) {
        Sequence = seq;
        UpdateText();
    }

    void Swap(int i0, int j0, int k0, int i1, int j1, int k1) {
        ResetColor();
        (Values[i0, j0, k0], Values[i1, j1, k1]) = (Values[i1, j1, k1], Values[i0, j0, k0]);
        Digits[i0, j0, k0].text = Values[i0, j0, k0].ToString();
        Digits[i1, j1, k1].text = Values[i1, j1, k1].ToString();
        if (SeqIdx >= 0) {
            Digits[i0, j0, k0].color = Color.green;
            Digits[i1, j1, k1].color = Color.green;
        }
    }

    void ResetColor() {
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                for (int k = 0; k < 5; k++) {
                    Digits[i, j, k].color = Color.white;
                }
            }
        }
    }

    public void DoSeq() {
        int i0, j0, k0, i1, j1, k1;
        int[] currentSeq = Sequence[SeqIdx];
        i0 = currentSeq[0]; j0 = currentSeq[1]; k0 = currentSeq[2];
        i1 = currentSeq[3]; j1 = currentSeq[4]; k1 = currentSeq[5];
        
        Swap(i0, j0, k0, i1, j1, k1);
    }
    
    public void NextSeq() {
        if (SeqIdx < Sequence.Count) {
            DoSeq();
            SeqIdx++;
        }
        UpdateText();
    }

    public void PrevSeq() {
        if (SeqIdx > 0) {
            SeqIdx--;
            DoSeq();
        }
        UpdateText();
    }

    private void UpdateText() {
        _counter.text = SeqIdx.ToString() + "/" + Sequence.Count.ToString();
    }
}
