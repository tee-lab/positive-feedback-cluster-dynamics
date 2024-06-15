#define SIZE 100
#define EQUILIBRATION 1000

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

void landscape_update(int lattice[SIZE][SIZE], float p, float q);
void get_random_neighbour(int focal_i, int focal_j, int *neigh_i, int *neigh_j);
void get_pair_neighbour(int focal_i, int focal_j, int neigh_i, int neigh_j, int *pair_i, int *pair_j);
float get_density(int lattice[SIZE][SIZE]);

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

    float density = get_density(lattice);
    printf("\nDensity: %f\n", density);
}