import sys

from piled.common import Location
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


def report_error(filepath: str, loc: Location, message: str, with_exit=True) -> None:
    print("%s:%d:%d: %s" % (filepath, loc.row, loc.col, message), file=sys.stderr)
    if with_exit:
        exit(1)


def parse_word_as_token(word: Word) -> Token:
    if word.value in token_literal_bindings.keys():
        return Token(word.filepath, word.loc, token_literal_bindings[word.value])
    else:
        try:
            value = int(word.value)
            return Token(word.filepath, word.loc, TokenType.PUSH_INT, value=value)
        except ValueError:
            report_error(word.filepath, word.loc, "unknown value `%s`" % (word.value,))


def cross_references(program: list[Token]) -> list[Token]:
    addr = 0
    stack: list[int] = []
    program_length = len(program)
    assert len(TokenType) == 19, "Exhaustive handling of TokenType in cross_reference. \n"
    while addr < program_length:
        if program[addr].type == TokenType.IF:
            stack.append(addr)
        elif program[addr].type == TokenType.ELSE:
            if_addr = stack.pop()
            if program[if_addr].type != TokenType.IF:
                report_error(program[if_addr].filepath, program[if_addr].loc,
                             "The token `else` can only be used in `if-else` block. \
                             but `%s` is found." % program[if_addr].type.name)
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
            if program[block_addr].type in (TokenType.IF, TokenType.ELSE, TokenType.DO):
                report_error(program[block_addr].filepath, program[block_addr].loc,
                             "The token `end` can only use to close blocks. \
                             but `%s` is found." % program[block_addr].type.name)
            if program[block_addr].type == TokenType.IF or program[block_addr].type == TokenType.ELSE:
                program[block_addr].value = addr
                program[addr].value = addr + 1
            elif program[block_addr].type == TokenType.DO:
                if program[block_addr].value is None:
                    report_error(program[block_addr].filepath, program[block_addr].loc,
                                 "`do` can use with `while`.")
                program[addr].value = program[block_addr].value
                program[block_addr].value = addr + 1
            else:
                assert False, "unreachable"

        addr += 1

    return program
