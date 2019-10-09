
def hex_to_rgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

COLORS = [
    hex_to_rgb("#0d2b45"), #0
    hex_to_rgb("#203c56"), #1
    hex_to_rgb("#544e68"), #2
    hex_to_rgb("#8d697a"), #3
    hex_to_rgb("#d08159"), #4
    hex_to_rgb("#ffaa5e"), #5
    hex_to_rgb("#ffd4a3"), #6
    hex_to_rgb("#ffecd6")  #7
]