from re import search

TOKENS = (
    ("PRINT", r"print"),
    ("RETURN", r"return"),
    ("FUN", r"function"),
    ("EXIT", r"exit"),

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
    ("SKIP", r"[ \t\n]+"),
)

def find_token(string):
    for token, regex in TOKENS:
        if search(regex, string):
            return token

    raise SyntaxError("Unknown syntax!")

def tokenize(code):
    output = []

    lines = code.split(";")

    for line in lines:
        tokens_in_this_line = []
        words = line.split()
        for word in words:
            token = find_token(word)
            tokens_in_this_line.append((token, word))

        if tokens_in_this_line:
            tokens_in_this_line.append(("SEMICOLON", ";"))

        output.append(tokens_in_this_line)

    return output[:-1]  # remove last empty line

def parse(tokens):
    pass
