import pyxel

index = {
    0: {
        "u": 0,
        "v": 0
    },
    1: {
        "u": 37,
        "v": 0
    },
    2: {
        "u": 74,
        "v": 0
    },
    3: {
        "u": 111,
        "v": 0
    },
    4: {
        "u": 148,
        "v": 0
    },
    5: {
        "u": 185,
        "v": 0
    },
    6: {
        "u": 0,
        "v": 48
    },
    7: {
        "u": 37,
        "v": 48
    },
    8: {
        "u": 74,
        "v": 48
    },
    9: {
        "u": 111,
        "v": 48
    },
    '/': {
        "u": 148,
        "v": 48
    }

}


def nice_font_number(x, y, str):
    for i, chr in enumerate(str):
        if chr == '/':
            pyxel.blt(x + i * 37, y, 1, index['/']["u"], index['/']["v"], 37, 48, 0)
        else:
            pyxel.blt(x + i*37, y, 1, index[int(chr)]["u"], index[int(chr)]["v"] , 37, 48, 0)
