#define SIZE 256
#define UPDATES 1000

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "tdp_helpers.c"

void landscape_update(int lattice[][SIZE], float p, float q);
void get_random_neighbour(int focal_i, int focal_j, int *neigh_i, int *neigh_j);
void get_pair_neighbour(int focal_i, int focal_j, int neigh_i, int neigh_j, int *pair_i, int *pair_j);
float get_density(int lattice[][SIZE]);

void landscape_update(int lattice[][SIZE], float p, float q) {
    int focal_i, focal_j;
    int neigh_i, neigh_j;
    int pair_i, pair_j;
    float random_number;

    for (int i = 0; i < SIZE * SIZE; i++) {
        focal_i = rand() % SIZE;
        focal_j = rand() % SIZE;

        if (lattice[focal_i][focal_j] == 1) {
            get_random_neighbour(focal_i, focal_j, &neigh_i, &neigh_j);

            if (lattice[neigh_i][neigh_j] == 0) {
                random_number = (float) rand() / RAND_MAX;

                if (random_number < p) {
                    lattice[neigh_i][neigh_j] = 1;
                }
                else {
                    lattice[focal_i][focal_j] = 0;
                }
            }
            else {
                random_number = (float) rand() / RAND_MAX;
                if (random_number < q) {
                    get_pair_neighbour(focal_i, focal_j, neigh_i, neigh_j, &pair_i, &pair_j);
                    lattice[pair_i][pair_j] = 1;
                }
                else if (((float) rand() / RAND_MAX) < 1 - p) {
                    lattice[focal_i][focal_j] = 0;
                }
            }
        }
    }
}

int main(int argc, char *argv[]) {
    float p = atof(argv[1]);
    float q = atof(argv[2]);
    int simulation_index = atoi(argv[3]);

    srand(time(NULL)); 
    int lattice[SIZE][SIZE];

    int random_value;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            random_value = rand() % 2;
            lattice[i][j] = random_value;
        }
    }

    for (int i = 0; i < UPDATES; i++) {
        landscape_update(lattice, p, q);
    }

    float density = get_density(lattice);
    printf("Density: %f\n", density);
}