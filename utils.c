#ifndef UTILS
    #define UTILS
#endif

#ifndef SIZE
    #define SIZE 100
#endif


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

float get_density(int lattice[SIZE][SIZE]) {
    int count = 0;
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            count += lattice[i][j];
        }
    }
    return (float) count / (SIZE * SIZE);
}

void print_lattice(int lattice[SIZE][SIZE]) {
    printf("\n");
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf("%d ", lattice[i][j]);
        }
        printf("\n");
    }
}

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