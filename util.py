
def position_to_string(position: tuple[int, int]) -> str:
    cols = "ABCDEFGH"
    row, col = position
    return f"{cols[col]}{8-row}"

def string_to_position(position: str) -> tuple[int, int]:
    cols = "ABCDEFGH"
    file, rank = position
    col = cols.index(file)
    row = 8 - int(rank)
    return row, col