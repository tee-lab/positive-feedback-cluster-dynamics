#define SIZE 40
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


int main(int argc, char *argv[]) {
    float req_density = atof(argv[1]);
    int simulation_index = atoi(argv[2]);
    char file_root[200];
    strcpy(file_root, argv[3]);

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

    float m, m_by_r, r;
    m = 1 - req_density;
    m_by_r = (1 / req_density) - 1;
    r = m / m_by_r;

    printf("m = %f, m_by_r = %f, r = %f\n", m, m_by_r, r);
}