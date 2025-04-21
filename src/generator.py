def generate_c(ast):
    def add_io(code):
        return f'#include <stdio.h>\n' + code

    c_code = "int main(void) {\n"

    for statement in ast:
        print(statement)
        if statement[0] == "print":
            add_io(c_code)
            c_code += f'    printf("{statement[1][1]}\\n");\n'
        elif statement[0] == "return":
            c_code += f'    return {statement[1][1]};\n'
        elif statement[0] == "assign":
            c_code += f'    int {statement[1]} = {statement[2][1]};\n'
        else:
            raise SyntaxError("Unknown statement syntax!")

    return c_code + "}\n"
