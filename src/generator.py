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
            if statement[2][0] == "number":
                c_code += f'    int {statement[1]} = {statement[2][1]};\n'
        else:
            raise SyntaxError("Unknown statement syntax!")

    return c_code + "}\n"
        #
        # ("PRINT", r"print"),
        # ("RETURN", r"return"),
        # ("FUN", r"function"),
        #
        # ("NUMBER", r"\d+"),
        # ("IDENT", r"[a-zA-Z_]\w*"),
        #
        # ("PLUS", r"\+"),
        # ("MINUS", r"\-"),
        # ("MULT", r"\*"),
        # ("DIV", r"\/"),
        #
        # ("EQUAL", r"="),
        #
        # ("LPAREN", r"\("),
        # ("RPAREN", r"\)"),
        #
