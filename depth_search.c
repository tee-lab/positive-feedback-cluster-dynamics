#ifndef SIZE
    #define SIZE 5
#endif

#include <stdio.h>
#include "utils.c"
#include "objects/coord_list.c"


void print_explored(int explored[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%d ", explored[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int depth_search(int lattice[SIZE][SIZE], int explored[SIZE][SIZE], int start_x, int start_y) {
    int coord_x[SIZE * SIZE] = {0};
    int coord_y[SIZE * SIZE] = {0};
    int current_index = 0;

    if (lattice[start_x][start_y] == 0 || explored[start_x][start_y] == 1) {
        return 0;
    }

    int cluster_size = 0;
    int neighs_x[4], neighs_y[4];
    coord_x[current_index] = start_x;
    coord_y[current_index] = start_y;
    current_index++;

    while (current_index > 0) {
        int x = coord_x[current_index - 1];
        int y = coord_y[current_index - 1];
        current_index--;
        int new_x, new_y;

        if (explored[x][y] == 0 && lattice[x][y] == 1) {
            explored[x][y] = 1;
            cluster_size++;
            get_neighbours(x, y, neighs_x, neighs_y);

            for (int i = 0; i < 4; i++) {
                new_x = neighs_x[i];
                new_y = neighs_y[i];
                if (lattice[new_x][new_y] == 1 && explored[new_x][new_y] == 0) {
                    coord_x[current_index] = new_x;
                    coord_y[current_index] = new_y;
                    current_index++;
                }
            }
        }
    }

    return cluster_size;
}

// int main() {
//     int lattice[SIZE][SIZE] = {
//         {1, 0, 0, 0, 1},
//         {0, 1, 1, 1, 0},
//         {1, 0, 1, 1, 1},
//         {0, 1, 0, 1, 0},
//         {1, 0, 1, 0, 1}
//     };

//     int explored[SIZE][SIZE] = {0};

//     int cluster_size = depth_search(lattice, explored, 1, 1);
//     printf("Cluster size: %d\n", cluster_size);

//     print_explored(explored);
// }