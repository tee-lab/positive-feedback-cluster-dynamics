#ifndef SIZE
    #define SIZE 5
#endif

#include <stdio.h>
#include "depth_search.c"

void cluster_dynamics(int lattice[][SIZE], int x, int y, int *before, int *after) {
    int explored[SIZE][SIZE] = {0};
    int blank[SIZE][SIZE] = {0};
    int neighs_x[4], neighs_y[4];

    if (lattice[x][y] == 1) {
        lattice[x][y] = 0;
        get_neighbours(x, y, neighs_x, neighs_y);

        for (int i = 0; i < 4; i++) {
            int new_x = neighs_x[i];
            int new_y = neighs_y[i];
            before[i] = depth_search(lattice, explored, new_x, new_y);
        }

        lattice[x][y] = 1;
        after[0] = depth_search(lattice, blank, x, y);
        after[1] = after[2] = after[3] = 0;
    }
    else if (lattice[x][y] == 0) {
        lattice[x][y] = 1;
        get_neighbours(x, y, neighs_x, neighs_y);
        before[0] = depth_search(lattice, blank, x, y);
        before[1] = before[2] = before[3] = 0;

        lattice[x][y] = 0;
        for (int i = 0; i < 4; i++) {
            int new_x = neighs_x[i];
            int new_y = neighs_y[i];
            after[i] = depth_search(lattice, explored, new_x, new_y);
        }
    }
}

void print_status(int before[], int after[]) {
    printf("Before: ");
    for (int i = 0; i < 4; i++) {
        printf("%d ", before[i]);
    }
    printf("\nAfter: ");
    for (int i = 0; i < 4; i++) {
        printf("%d ", after[i]);
    }
    printf("\n");
}

// void main() {
//     int before[4] = {0};
//     int after[4] = {0};

//     // growth
//     // int lattice[SIZE][SIZE] = {
//     //     {0, 0, 0, 0, 0},
//     //     {0, 1, 1, 1, 0},
//     //     {0, 1, 1, 1, 0},
//     //     {0, 1, 1, 1, 0},
//     //     {0, 0, 0, 0, 0}
//     // };
//     // cluster_dynamics(lattice, 2, 2, before, after);
//     // print_status(before, after);

//     // decay
//     // int lattice[SIZE][SIZE] = {
//     //     {0, 0, 0, 0, 0},
//     //     {0, 1, 1, 1, 0},
//     //     {0, 1, 0, 1, 0},
//     //     {0, 1, 1, 1, 0},
//     //     {0, 0, 0, 0, 0}
//     // };
//     // cluster_dynamics(lattice, 2, 2, before, after);
//     // print_status(before, after);

//     // merge
//     // int lattice[SIZE][SIZE] = {
//     //     {0, 0, 1, 0, 0},
//     //     {0, 0, 1, 0, 0},
//     //     {0, 1, 1, 1, 0},
//     //     {0, 1, 0, 1, 0},
//     //     {0, 0, 0, 0, 0}
//     // };
//     // cluster_dynamics(lattice, 2, 2, before, after);
//     // print_status(before, after);

//     // split
//     int lattice[SIZE][SIZE] = {
//         {0, 0, 1, 0, 0},
//         {0, 0, 1, 0, 0},
//         {0, 1, 0, 1, 0},
//         {0, 1, 0, 1, 0},
//         {0, 0, 0, 0, 0}
//     };
//     cluster_dynamics(lattice, 2, 2, before, after);
//     print_status(before, after);
// }