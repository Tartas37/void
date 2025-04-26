from os.path import splitext
from parser import parse, tokenize
from sys import argv

from generator import generate_c


def main() -> None:

    # reading code from file
    with open(argv[1]) as file:
        code = file.read()

    # generating tokens
    try:
        tokens = tokenize(code)
    except Exception:
        raise

    # parsing tokens
    try:
        ast = parse(tokens)
    except Exception:
        raise

    # generating C code
    try:
        c_code = generate_c(ast)
    except Exception:
        raise

    # writing C code as output
    with open(splitext(argv[1])[0] + ".c", "w") as file:
        file.write(c_code)


if __name__ == "__main__":
    main()
