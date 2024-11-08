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
            ret += (abs(mn - temp1) * abs(mn - temp1))  + (abs(mn - temp2) * abs(mn - temp2)) + (abs(mn - temp3) * abs(mn - temp3));
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
        ret += (abs(mn - temp1) * abs(mn - temp1))  + (abs(mn - temp2) * abs(mn - temp2)) + (abs(mn - temp3) * abs(mn - temp3));
    }

    // Plane Diagonal 2
    for (int i = 0; i < size; ++i) {
        int temp1 = 0, temp2 = 0, temp3 = 0;
        for (int j = 0; j < size; ++j) {
            temp1 += m[i][j][j];
            temp2 += m[j][j][i];
            temp3 += m[j][i][j];
        }
        ret += (abs(mn - temp1) * abs(mn - temp1))  + (abs(mn - temp2) * abs(mn - temp2)) + (abs(mn - temp3) * abs(mn - temp3));
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
        ret += (abs(mn - temp1) * abs(mn - temp1))  + (abs(mn - temp2) * abs(mn - temp2)) + (abs(mn - temp3) * abs(mn - temp3)) + (abs(mn - temp4) * abs(mn - temp4)) ;
    }

    return ret;
}

int swapCost(int m[5][5][5], int mn, int i0, int j0, int k0, int i1, int j1, int k1) {
    // Cloning the array
    const int size = 5;
    int clone[size][size][size];
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            for (int k = 0 ; k < size; ++k) {
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
    const double initial_temperature = 1000;
    const double min_temperature = 1;
    const double cooling_rate = 0.999;

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

    int iteration = 0; 
    double current_temperature = initial_temperature;
    int current_cost = totalCost(cube, MN);
    int lowestValue = INT_MAX;

    // Array to store swap steps
    vector<vector<int>> swap_steps;

    while (current_temperature > min_temperature && current_cost > 0) {
        // Randomize the points
        int i0 = r(), j0 = r(), k0 = r();
        int i1 = r(), j1 = r(), k1 = r();

        int new_cost = swapCost(cube, MN, i0, j0, k0, i1, j1, k1);
        int cost_difference = new_cost - current_cost;

        if (cost_difference < 0) {
            current_cost = new_cost;
            int temp = cube[i0][j0][k0];
            cube[i0][j0][k0] = cube[i1][j1][k1];
            cube[i1][j1][k1] = temp;

            // Record the swap
            swap_steps.push_back({i0, j0, k0, i1, j1, k1});
        }
        else {
            double probability = exp(-cost_difference / current_temperature);
            if (rand() % 100 < (probability * 100)) {
                current_cost = new_cost;
                int temp = cube[i0][j0][k0];
                cube[i0][j0][k0] = cube[i1][j1][k1];
                cube[i1][j1][k1] = temp;

                // Record the swap
                swap_steps.push_back({i0, j0, k0, i1, j1, k1});
            }
        }
        current_temperature *= cooling_rate;
        iteration += 1;

        if (current_cost < lowestValue) lowestValue = current_cost;
    }


    // Output the swap steps
    cout << "Proses Swap:" << endl;
    for (const auto &step : swap_steps) {
        cout << "[" << step[0] << ", " << step[1] << ", " << step[2] 
             << "] ditukar dengan [" << step[3] << ", " << step[4] << ", " << step[5] << "]" << endl;
    }

    cout << "Iteration " << iteration << " dengan cost " << lowestValue << endl;
    
    cout << "Jumlah perubahan (swap) yang terjadi: " << swap_steps.size() << endl;
    

    return 0;
}
