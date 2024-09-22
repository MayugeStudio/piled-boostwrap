from .asm_generator import generate_assembly
from .ir_builder import build_IR_from_token
from .lexer import lex_file
from .parser import parse_word_as_token

__all__ = ["lex_file", "parse_word_as_token", "build_IR_from_token", "generate_assembly"]
