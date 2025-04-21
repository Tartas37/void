from re import findall, fullmatch

def tokenize(code):

    TOKENS = (
        ("PRINT", r"print"),
        ("RETURN", r"return"),
        ("FUN", r"function"),

        ("NUMBER", r"\d+"),
        ("IDENT", r"[a-zA-Z_]\w*"),

        ("PLUS", r"\+"),
        ("MINUS", r"\-"),
        ("MULT", r"\*"),
        ("DIV", r"\/"),

        ("EQUAL", r"="),

        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),

        ("SEMICOLON", r";"),
    )

    def find_token(string):
        for token, regex in TOKENS:
            if fullmatch(regex, string):
                return token

        raise SyntaxError(f"Unknown token: {string}")

    output = []

    tokens = findall(r'\w+|==|[-+*/=;()]', code)

    for word in tokens:
        token = find_token(word)
        output.append((token, word))

    return output
def parse(tokens):
    pos = 0

    def current():
        return tokens[pos] if pos < len(tokens) else ("EOF", "")

    def match(type_):
        nonlocal pos
        if current()[0] == type_:
            pos += 1
            return True
        return False

    def expect(type_):
        if not match(type_):
            raise SyntaxError(f"Expected {type_}, got {current()}")

    def parse_expression():
        nonlocal pos
        left = parse_term()
        while current()[0] in ("PLUS", "MINUS"):
            op = current()[1]
            pos += 1
            right = parse_term()
            left = (op, left, right)
        return left

    def parse_term():
        nonlocal pos
        tok_type, value = current()
        if tok_type == "NUMBER":
            pos += 1
            return ("number", int(value))
        elif tok_type == "IDENT":
            pos += 1
            return ("ident", value)
        elif tok_type == "LPAREN":
            pos += 1
            expr = parse_expression()
            expect("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected expression: {current()}")

    def parse_statement():
        nonlocal pos
        if match("PRINT"):
            expect("LPAREN")
            expr = parse_expression()
            expect("RPAREN")
            expect("SEMICOLON")
            return ("print", expr)

        elif match("RETURN"):
            expr = parse_expression()
            expect("SEMICOLON")
            return ("return", expr)

        elif match("FUN"):
            tok_type, name = current()
            if tok_type != "IDENT":
                raise SyntaxError("Expected function name")
            pos += 1
            expect("LPAREN")
            expect("RPAREN")
            expect("LBRACE")  # еще не добавили в токены, пока можно убрать или заменить
            body = []
            while not match("RBRACE"):
                body.append(parse_statement())
            return ("function", name, body)

        elif current()[0] == "IDENT":
            # переменная = выражение;
            name = current()[1]
            pos += 1
            expect("EQUAL")
            expr = parse_expression()
            expect("SEMICOLON")
            return ("assign", name, expr)

        else:
            raise SyntaxError(f"Unknown statement: {current()}")

    # основной цикл
    ast = []
    while current()[0] != "EOF":
        ast.append(parse_statement())
    return ast

