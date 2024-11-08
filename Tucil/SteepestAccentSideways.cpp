#include <bits/stdc++.h>
#include <random>
using namespace std;

int totalCost(int m[5][5][5], int mn) {
    int ret = 0;
    int size = 5;

    // Horzontal and vetical
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            int temp1 = 0, temp2 = 0, temp3 = 0;
            for (int k = 0; k < size; ++k) {
                temp1 += m[i][j][k];
                temp2 += m[i][k][j];
                temp3 += m[k][i][j];
            }
            ret += abs(mn - temp1) + abs(mn - temp2) + abs(mn - temp3);
        }
    }

    // Plane Diagonal 1
    for (int i = 0; i < size; ++i) {
        int temp1 = 0, temp2 = 0, temp3 = 0;
        for (int j = 0; j < size; ++j) {
            temp1 += m[i][j][j];
            temp2 += m[j][j][i];
            temp3 += m[j][i][j];
        }
        ret += abs(mn - temp1) + abs(mn - temp2) + abs(mn - temp3);
    }

    // Plane Diagonal 2
    for (int i = 0; i < size; ++i) {
        int temp1 = 0, temp2 = 0, temp3 = 0;
        for (int j = 0; j < size; ++j) {
            temp1 += m[i][j][j];
            temp2 += m[j][j][i];
            temp3 += m[j][i][j];
        }
        ret += abs(mn - temp1) + abs(mn - temp2) + abs(mn - temp3);
    }

    // Cube Diagonal
    for (int i = 0; i < size; ++i) {
        int temp1 = 0, temp2 = 0, temp3 = 0, temp4 = 0;
        for (int j = 0; j < size; ++j) {
            temp1 += m[j][j][j];
            temp2 += m[j][j][4 - j];
            temp3 += m[j][4 - j][j];
            temp4 += m[4 - j][j][j];
        }
        ret += abs(mn - temp1) + abs(mn - temp2) + abs(mn - temp3) + abs(mn - temp4);
    }

    return ret;
}

int swapCost(int m[5][5][5], int mn, int i0, int j0, int k0, int i1, int j1, int k1) {
    // Cloning the array
    const int size = 5;
    int clone[size][size][size];
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            for (int k = 0 ; k< size; ++k) {
                clone[i][j][k] = m[i][j][k];
            }
        }
    }

    // Swapping the element
    clone[i0][j0][k0] = m[i1][j1][k1];
    clone[i1][j1][k1] = m[i0][j0][k0];

    // Calculating the difference
    int ret = totalCost(clone, mn);
    return ret;
}

int r() { return rand() % 5; }

int main() {
    const int SIZE = 5;
    const int SIZE3 = SIZE * SIZE * SIZE;
    const int SUM = SIZE3 * (SIZE3 + 1) / 2;
    const int MN = SUM / (SIZE3 / SIZE);
    const int TRIES = 500;


    // Randomizing the initial state
    vector<int> pool;
    int cube[SIZE][SIZE][SIZE];
    for (int i = 1; i <= SIZE3; i ++) {
        pool.push_back(i);
    }
    auto rng = default_random_engine();
    int n; cin >> n;
    for (int i = 0; i < SUM; i++) shuffle(pool.begin(), pool.end(), rng);

    // Filling the cube
    for (int i = 0; i < SIZE; ++i) {
        for (int j = 0; j < SIZE; ++j) {
            for (int k = 0; k < SIZE; ++k) {
                cube[i][j][k] = pool.back();
                pool.pop_back();
            }
        }
    }

    int poinSebelumnya = 0;
    bool running = true;
    int t = 0;
    int stuck = 0;
    int stuckLimit = 10;

    // Objective Function
    while(running) {
        t ++;
        int i0, j0, k0;
        int i1, j1, k1;
        int minV = INT_MAX;
        for (int di = 0; di < SIZE; ++di) {
            for (int dj = 0; dj < SIZE; ++dj) {
                for (int dk = 0; dk < SIZE; ++dk) {

                    for (int ni = 0; ni < SIZE; ++ni) {
                        for (int nj = 0; nj < SIZE; ++nj) {
                            for (int nk = 0; nk < SIZE; ++nk) {
                                if (ni != di || nj != dj || nk != dk) {
                                    int v = swapCost(cube, MN, di, dj, dk, ni, nj, nk);
                                    if (v <= minV) {
                                        minV = v;
                                        i0 = di; j0 = dj; k0 = dk;
                                        i1 = ni; j1 = nj; k1 = nk;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        int temp = cube[i0][j0][k0];
        cube[i0][j0][k0] = cube[i1][j1][k1];
        cube[i1][j1][k1] = temp;

        cout << totalCost(cube, MN) << endl;
        if (poinSebelumnya == totalCost(cube, MN)) {
            stuck ++;
        }
        else stuck = 0;
        poinSebelumnya = totalCost(cube, MN);

        if (stuck > stuckLimit) {
            cout << "Search berhenti pada " << (t - stuckLimit) << " iterasi dengan sisa cost " << poinSebelumnya << endl;
            running = false;
        }
    }
}