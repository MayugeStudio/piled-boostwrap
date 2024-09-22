from piled.common import ErrorType, Token, TokenType, Word

assert len(TokenType) == 4, "Exhaustive handling of TokenKind"
token_literal_bindings: dict[str, TokenType] = {
    "+"    : TokenType.PLUS,
    "-"    : TokenType.MINUS,
    "print": TokenType.PRINT,
}


def parser_report_error(word: Word, err_type: ErrorType, message: str, with_exit=True) -> None:
    print("%s:%d:%d: %s: %s" % (word.filepath, word.location.row, word.location.col, str(err_type.value), message))
    if with_exit:
        exit(1)


def parse_word_as_token(word: Word) -> Token:
    if word.value in token_literal_bindings.keys():
        return Token(word.filepath, word.location, token_literal_bindings[word.value])
    else:
        try:
            value = int(word.value)
            return Token(word.filepath, word.location, TokenType.WORD, value=value)
        except ValueError:
            parser_report_error(word, ErrorType.UnknownValue, "unknown value `%s`" % (word.value,))
