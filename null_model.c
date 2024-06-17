#define SIZE 100
#define EQUILIBRATION 1000
#define SIMULATION 1000

#ifdef _WIN32
    #include <io.h>
#define access _access

#else
    #include <unistd.h>
#endif

#define min(a, b) ((a) < (b) ? (a) : (b))
#define max(a, b) ((a) > (b) ? (a) : (b))

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>
#include "cluster_dynamics.c"
#include "objects/dynamics_list.c"

void landscape_update(int lattice[SIZE][SIZE], float m, float r);

int single_update(int lattice[SIZE][SIZE], float m, float r, int *changed_x, int *changed_y) {
    int random_i, random_j;
    float random_number;
    int updated = 0;

    for (int i = 0; i < SIZE * SIZE; i++) {
        random_i = rand() % SIZE;
        random_j = rand() % SIZE;

        if (lattice[random_i][random_j] == 0) {
            random_number = (float) rand() / RAND_MAX;

            if (random_number < r) {
                lattice[random_i][random_j] = 1;
                *changed_x = random_i;
                *changed_y = random_j;
                updated = 1;
            }
        }
        else {
            random_number = (float) rand() / RAND_MAX;

            if (random_number < m) {
                lattice[random_i][random_j] = 0;
                *changed_x = random_i;
                *changed_y = random_j;
                updated = 1;
            }
        }
    }
    return updated;
}

int main(int argc, char *argv[]) {
    float req_density = atof(argv[1]);
    int simulation_index = atoi(argv[2]);
    char file_root[200];
    strcpy(file_root, argv[3]);

    float m, m_by_r, r;
    m = 1 - req_density;
    m_by_r = (1 / req_density) - 1;
    r = m / m_by_r;

    srand(getpid()); 
    int lattice[SIZE][SIZE];
    dynamics_node *dynamics_list;

    if (simulation_index == 0) {
        printf("---> Simulating f = %f <---\n", req_density);
    }

    float random_value;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            random_value =  (float) rand() / RAND_MAX;
            if (random_value < req_density) {
                lattice[i][j] = 1;
            }
            else {
                lattice[i][j] = 0;
            }
        }
    }

    if (simulation_index == 0) {
        printf("Equilibrating (takes a few seconds) ...\n");
    }
    for (int i = 0; i < EQUILIBRATION; i++) {
        landscape_update(lattice, m, r);
    }

    if (SIMULATION) {
        int changed_x, changed_y;
        int before[4], after[4];
        for (int i = 0; i < SIMULATION; i++) {
            if (simulation_index == 0) {
                printf("(%f) Simulating update %d of %d\n", req_density, i + 1, SIMULATION);
            }
            for (int j = 0; j < SIZE * SIZE; j++) {
                if (single_update(lattice, m, r, &changed_x, &changed_y)) {
                    cluster_dynamics(lattice, changed_x, changed_y, before, after);
                    dynamics_list = prepend_dynamics(dynamics_list, before, after);
                }
            }
        }
    }

     // save lattice
    char landscape_file_name[200] = {'\0'};
    strcat(landscape_file_name, file_root);
    strcat(landscape_file_name, "landscape.txt");

    FILE *landscape_file = fopen(landscape_file_name, "w");
    if (landscape_file == NULL) {
        printf("Error opening landscape file!\n");
        exit(1);
    }

    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            fprintf(landscape_file, "%d ", lattice[i][j]);  
        }
        fprintf(landscape_file, "\n");
    }
    fclose(landscape_file);
    
    // save dynamics
    char dynamics_file_name[200] = {'\0'};
    strcat(dynamics_file_name, file_root);
    strcat(dynamics_file_name, "dynamics.txt");

    FILE *dynamics_file = fopen(dynamics_file_name, "w");
    if (dynamics_file == NULL) {
        printf("Error opening dynamics file!\n");
        exit(1);
    }

    dynamics_node *current = dynamics_list;
    while (current != NULL) {
        for (int i = 0; i < 4; i++) {
            fprintf(dynamics_file, "%d ", current->before[i]);
        }
        fprintf(dynamics_file, ": ");
        for (int i = 0; i < 4; i++) {
            fprintf(dynamics_file, "%d ", current->after[i]);
        }
        fprintf(dynamics_file, "\n");
        current = current->next;
    }
    fclose(dynamics_file);
}

void landscape_update(int lattice[SIZE][SIZE], float m, float r) {
    int random_i, random_j;
    float random_number;

    for (int i = 0; i < SIZE * SIZE; i++) {
        random_i = rand() % SIZE;
        random_j = rand() % SIZE;

        if (lattice[random_i][random_j] == 0) {
            random_number = (float) rand() / RAND_MAX;

            if (random_number < r) {
                lattice[random_i][random_j] = 1;
            }
        }
        else {
            random_number = (float) rand() / RAND_MAX;

            if (random_number < m) {
                lattice[random_i][random_j] = 0;
            }
        }
    }
}