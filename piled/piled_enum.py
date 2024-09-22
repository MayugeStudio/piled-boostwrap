from typing import TypeAlias

EnumType: TypeAlias = int

default_iota: EnumType = 1
iota = default_iota


def enum(reset=False) -> int:
    global iota
    if reset:
        iota = default_iota
    result = iota
    iota += 1
    return result
