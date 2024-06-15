#define SIZE 100
#define EQUILIBRATION 1000
#define SIMULATION 1000

#ifdef _WIN32
    #include <io.h>
#define access _access

#else
    #include <unistd.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "tdp_utils.c"
#include "cluster_dynamics.c"
#include "objects/dynamics_list.c"

int single_update(int lattice[SIZE][SIZE], float p, float q, int *changed_x, int *changed_y);
void landscape_update(int lattice[SIZE][SIZE], float p, float q);
void get_random_neighbour(int focal_i, int focal_j, int *neigh_i, int *neigh_j);
void get_pair_neighbour(int focal_i, int focal_j, int neigh_i, int neigh_j, int *pair_i, int *pair_j);
float get_density(int lattice[SIZE][SIZE]);

int single_update(int lattice[][SIZE], float p, float q, int *changed_x, int *changed_y) {
    int focal_i, focal_j;
    int neigh_i, neigh_j;
    int pair_i, pair_j;
    int updated = 0;
    float random_number;

    focal_i = rand() % SIZE;
    focal_j = rand() % SIZE;

    if (lattice[focal_i][focal_j] == 1) {
        get_random_neighbour(focal_i, focal_j, &neigh_i, &neigh_j);

        if (lattice[neigh_i][neigh_j] == 0) {
            random_number = (float) rand() / RAND_MAX;

            if (random_number < p) {
                lattice[neigh_i][neigh_j] = 1;
                *changed_x = neigh_i;
                *changed_y = neigh_j;
                updated = 1;
            }
            else {
                lattice[focal_i][focal_j] = 0;
                *changed_x = focal_i;
                *changed_y = focal_j;
                updated = 1;
            }
        }
        else {
            random_number = (float) rand() / RAND_MAX;
            if (random_number < q) {
                get_pair_neighbour(focal_i, focal_j, neigh_i, neigh_j, &pair_i, &pair_j);
                if (lattice[pair_i][pair_j] == 0) {    
                    *changed_x = pair_i;
                    *changed_y = pair_j;
                    updated = 1;
                }
                lattice[pair_i][pair_j] = 1;
            }
            else if (((float) rand() / RAND_MAX) < 1 - p) {
                lattice[focal_i][focal_j] = 0;
                *changed_x = focal_i;
                *changed_y = focal_j;
                updated = 1;
            }
        }
    }
    return updated;
}

int main(int argc, char *argv[]) {
    float p = atof(argv[1]);
    float q = atof(argv[2]);
    int simulation_index;

    if (argc == 4) {
        simulation_index = atoi(argv[3]);
    }
    else {
        simulation_index = 0;
    }

    srand(getpid()); 
    int lattice[SIZE][SIZE];
    dynamics_node *dynamics_list;

    int random_value;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            random_value = rand() % 2;
            lattice[i][j] = random_value;
        }
    }

    for (int i = 0; i < EQUILIBRATION; i++) {
        if (simulation_index == 0) {
            printf("\33[2K\r");
            printf("Equilibration: %f", (float) i * 100 / EQUILIBRATION);
        }
        landscape_update(lattice, p, q);
    }

    int changed_x, changed_y;
    int before[4], after[4];
    for (int i = 0; i < SIMULATION; i++) {
        if (simulation_index == 0) {
            printf("\33[2K\r");
            printf("Simulation: %f", (float) i * 100 / SIMULATION);
        }
        for (int j = 0; j < SIZE * SIZE; j++) {
            if (single_update(lattice, p, q, &changed_x, &changed_y)) {
                cluster_dynamics(lattice, changed_x, changed_y, before, after);
                dynamics_list = prepend_dynamics(dynamics_list, before, after);
            }
        }
    }

    print_dynamics_list(dynamics_list);
}