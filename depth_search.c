#ifndef SIZE
    #define SIZE 5
#endif

#include <stdio.h>
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

void get_neighbours(int x, int y, int neighs_x[], int neighs_y[]) {
    // left neighbour
    if (x - 1 < 0) {
        neighs_x[0] = SIZE - 1;
    }
    else {
        neighs_x[0] = x - 1;
    }
    neighs_y[0] = y;

    // right neighbour
    if (x + 1 >= SIZE) {
        neighs_x[1] = 0;
    }
    else {
        neighs_x[1] = x + 1;
    }
    neighs_y[1] = y;

    // top neighbour
    neighs_x[2] = x;
    if (y - 1 < 0) {
        neighs_y[2] = SIZE - 1;
    }
    else {
        neighs_y[2] = y - 1;
    }

    // bottom neighbour
    neighs_x[3] = x;
    if (y + 1 >= SIZE) {
        neighs_y[3] = 0;
    }
    else {
        neighs_y[3] = y + 1;
    }
}


int depth_search(int lattice[SIZE][SIZE], int explored[SIZE][SIZE], int start_x, int start_y) {
    node *stack = NULL;
    
    if (lattice[start_x][start_y] == 0 || explored[start_x][start_y] == 1) {
        return 0;
    }

    int cluster_size = 0;
    int neighs_x[4], neighs_y[4];
    stack = prepend(stack, start_x, start_y);

    while (!is_empty(stack)) {
        node *current = stack;
        stack = pop(stack);

        int x = current->x;
        int y = current->y;
        int new_x, new_y;

        if (explored[x][y] == 0 && lattice[x][y] == 1) {
            explored[x][y] = 1;
            cluster_size++;
            get_neighbours(x, y, neighs_x, neighs_y);

            for (int i = 0; i < 4; i++) {
                new_x = neighs_x[i];
                new_y = neighs_y[i];
                if (lattice[new_x][new_y] == 1 && explored[new_x][new_y] == 0) {
                    stack = prepend(stack, new_x, new_y);
                }
            }
        }
    }

    return cluster_size;
}

int main() {
    int lattice[SIZE][SIZE] = {
        {1, 0, 0, 0, 1},
        {0, 1, 1, 1, 0},
        {1, 0, 1, 1, 1},
        {0, 1, 0, 1, 0},
        {1, 0, 1, 0, 1}
    };

    int explored[SIZE][SIZE] = {0};

    int cluster_size = depth_search(lattice, explored, 1, 1);
    printf("Cluster size: %d\n", cluster_size);

    print_explored(explored);
}