
def generate_c(ast):
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

    def add_variable(c_code, ident, var_type):
        c_code += f'    item = malloc(sizeof(HashItem));\n'
        c_code += f'    strcpy(item->key, "{ident}");\n'
        c_code += f'    item->value = \"{var_type}\";\n'
        c_code += f'    HASH_ADD_STR(table, key, item);\n'
        return c_code

    def print_variable(c_code, ident):
        c_code += f"    HASH_FIND_STR(table, \"{ident}\", item);\n"
        c_code += '     if (strcmp("int", item->value) == 0) {\n'
        c_code += f'        printf("%i\\n", {ident});\n'
        c_code += '     }\n'
        c_code += '     else if (strcmp("string", item->value) == 0){\n'
        c_code += f'        printf("%s\\n", {ident});\n'
        c_code += '     }\n'
        return c_code

    for statement in ast:
        print(statement)
        if statement[0] == "print":
            if statement[1][0] == "number":
                c_code += f'    printf("%i\\n", {statement[1][1]});\n'
            elif statement[1][0] == "string":
                c_code += f'    printf("%s\\n", "{statement[1][1]}");\n'
            elif statement[1][0] == "ident":
                c_code = print_variable(c_code, statement[1][1])
            else:
                raise SyntaxError("Unknown print syntax!")
        elif statement[0] == "return":
            c_code += f'    return {statement[1][1]};\n'
        elif statement[0] == "assign":
            if statement[2][0] == "number":
                c_code += f'    int {statement[1]} = {statement[2][1]};\n'
                c_code = add_variable(c_code, statement[1], "int")
            elif statement[2][0] == "STRING":
                c_code += f'    char *{statement[1]} = "{statement[2][1]}";\n'
                c_code = add_variable(c_code, statement[1], "string")
        else:
            raise SyntaxError("Unknown statement syntax!")

    return c_code + """
    HashItem *tmp;
    HASH_ITER(hh, table, item, tmp) {
        HASH_DEL(table, item);
        free(item);
    }
}
        """
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
