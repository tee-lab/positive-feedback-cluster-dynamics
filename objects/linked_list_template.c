#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int data;
    struct node *next;
} node;

node *prepend(node *head, int data) {
    if (head == NULL) {
        node *new_node = (node *) malloc(sizeof(node));
        new_node->data = data;
        new_node->next = NULL;
        return new_node;
    }

    node *new_node = (node *) malloc(sizeof(node));
    new_node->data = data;
    new_node->next = head;
    return new_node;
}

void print_list(node *head) {
    node *current = head;
    while (current != NULL) {
        printf("%d\n", current->data);
        current = current->next;
    }
}

int main() {
    node *head = NULL;
    head = prepend(head, 1);
    head = prepend(head, 2);
    head = prepend(head, 3);
    print_list(head);
}