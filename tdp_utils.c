#ifndef SIZE
    #define SIZE 100
#endif

#define min(a, b) ((a) < (b) ? (a) : (b))
#define max(a, b) ((a) > (b) ? (a) : (b))

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

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

float get_density(int lattice[][SIZE]) {
    int count = 0;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            count += lattice[i][j];
        }
    }
    return (float) count / (SIZE * SIZE);
}