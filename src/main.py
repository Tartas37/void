from parser import tokenize, parse
from generator import generate_c

from sys import argv
from os.path import splitext

def main():

    # reading code from file
    with open(argv[1], "r") as file:
        code = file.read()

    # generating tokens
    try:
        tokens = tokenize(code)
    except Exception as e:
        print("Error while generating tokens")
        raise(e)

    # parsing tokens
    try:
        ast = parse(tokens)
    except Exception as e:
        print("Error while parsing tokens")
        raise(e)

    # generating C code
    try:
        c_code = generate_c(ast)
    except Exception as e:
        print("Error while generating c code")
        raise(e)

    # writing C code as output
    with open(splitext(argv[1])[0] + ".c", "w") as file:
        file.write(c_code)

    print("Translation to C was complited successfuly!")

if __name__ == "__main__":
    main()
