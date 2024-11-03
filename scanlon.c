#define SIZE 256
#define EQUILIBRATION 500
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

int single_update(int lattice[SIZE][SIZE], float carrying_capacity, int radius, int immediacy, int *changed_x, int *changed_y);
void landscape_update(int lattice[SIZE][SIZE], float carrying_capacity, int radius, int immediacy);
float get_forest_cover(int rainfall);
float get_neigh_density(int lattice[SIZE][SIZE], int i, int j, int radius, int immediacy);

int single_update(int lattice[SIZE][SIZE], float carrying_capacity, int radius, int immediacy, int *changed_x, int *changed_y) {
    float current_density, rho;
    int random_i, random_j;
    float random_number, prob;
    int updated = 0;

    current_density = get_density(lattice);
    random_i = rand() % SIZE;
    random_j = rand() % SIZE;
    rho = get_neigh_density(lattice, random_i, random_j, radius, immediacy);

    if (lattice[random_i][random_j] == 0) {
        prob = rho + (carrying_capacity - current_density) / (1 - current_density);
        random_number = rand() / (float) RAND_MAX;

        if (random_number < prob) {
            lattice[random_i][random_j] = 1;
            updated = 1;
            *changed_x = random_i;
            *changed_y = random_j;
        }
    }
    else {
        prob = (1.0 - rho) + (current_density - carrying_capacity) / current_density;
        random_number = rand() / (float) RAND_MAX;

        if (random_number < prob) {
            lattice[random_i][random_j] = 0;
            updated = 1;
            *changed_x = random_i;
            *changed_y = random_j;
        }
    }
    return updated;
}

int main(int argc, char *argv[]) {
    int rainfall = atof(argv[1]);
    int simulation_index = atoi(argv[2]);
    char file_root[200];
    strcpy(file_root, argv[3]);

    int radius = 8;
    int immediacy = 24;
    float carrying_capacity = get_forest_cover(rainfall);

    srand(getpid()); 
    int lattice[SIZE][SIZE];
    dynamics_node *dynamics_list;

    if (simulation_index == 0) {
        printf("---> Simulating rainfall = %d <---\n", rainfall);
    }

    float random_value;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            random_value = rand() / (float) RAND_MAX;
            if (random_value < carrying_capacity) {
                lattice[i][j] = 1;
            }
            else {
                lattice[i][j] = 0;
            }
        }
    }

    for (int i = 0; i < EQUILIBRATION; i++) {
        if (simulation_index == 0) {
            printf("(%d) Equilibration step %d of %d\n", rainfall, i + 1, EQUILIBRATION);
        }
        landscape_update(lattice, carrying_capacity, radius, immediacy);
    }

    if (SIMULATION) {
        int changed_x, changed_y;
        int before[4], after[4];
        for (int i = 0; i < SIMULATION; i++) {
            if (simulation_index == 0) {
                printf("(%d) Simulating update %d of %d\n", rainfall, i + 1, SIMULATION);
            }
            for (int j = 0; j < SIZE * SIZE; j++) {
                if (single_update(lattice, carrying_capacity, radius, immediacy, &changed_x, &changed_y)) {
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

void landscape_update(int lattice[SIZE][SIZE], float carrying_capacity, int radius, int immediacy) {
    float current_density, rho;
    int random_i, random_j;
    float random_number, prob;

    for (int i = 0; i < SIZE * SIZE; i++) {
        current_density = get_density(lattice);
        random_i = rand() % SIZE;
        random_j = rand() % SIZE;
        rho = get_neigh_density(lattice, random_i, random_j, radius, immediacy);

        if (lattice[random_i][random_j] == 0) {
            prob = rho + (carrying_capacity - current_density) / (1 - current_density);
            random_number = rand() / (float) RAND_MAX;

            if (random_number < prob) {
                lattice[random_i][random_j] = 1;
            }
        }
        else {
            prob = (1.0 - rho) + (current_density - carrying_capacity) / current_density;
            random_number = rand() / (float) RAND_MAX;

            if (random_number < prob) {
                lattice[random_i][random_j] = 0;
            }
        }
    }
}

float get_neigh_density(int lattice[SIZE][SIZE], int i, int j, int radius, int immediacy) {
    int dx, dy;
    int neigh_i, neigh_j;
    float distance, weight;
    float normalization = 0;
    float density = 0;

    for (int a = i - radius; a < i + radius + 1; a++)
    {
        for (int b = j - radius; b < j + radius + 1; b++) {
            neigh_i = a;
            if (neigh_i < 0) {
                neigh_i += SIZE;
            }
            else if (neigh_i >= SIZE) {
                neigh_i -= SIZE;
            }
            neigh_j = b;
            if (neigh_j < 0) {
                neigh_j += SIZE;
            }
            else if (neigh_j >= SIZE) {
                neigh_j -= SIZE;
            }

            dx = abs(neigh_i - i) ? abs(neigh_i - i) > SIZE / 2 : SIZE - abs(neigh_i - i);
            dy = abs(neigh_j - j) ? abs(neigh_j - j) > SIZE / 2 : SIZE - abs(neigh_j - j);
            distance = sqrt(dx * dx + dy * dy);

            if (distance <= radius) {
                weight = 1.0 - ((float) radius / (float) immediacy);
                density += weight * (float) lattice[neigh_i][neigh_j];
                normalization += weight;
            }
        }
    }

    return density / normalization;
}

float get_forest_cover(int rainfall) {
    float slope = 0.0008588;
    float intercept = -0.1702;
    return max(slope * rainfall + intercept, 0);
}