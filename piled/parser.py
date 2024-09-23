from piled.common import ErrorType
from piled.common import Token
from piled.common import TokenType
from piled.common import Word

assert len(TokenType) == 7, "Exhaustive handling of TokenKind"
token_literal_bindings: dict[str, TokenType] = {
    "+"    : TokenType.PLUS,
    "-"    : TokenType.MINUS,
    "="    : TokenType.EQUAL,
    "if"   : TokenType.IF,
    "endif": TokenType.ENDIF,
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
            return Token(word.filepath, word.location, TokenType.PUSH_INT, value=value)
        except ValueError:
            parser_report_error(word, ErrorType.UnknownValue, "unknown value `%s`" % (word.value,))


def cross_references(program: list[Token]) -> list[Token]:
    addr = 0
    stack = []
    program_length = len(program)
    assert len(TokenType) == 7, \
        "Exhaustive handling of TokenType in cross_reference. \
         Note that not all of tokens need to be handled in here.\
         Only those that form blocks."
    while addr < program_length:
        if program[addr].type == TokenType.IF:
            stack.append(addr)
        elif program[addr].type == TokenType.ENDIF:
            if_addr = stack.pop()
            assert program[if_addr].type == TokenType.IF, \
                "The token `endif` can only close `if` block. but other are found."
            program[if_addr].value = addr

        addr += 1

    return program
