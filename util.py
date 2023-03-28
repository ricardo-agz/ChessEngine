
def position_to_string(position: tuple[int, int]):
    cols = "ABCDEFGH"
    row, col = position
    return f"{cols[col]}{8-row}"