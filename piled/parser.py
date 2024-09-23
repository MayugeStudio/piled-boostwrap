from piled.common import ErrorType
from piled.common import Token
from piled.common import TokenType
from piled.common import Word

assert len(TokenType) == 8, "Exhaustive handling of TokenKind"
token_literal_bindings: dict[str, TokenType] = {
    "+"    : TokenType.PLUS,
    "-"    : TokenType.MINUS,
    "="    : TokenType.EQUAL,
    "if"   : TokenType.IF,
    "then" : TokenType.THEN,
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
    stack: list[int] = []
    program_length = len(program)
    assert len(TokenType) == 8, \
        "Exhaustive handling of TokenType in cross_reference. \n \
         Note that not all of tokens need to be handled in here.\n \
         Only those that form blocks."
    while addr < program_length:
        if program[addr].type == TokenType.IF:
            pass
        elif program[addr].type == TokenType.THEN:
            stack.append(addr)
        elif program[addr].type == TokenType.ENDIF:
            then_addr = stack.pop()
            assert program[then_addr].type == TokenType.THEN, \
                "The token `endif` can only close `if` block. but %s is found." % program[then_addr].type.name
            program[then_addr].value = addr

        addr += 1

    return program
