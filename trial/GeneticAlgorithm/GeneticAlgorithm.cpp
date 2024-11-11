#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <climits>

#define CUBE_SIZE 5
#define MAGIC_NUMBER 315
#define MUTATION_RATE 0.05

using namespace std;

// Fungsi untuk menghitung fitness
int fitness(const vector<vector<vector<int> > >& cube) {
    int total_difference = 0;

    // Menghitung baris, kolom, tiang
    for (int i = 0; i < CUBE_SIZE; i++) {
        for (int j = 0; j < CUBE_SIZE; j++) {
            int row_sum = 0, col_sum = 0, pillar_sum = 0;
            for (int k = 0; k < CUBE_SIZE; k++) {
                row_sum += cube[i][j][k];
                col_sum += cube[i][k][j];
                pillar_sum += cube[k][i][j];
            }
            total_difference += (row_sum - MAGIC_NUMBER) * (row_sum - MAGIC_NUMBER);
            total_difference += (col_sum - MAGIC_NUMBER) * (col_sum - MAGIC_NUMBER);
            total_difference += (pillar_sum - MAGIC_NUMBER) * (pillar_sum - MAGIC_NUMBER);
        }
    }

    // Menghitung diagonal ruang
    int diag_3d_1 = 0, diag_3d_2 = 0, diag_3d_3 = 0, diag_3d_4 = 0;
    for (int j = 0; j < CUBE_SIZE; j++) {
        diag_3d_1 += cube[j][j][j];
        diag_3d_2 += cube[j][j][CUBE_SIZE - 1 - j];
        diag_3d_3 += cube[j][CUBE_SIZE - 1 - j][j];
        diag_3d_4 += cube[CUBE_SIZE - 1 - j][j][j];
    }
    total_difference += (diag_3d_1 - MAGIC_NUMBER) * (diag_3d_1 - MAGIC_NUMBER);
    total_difference += (diag_3d_2 - MAGIC_NUMBER) * (diag_3d_2 - MAGIC_NUMBER);
    total_difference += (diag_3d_3 - MAGIC_NUMBER) * (diag_3d_3 - MAGIC_NUMBER);
    total_difference += (diag_3d_4 - MAGIC_NUMBER) * (diag_3d_4 - MAGIC_NUMBER);

    return total_difference;
}

// Fungsi crossover
void crossover(const vector<vector<vector<int> > >& parent1, const vector<vector<vector<int> > >& parent2,
               vector<vector<vector<int> > >& child1, vector<vector<vector<int> > >& child2) {
    for (int i = 0; i < CUBE_SIZE; i++) {
        for (int j = 0; j < CUBE_SIZE; j++) {
            for (int k = 0; k < CUBE_SIZE; k++) {
                if (rand() % 2) {
                    child1[i][j][k] = parent1[i][j][k];
                    child2[i][j][k] = parent2[i][j][k];
                } else {
                    child1[i][j][k] = parent2[i][j][k];
                    child2[i][j][k] = parent1[i][j][k];
                }
            }
        }
    }
}

// Fungsi mutasi
void mutation(vector<vector<vector<int> > >& cube) {
    for (int i = 0; i < CUBE_SIZE; i++) {
        for (int j = 0; j < CUBE_SIZE; j++) {
            for (int k = 0; k < CUBE_SIZE; k++) {
                if (static_cast<double>(rand()) / RAND_MAX < MUTATION_RATE) {
                    cube[i][j][k] = rand() % 125 + 1;
                }
            }
        }
    }
}

// Fungsi menjalankan algoritma genetika
void run_genetic_algorithm(int population_size, int num_iterations, vector<int>& best_cube, int& best_fitness) {
    vector<vector<vector<vector<int> > > > cubes(population_size, vector<vector<vector<int> > >(CUBE_SIZE, vector<vector<int> >(CUBE_SIZE, vector<int>(CUBE_SIZE))));
    vector<int> fitness_values(population_size);
    int total_fitness = 0;
    best_fitness = INT_MAX;

    for (int i = 0; i < population_size; i++) {
        for (int x = 0; x < CUBE_SIZE; x++) {
            for (int y = 0; y < CUBE_SIZE; y++) {
                for (int z = 0; z < CUBE_SIZE; z++) {
                    cubes[i][x][y][z] = rand() % 125 + 1;
                }
            }
        }

        fitness_values[i] = fitness(cubes[i]);
        total_fitness += fitness_values[i];

        if (fitness_values[i] < best_fitness) {
            best_fitness = fitness_values[i];
            for (int x = 0; x < CUBE_SIZE; x++)
                for (int y = 0; y < CUBE_SIZE; y++)
                    for (int z = 0; z < CUBE_SIZE; z++)
                        best_cube[x * CUBE_SIZE * CUBE_SIZE + y * CUBE_SIZE + z] = cubes[i][x][y][z];
        }
    }

    for (int iter = 0; iter < num_iterations; iter++) {
        int parent1_idx = rand() % population_size;
        int parent2_idx = rand() % population_size;
        vector<vector<vector<int> > > child1(CUBE_SIZE, vector<vector<int> >(CUBE_SIZE, vector<int>(CUBE_SIZE)));
        vector<vector<vector<int> > > child2(CUBE_SIZE, vector<vector<int> >(CUBE_SIZE, vector<int>(CUBE_SIZE)));

        crossover(cubes[parent1_idx], cubes[parent2_idx], child1, child2);
        mutation(child1);
        mutation(child2);

        int child1_fitness = fitness(child1);
        int child2_fitness = fitness(child2);

        if (child1_fitness < best_fitness) {
            best_fitness = child1_fitness;
            for (int x = 0; x < CUBE_SIZE; x++)
                for (int y = 0; y < CUBE_SIZE; y++)
                    for (int z = 0; z < CUBE_SIZE; z++)
                        best_cube[x * CUBE_SIZE * CUBE_SIZE + y * CUBE_SIZE + z] = child1[x][y][z];
        }
        if (child2_fitness < best_fitness) {
            best_fitness = child2_fitness;
            for (int x = 0; x < CUBE_SIZE; x++)
                for (int y = 0; y < CUBE_SIZE; y++)
                    for (int z = 0; z < CUBE_SIZE; z++)
                        best_cube[x * CUBE_SIZE * CUBE_SIZE + y * CUBE_SIZE + z] = child2[x][y][z];
        }
    }
}

// Fungsi utama
int main() {
    srand(time(0));

    int num_trials;
    cout << "Enter number of trials: ";
    cin >> num_trials;

    vector<int> population_sizes(num_trials);
    vector<int> iterations(num_trials);

    for (int i = 0; i < num_trials; i++) {
        do {
            cout << "Enter population size for trial " << i + 1 << ": ";
            cin >> population_sizes[i];
            if (population_sizes[i] <= 0) {
                cout << "Population size must be greater than zero. Please try again.\n";
            }
        } while (population_sizes[i] <= 0);

        do {
            cout << "Enter number of iterations for trial " << i + 1 << ": ";
            cin >> iterations[i];
            if (iterations[i] <= 0) {
                cout << "Number of iterations must be greater than zero. Please try again.\n";
            }
        } while (iterations[i] <= 0);
    }

    vector<int> global_best_cube(CUBE_SIZE * CUBE_SIZE * CUBE_SIZE);
    int global_best_fitness = INT_MAX;

    for (int p = 0; p < num_trials; p++) {
        cout << "\nRunning GA with Population Size: " << population_sizes[p] << ", Iterations: " << iterations[p] << endl;
        vector<int> best_cube(CUBE_SIZE * CUBE_SIZE * CUBE_SIZE);
        int best_fitness;
        run_genetic_algorithm(population_sizes[p], iterations[p], best_cube, best_fitness);

        cout << "\nBest cube found in this run:\n";
        for (int x = 0; x < CUBE_SIZE; x++) {
            for (int y = 0; y < CUBE_SIZE; y++) {
                for (int z = 0; z < CUBE_SIZE; z++) {
                    cout << best_cube[x * CUBE_SIZE * CUBE_SIZE + y * CUBE_SIZE + z] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }
        cout << "Best fitness value: " << best_fitness << endl;

        if (best_fitness < global_best_fitness) {
            global_best_fitness = best_fitness;
            global_best_cube = best_cube;
        }
    }

    cout << "\nGlobal Best Result\n";
    cout << "Global Best Cube:\n";
    for (int x = 0; x < CUBE_SIZE; x++) {
        for (int y = 0; y < CUBE_SIZE; y++) {
            for (int z = 0; z < CUBE_SIZE; z++) {
                cout << global_best_cube[x * CUBE_SIZE * CUBE_SIZE + y * CUBE_SIZE + z] << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
    cout << "Global Best Fitness Value: " << global_best_fitness << endl;

    return 0;
}
