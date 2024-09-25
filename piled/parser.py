from piled.common import ErrorType
from piled.common import Token
from piled.common import TokenType
from piled.common import Word

assert len(TokenType) == 19, "Exhaustive handling of TokenKind in bindings of parser"
token_literal_bindings: dict[str, TokenType] = {
    "+"    : TokenType.PLUS,
    "-"    : TokenType.MINUS,
    "="    : TokenType.EQUAL,
    ">"    : TokenType.GT,
    "<"    : TokenType.LT,
    ">="    : TokenType.GE,
    "<="    : TokenType.LE,
    "if"   : TokenType.IF,
    "else" : TokenType.ELSE,
    "while": TokenType.WHILE,
    "do"   : TokenType.DO,
    "end"  : TokenType.END,
    "dup"  : TokenType.DUP,
    "print": TokenType.PRINT,
    "memory": TokenType.MEMORY,
    "@": TokenType.LOAD,
    "!": TokenType.STORE,
    "syscall3" : TokenType.SYSCALL3,
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
    assert len(TokenType) == 19, \
        "Exhaustive handling of TokenType in cross_reference. \n \
         Note that not all of tokens need to be handled in here.\n \
         Only those that form blocks."
    while addr < program_length:
        if program[addr].type == TokenType.IF:
            stack.append(addr)
        elif program[addr].type == TokenType.ELSE:
            if_addr = stack.pop()
            assert program[if_addr].type == TokenType.IF, \
                "The token `else` can only be used in `if-else` block.\
                 but `%s` is found." % program[if_addr].type.name
            program[if_addr].value = addr + 1
            stack.append(addr)
        elif program[addr].type == TokenType.WHILE:
            stack.append(addr)
        elif program[addr].type == TokenType.DO:
            while_ip = stack.pop()
            program[addr].value = while_ip
            stack.append(addr)
        elif program[addr].type == TokenType.END:
            block_addr = stack.pop()
            assert program[block_addr].type in (TokenType.IF, TokenType.ELSE, TokenType.DO), \
                "The token `end` can only use to close blocks. but `%s` is found." % program[block_addr].type.name
            if program[block_addr].type == TokenType.IF or program[block_addr].type == TokenType.ELSE:
                program[block_addr].value = addr
                program[addr].value = addr + 1
            elif program[block_addr].type == TokenType.DO:
                assert program[block_addr].value is not None
                program[addr].value = program[block_addr].value
                program[block_addr].value = addr + 1
            else:
                assert False, "unreachable"

        addr += 1

    return program
