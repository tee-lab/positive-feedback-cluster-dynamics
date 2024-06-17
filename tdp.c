#define SIZE 100
#define EQUILIBRATION 1000
#define SIMULATION 100

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

int single_update(int lattice[SIZE][SIZE], float p, float q, int *changed_x, int *changed_y);
void landscape_update(int lattice[SIZE][SIZE], float p, float q);
void get_random_neighbour(int focal_i, int focal_j, int *neigh_i, int *neigh_j);
void get_pair_neighbour(int focal_i, int focal_j, int neigh_i, int neigh_j, int *pair_i, int *pair_j);
float get_density(int lattice[SIZE][SIZE]);

int single_update(int lattice[SIZE][SIZE], float p, float q, int *changed_x, int *changed_y) {
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
    int simulation_index = atoi(argv[3]);
    char file_root[200];
    strcpy(file_root, argv[4]);

    srand(getpid()); 
    int lattice[SIZE][SIZE];
    dynamics_node *dynamics_list;

    if (simulation_index == 0) {
        printf("Simulating p = %f, q = %f\n", p, q);
    }

    int random_value;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            random_value = rand() % 2;
            lattice[i][j] = random_value;
        }
    }

    if (simulation_index == 0) {
        printf("Equilibrating (takes a few seconds) ...");
    }
    for (int i = 0; i < EQUILIBRATION; i++) {
        landscape_update(lattice, p, q);
    }

    if (SIMULATION) {
        int changed_x, changed_y;
        int before[4], after[4];
        for (int i = 0; i < SIMULATION; i++) {
            if (simulation_index == 0) {
                printf("Simulating update %d of %d\n", i + 1, SIMULATION);
            }
            for (int j = 0; j < SIZE * SIZE; j++) {
                if (single_update(lattice, p, q, &changed_x, &changed_y)) {
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

void landscape_update(int lattice[SIZE][SIZE], float p, float q) {
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

void get_random_neighbour(int focal_i, int focal_j, int *neigh_i, int *neigh_j) {
    int random_direction = rand() % 4;
    int i, j;

    switch (random_direction) {
        case 0:
            i = focal_i - 1;
            j = focal_j;
            break;
        case 1:
            i = focal_i + 1;
            j = focal_j;
            break;
        case 2:
            i = focal_i;
            j = focal_j - 1;
            break;
        case 3:
            i = focal_i;
            j = focal_j + 1;
            break;
    }

    if (i < 0) {
        i = SIZE - 1;
    } else if (i >= SIZE) {
        i = 0;
    }

    if (j < 0) {
        j = SIZE - 1;
    } else if (j >= SIZE) {
        j = 0;
    }

    *neigh_i = i;
    *neigh_j = j;
}

void get_pair_neighbour(int focal_i, int focal_j, int neigh_i, int neigh_j, int *pair_i, int *pair_j) {
    int random_direction = rand() % 6;
    int i, j;

    if (focal_i == neigh_i) {
        int j_left = min(focal_j, neigh_j);
        int j_right = max(focal_j, neigh_j);

        switch (random_direction) {
            case 0: // on top of left cell
                i = focal_i - 1;
                j = j_left;
                break;
            case 1: // on top of right cell
                i = focal_i - 1;
                j = j_right;
                break;
            case 2: // on right of right cell
                i = focal_i;
                j = j_right + 1;
                break;
            case 3: // on bottom of right cell
                i = focal_i + 1;
                j = j_right;
                break;
            case 4: // on bottom of left cell
                i = focal_i + 1;
                j = j_left;
                break;
            case 5: // on left of left cell
                i = focal_i;
                j = j_left - 1;
                break;
        }
    }
    else {
        int i_top = min(focal_i, neigh_i);
        int i_bottom = max(focal_i, neigh_i);

        switch(random_direction) {
            case 0: // on top of top cell
                i = i_top - 1;
                j = focal_j;
                break;
            case 1: // on right of top cell
                i = i_top;
                j = focal_j + 1;
                break;
            case 2: // on right of bottom cell
                i = i_bottom;
                j = focal_j + 1;
                break;
            case 3: // on bottom of bottom cell
                i = i_bottom + 1;
                j = focal_j;
                break;
            case 4: // on left of bottom cell
                i = i_bottom;
                j = focal_j - 1;
                break;
            case 5: // on left of top cell
                i = i_top;
                j = focal_j - 1;
                break;
        }
    }

    if (i < 0) {
        i = SIZE - 1;
    } else if (i >= SIZE) {
        i = 0;
    }
    if (j < 0) {
        j = SIZE - 1;
    } else if (j >= SIZE) {
        j = 0;
    }

    *pair_i = i;
    *pair_j = j;
}