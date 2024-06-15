#include <stdio.h>
#include <stdlib.h>

typedef struct dynamics_node {
    int before[4];
    int after[4];
    struct dynamics_node *next;
} dynamics_node;

dynamics_node *prepend_dynamics(dynamics_node *head, int before[4], int after[4]) {
    if (head == NULL) {
        dynamics_node *new_node = (dynamics_node *) malloc(sizeof(dynamics_node));
        for (int i = 0; i < 4; i++) {
            new_node->before[i] = before[i];
            new_node->after[i] = after[i];
        }
        new_node->next = NULL;
        return new_node;
    }

    dynamics_node *new_node = (dynamics_node *) malloc(sizeof(dynamics_node));
    for (int i = 0; i < 4; i++) {
            new_node->before[i] = before[i];
            new_node->after[i] = after[i];
        }
    new_node->next = head;
    return new_node;
}

void print_dynamics_list(dynamics_node *head) {
    dynamics_node *current = head;
    while (current != NULL) {
        for (int i = 0; i < 4; i++) {
            printf("%d ", current->before[i]);
        }
        printf("\t");
        for (int i = 0; i < 4; i++) {
            printf("%d ", current->after[i]);
        }
        printf("\n");
        current = current->next;
    }
}

// int main() {
//     node *head = NULL;
//     int list1[4] = {1, 2, 3, 4};
//     int list2[4] = {5, 6, 7, 8};

//     head = prepend(head, list1, list2);
//     head = prepend(head, list2, list1);
//     print_list(head);
// }