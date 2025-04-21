def generate_c(ast):
    c_code = ""

    for statement in ast:
        if statement[0] == "PRINT":
            c_code += f'printf("{statement[1][1]}\\n");\n'
        elif statement[0] == "RETURN":
            c_code += f'return {statement[1][1]};\n'
        else:
            raise SyntaxError("Unknown statement syntax!")

    return c_code
