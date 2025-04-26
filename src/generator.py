def generate_c(ast):
    variables = {}

    c_code = """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "uthash.h"

typedef struct {
    char key[32];
    char *value;
    UT_hash_handle hh;
} HashItem;

int main() {
    HashItem *table = NULL, *item;
"""

    def add_variable(c_code, ident, var_type, value):
        nonlocal variables

        if var_type == "int":
            c_code += f"    int {ident} = {value};\n"
        elif var_type == "string":
            c_code += f'    char *{ident} = "{value}";\n'
        else:
            msg = "Unknown variable type!"
            raise SyntaxError(msg)

        variables[ident] = var_type

        return c_code

    def print_variable(c_code, ident):
        try:
            var_type = variables.get(ident)
        except KeyError:
            msg = f"Variable '{ident}' not found!"
            raise SyntaxError(msg)

        if var_type == "int":
            c_code += f'    printf("%i\\n", {ident});\n'
        elif var_type == "string":
            c_code += f'    printf("%s\\n", {ident});\n'
        else:
            msg = "Unknown variable type!"
            raise SyntaxError(msg)

        return c_code

    def add_function(c_code, function_name, arguments):
        for arg in arguments:
            c_code += f'HASH_FIND_STR(table, "{arg}", item);\n'
            c_code += 'if (strcmp("int", item->value) == 0) {\n'
            c_code += f"    int {arg};\n"
        c_code += f"void {function_name}("
        return c_code

    for statement in ast:
        if statement[0] == "print":
            if statement[1][0] == "number":
                c_code += f'    printf("%i\\n", {statement[1][1]});\n'
            elif statement[1][0] == "string":
                c_code += f'    printf("%s\\n", "{statement[1][1]}");\n'
            elif statement[1][0] == "ident":
                c_code = print_variable(c_code, statement[1][1])
            else:
                msg = "Unknown print syntax!"
                raise SyntaxError(msg)
        elif statement[0] == "return":
            c_code += f"    return {statement[1][1]};\n"
        elif statement[0] == "assign":
            if statement[2][0] == "number":
                c_code = add_variable(c_code, statement[1], "int", statement[2][1])
            elif statement[2][0] == "string":
                c_code = add_variable(c_code, statement[1], "string", statement[2][1])
        else:
            msg = "Unknown statement syntax!"
            raise SyntaxError(msg)

    return (
        c_code
        + """
    HashItem *tmp;
    HASH_ITER(hh, table, item, tmp) {
        HASH_DEL(table, item);
        free(item);
    }
}
"""
    )
