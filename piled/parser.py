from piled.common import Word, TokenKind, Token, ErrorKind

assert len(TokenKind) == 4, "Exhaustive handling of TokenKind"
token_literal_bindings: dict[str, TokenKind] = {
    '+': TokenKind.PLUS,
    '-': TokenKind.MINUS,
    'print': TokenKind.PRINT,
}


def parser_report_error(word: Word, kind: ErrorKind, message: str, with_exit=True) -> None:
    print("%s:%d:%d: %s: %s" %
          (word.filepath,
           word.location.row, word.location.col,
           str(kind.value), message))
    if with_exit:
        exit(1)


def parse_word_as_token(word: Word) -> Token:
    if word.value in token_literal_bindings.keys():
        return Token(word.filepath, word.location, token_literal_bindings[word.value])
    else:
        try:
            value = int(word.value)
            return Token(word.filepath, word.location, TokenKind.WORD, value=value)
        except ValueError:
            parser_report_error(word, ErrorKind.UnknownValue, "unknown value `%s`" % (word.value,))
