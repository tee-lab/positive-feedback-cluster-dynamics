#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int x, y;
    struct node *next;
} node;

node *prepend(node *head, int x, int y) {
    if (head == NULL) {
        node *new_node = (node *) malloc(sizeof(node));
        new_node->x = x;
        new_node->y = y;
        new_node->next = NULL;
        return new_node;
    }

    node *new_node = (node *) malloc(sizeof(node));
    new_node->x = x;
    new_node->y = y;
    new_node->next = head;
    return new_node;
}

node *pop(node *head) {
    head = head->next;
    return head;
}

void print_list(node *head) {
    node *current = head;
    while (current != NULL) {
        printf("%d %d\n", current->x, current->y);
        current = current->next;
    }
}

int is_empty(node *head) {
    return head == NULL;
}