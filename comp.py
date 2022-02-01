# TODO add errors if program fails
# TODO add () support ## dump 1 ( 2 2 + ) +
#                     ##      1 + ( 2 + 2 )

'''
push (num)
PUSH A NUMBER TO THE TOP OF THE STACK

plus
ADDS THE TOP 2 NUMBERS FROM THE STACK TOGETHER

minus
SUBTRACTS THE TOP 2 NUMBERS FROM THE STACK

dump [(num1) (num2) (+-)]
PRINTS THE NUMBER FROM THE TOP OF THE STACK

clon
DUPLICATES THE TOP NUMBER FROM THE STACK AND PUTS IT INFRONT

swap (pos1) (pos2)
SWAPS TWO NUMBERS FROM THE STACK

put (pos) (num)
INSERTS A NUMBER IN THE STACK AT A POSITION

== (num)
POPS THE TOP NUMBER FROM THE STACK AND SEES IF IT IS EQUAL TO i. PUSHES 0 IF IT IS NOT. PUSHES 1 IF IT IS.

if (tok) (num) 
IF tok IS ==
THEN IT MEANS THE PROGRAM IS CHECKING IF num IS EQUAL TO THE NUMBER FROM THE TOP OF THE STACK
'''

from datetime import datetime
import subprocess
import sys, os

counter = 0
def cc(i = False):
    global counter
    if i is True:
        counter = 0
    c = counter
    counter += 1
    return c
   
PUSH = cc(True) # (0, i)
PLUS = cc()     # (1,  )
MINUS = cc()    # (2,  )
DUMP = cc()     # (3,  )
CLONE = cc()    # (4,  )
SWAP = cc()     # [5, x, y]
PUT = cc()      # [6, x, i]
OPS = cc()

def push(i):
    return (PUSH, i)

def plus():
    return (PLUS, )

def minus():
    return (MINUS, )

def dump():
    return (DUMP, )

def clone():
    return (CLONE, )

def swap(x, y):
    return [SWAP, x, y]

def put(x, i):
    return [PUT, x, i]

def simulate(program):
    stack = []
    for op in program:
        if op[0] == PUSH:
            stack.append(op[1])
        elif op[0] == PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
        elif op[0] == MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif op[0] == DUMP:
            a = stack.pop()
            print(a)
        elif op[0] == CLONE:
            a = stack.pop()
            stack.append(a)
            stack.append(a)
            pass
        elif op[0] == SWAP:
            stack[op[1]], stack[op[2]] = stack[op[2]], stack[op[1]]
        elif op[0] == PUT:
            stack.insert(op[1], op[2])
        else:
            print("\n\nERROR :: unknown operation given")

def compile(program, path):
    with open(path, "w") as out:
            # Include
            out.write("#include <stdio.h>\n\n")
            
            out.write("int stack[256];\n")  # Initialising stack
            out.write("int count = 0;\n")
            
            out.write("char n = 10;\n\n")
            
            # Push function
            out.write("void push(int i) {\n")
            out.write("\tstack[count] = i;\n")
            out.write("\tcount++;\n")
            out.write("}\n\n")
            
            # Pop function
            out.write("int pop() {\n")
            out.write("\tint res = stack[count - 1];\n")
            out.write("\tcount--;\n")
            out.write("\treturn res;\n")
            out.write("}\n\n")

            
            # Put function
            out.write("void put(int x, int i) {\n")
            out.write("\tfor(int index = 255; index >= x; index--)\n")
            out.write("\t\tstack[index+1] = stack[index];\n")
            out.write("\tstack[x] = i;\n")
            out.write("\tcount++;\n")
            out.write("}\n\n")
            
            # Main function
            out.write("int main() {\n")
            
            out.write("\tint a;\n")
            out.write("\tint b;\n")
            out.write("\tint c;\n\n")
            
            out.write("\t//\n")
            out.write("\t// PROGRAM START\n")
            out.write("\t//\n")

            # Operations
            for op in program:
                if op[0] == PUSH:
                    out.write("\n\t// -- PUSH %d -- \n" % op[1])
                    out.write("\tpush(%d);\n" % op[1])
                elif op[0] == PLUS:
                    out.write("\n\t// -- PLUS -- \n")
                    out.write("\ta = pop();\n")
                    out.write("\tb = pop();\n")
                    out.write("\tpush(a + b);\n")
                elif op[0] == MINUS:
                    out.write("\n\t// -- MINUS -- \n")
                    out.write("\ta = pop();\n")
                    out.write("\tb = pop();\n")
                    out.write("\tpush(b - a);\n")
                elif op[0] == DUMP:
                    out.write("\n\t// -- DUMP -- \n")
                    out.write("\ta = pop();\n")
                    out.write('\tprintf("%d%c", a, n);\n')
                elif op[0] == CLONE:
                    out.write("\n\t// -- CLONE -- \n")
                    out.write("\ta = pop();\n")
                    out.write("\tpush(a);\n")
                    out.write("\tpush(a);\n")
                elif op[0] == SWAP:
                    out.write(f"\n\t// -- SWAP {op[1]} {op[2]} -- \n")
                    out.write("\ta = stack[%d];\n" % op[1])
                    out.write("\tb = stack[%d];\n" % op[2])
                    out.write("\tstack[%d] = b;\n" % op[1])
                    out.write("\tstack[%d] = a;\n" % op[2])
                elif op[0] == PUT:
                    out.write(f"\n\t// -- PUT {op[1]} {op[2]} -- \n")
                    out.write(f"\tput({op[1]}, {op[2]});\n")

            out.write("\n\t//\n")
            out.write("\t// PROGRAM END\n")
            out.write("\t//\n\n")

            out.write("\treturn 0;\n")
            out.write("}")

def make_program(file):
    global program
    index = 0
    file = open(os.getcwd()+"\\"+file) 
    fl = file.read()
    lines = fl.split("\n")
    for i in lines:
        col = i.split(" ")
        for j in col:
            index += 1
            if j == '':
                pass
            elif '//' in j:
                index = 0
                break
            elif j == 'push':
                if int(col[index]) and col[index-1] == 'push':
                    program.append(push(int(col[index])))
            elif j == 'plus':
                col.append('')
                if col[index-1] == 'plus' and not col[index]:
                    program.append(plus())
            elif j == 'minus':
                col.append('')
                if col[index-1] == 'minus' and not col[index]:
                    program.append(minus())
            elif j == 'dump':
                col.append('')
                if col[index-1] == 'dump' and not col[index]:
                    program.append(dump())
            elif j == 'clone':
                col.append('')
                if col[index-1] == 'clone' and not col[index]:
                    program.append(clone())
            elif j == 'swap':
                col.append('')
                if col[index-1] == 'swap' and int(col[index+1]):
                    program.append(swap(int(col[index]), int(col[index+1])))
            elif j == 'put':
                col.append('')
                if col[index-1] == 'put' and int(col[index]) and int(col[index+1]) and not col[index+2]:
                    program.append(put(int(col[index]), int(col[index+1])))
            index = 0

program = [
    
]

def usage():
    print("\nSUBCOMMAND USAGE")
    print("\n  sim    Simulates program")
    print("\n  com    Compiles program")
    print("\n  mat    Simulates and compiles program")


if __name__ == "__main__":
    first = datetime.now()
    if len(sys.argv) == 1:
        usage()
        print("\n\nERROR :: No subcommand given")
        exit(0)
    elif len(sys.argv) == 2:
        usage()
        print("\n\nERROR :: No file given")
        exit(0)
    elif len(sys.argv) > 3:
        usage()
        print("\n\nERROR :: To many arguments given")
        exit(0)
    
    subcmd = sys.argv[1]

    file = sys.argv[2]
    if not file.endswith(".comp"):
        print("\nERROR :: Wrong type file given")
        exit(0)

    make_program(file)

    if subcmd == "sim":
        simulate(program)
    elif subcmd == "com":
        compile(program, "compile.c")
        subprocess.call(["gcc", "compile.c", "-o", "compile"])
        subprocess.call(["compile.exe"])
    elif subcmd == "mat":
        print("\nSIMULATION")
        simulate(program)
        print("\nCOMPILATION")
        compile(program, "compile.c")
        subprocess.call(["gcc", "compile.c", "-o", "compile"])
        subprocess.call(["compile.exe"])
    else:
        usage()
        print("\n\nERROR :: Wrong subcommand given")
        exit(0)