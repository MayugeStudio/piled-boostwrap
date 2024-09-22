from enum_helper import enum

TOKEN_INT = enum(reset=True)
TOKEN_PLUS = enum()
TOKEN_MINUS = enum()
TOKEN_TOTAL_COUNT = enum()

token_literal_bindings = {
    '+': TOKEN_PLUS,
    '-': TOKEN_MINUS,
}
