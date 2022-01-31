# TODO add errors if program fails
# TODO add () support ## dump 1 ( 2 2 + ) +
#                             1 + (2 + 2)


import subprocess
import sys, os

def usage():
    print("\nSUBCOMMAND USAGE")
    print("\n  sim    Simulate program")
    print("\n  com    Compile program")

counter = 0
def cc(i = False):
    global counter
    if i is True:
        counter = 0
    c = counter
    counter += 1
    return c
   
PUSH = cc(True) # (0, x)
PLUS = cc()     # (1,  )
MINUS = cc()    # (2,  )
DUMP = cc()     # (3,  )

OPS = cc()

def push(x):
    return (PUSH, x)

def plus():
    return (PLUS, )

def minus():
    return (MINUS, )

def dump():
    return (DUMP, )


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
            out.write("void push(int x) {\n")
            out.write("\tstack[count] = x;\n")
            out.write("\tcount++;\n")
            out.write("}\n\n")
            
            # Pop function
            out.write("int pop() {\n")
            out.write("\tint res = stack[count - 1];\n")
            out.write("\tcount--;\n")
            out.write("\treturn res;\n")
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
                if col[index] in "0123456789" and col[index-1] == 'push':
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
                elif col[index] in "0123456789" and col[index+1] in "0123456789" and col[index+2] in "+-" and col[index-1] == 'dump':
                    program.append(push(int(col[index])))
                    program.append(push(int(col[index+1])))
                    if col[index+2] == '+':
                        program.append(plus())
                    if col[index+2] == '-':
                        program.append(minus())
                    program.append(dump())
            index = 0

program = [

]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        print("\n\nERROR :: no file given")
        exit(0)
    
    subcmd = sys.argv[1]

    file = sys.argv[2]

    make_program(file)

    if subcmd == "sim":
        simulate(program)
    elif subcmd == "com":
        compile(program, "compile.c")
        subprocess.call(["gcc", "compile.c", "-o", "compile"])
        subprocess.call(["compile.exe"])