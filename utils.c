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