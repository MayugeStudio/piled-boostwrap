from piled.common import ErrorType
from piled.common import Token
from piled.common import TokenType
from piled.common import Word

assert len(TokenType) == 9, "Exhaustive handling of TokenKind in bindings of parser"
token_literal_bindings: dict[str, TokenType] = {
    "+"    : TokenType.PLUS,
    "-"    : TokenType.MINUS,
    "="    : TokenType.EQUAL,
    "if"   : TokenType.IF,
    "then" : TokenType.THEN,
    "else" : TokenType.ELSE,
    "end"  : TokenType.END,
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
            parser_report_error(word, ErrorType.UnknownTokenError, "unknown value `%s`" % (word.value,))


def cross_references(program: list[Token]) -> list[Token]:
    addr = 0
    stack: list[int] = []
    program_length = len(program)
    assert len(TokenType) == 9, \
        "Exhaustive handling of TokenType in cross_reference. \n \
         Note that not all of tokens need to be handled in here.\n \
         Only those that form blocks."
    while addr < program_length:
        if program[addr].type == TokenType.IF:
            pass
        elif program[addr].type == TokenType.THEN:
            stack.append(addr)
        elif program[addr].type == TokenType.ELSE:
            then_addr = stack.pop()
            assert program[then_addr].type == TokenType.THEN, \
                "The token `else` can only be used in `if-else` block. but %s is found." % program[then_addr].type.name
            program[then_addr].value = addr + 1
            stack.append(addr)
        elif program[addr].type == TokenType.END:
            block_addr = stack.pop()
            assert program[block_addr].type == TokenType.THEN or program[block_addr].type == TokenType.ELSE, \
                "The token `end` can only use to close blocks. but %s is found." % program[block_addr].type.name

            if program[block_addr].type == TokenType.THEN or program[block_addr].type == TokenType.ELSE:
                program[block_addr].value = addr
            else:
                assert False, "unreachable"

        addr += 1

    return program
