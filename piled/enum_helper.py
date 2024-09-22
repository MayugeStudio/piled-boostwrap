iota = 0


def enum(reset=False) -> int:
    global iota
    if reset:
        iota = 0
    result = iota
    iota += 1
    return result
