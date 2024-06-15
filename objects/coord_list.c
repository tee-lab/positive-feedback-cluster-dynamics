#include <stdio.h>
#include <stdlib.h>

typedef struct coord_node {
    int x, y;
    struct coord_node *next;
} coord_node;

coord_node *prepend_coord(coord_node *head, int x, int y) {
    if (head == NULL) {
        coord_node *new_node = (coord_node *) malloc(sizeof(coord_node));
        new_node->x = x;
        new_node->y = y;
        new_node->next = NULL;
        return new_node;
    }

    coord_node *new_node = (coord_node *) malloc(sizeof(coord_node));
    new_node->x = x;
    new_node->y = y;
    new_node->next = head;
    return new_node;
}

coord_node *pop(coord_node *head) {
    coord_node *new_head = head->next;
    // head = NULL;
    free(head);
    return new_head;
}

void print_coord_list(coord_node *head) {
    coord_node *current = head;
    while (current != NULL) {
        printf("%d %d\n", current->x, current->y);
        current = current->next;
    }
}

int is_empty(coord_node *head) {
    return head == NULL;
}

// void main() {
//     coord_node *list = NULL;
//     list = prepend_coord(list, 1, 2);
//     list = prepend_coord(list, 3, 4);
//     list = prepend_coord(list, 5, 6);
//     print_coord_list(list);

//     list = pop(list);
//     print_coord_list(list);
// }