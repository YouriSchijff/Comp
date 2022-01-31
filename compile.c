#include <stdio.h>

int stack[256];
int count = 0;
char n = 10;

void push(int x) {
	stack[count] = x;
	count++;
}

int pop() {
	int res = stack[count - 1];
	count--;
	return res;
}

int main() {
	int a;
	int b;
	int c;

	//
	// PROGRAM START
	//

	// -- PUSH 1 -- 
	push(1);

	// -- PUSH 2 -- 
	push(2);

	// -- PLUS -- 
	a = pop();
	b = pop();
	push(a + b);

	// -- DUMP -- 
	a = pop();
	printf("%d%c", a, n);

	//
	// PROGRAM END
	//

	return 0;
}