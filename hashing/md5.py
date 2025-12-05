import math


def _left_rotate(x, amount):
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message):
    if isinstance(message, str):
        message = message.encode()

    orig_len_bits = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF

    message += b"\x80"
    while (len(message) % 64) != 56:
        message += b"\x00"
    message += orig_len_bits.to_bytes(8, byteorder="little")

    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    def f(x, y, z):
        return (x & y) | (~x & z)

    def g(x, y, z):
        return (x & z) | (y & ~z)

    def h(x, y, z):
        return x ^ y ^ z

    def i_func(x, y, z):
        return y ^ (x | ~z)

    s = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
    ]

    k = [int((1 << 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        x = [int.from_bytes(chunk[i:i + 4], byteorder="little") for i in range(0, 64, 4)]

        aa, bb, cc, dd = a, b, c, d

        for i in range(64):
            if 0 <= i <= 15:
                f_res = f(b, c, d)
                g_idx = i
            elif 16 <= i <= 31:
                f_res = g(b, c, d)
                g_idx = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f_res = h(b, c, d)
                g_idx = (3 * i + 5) % 16
            else:
                f_res = i_func(b, c, d)
                g_idx = (7 * i) % 16

            temp = (a + f_res + k[i] + x[g_idx]) & 0xFFFFFFFF
            temp = _left_rotate(temp, s[i])
            a, d, c, b = d, c, b, (b + temp) & 0xFFFFFFFF

        a = (a + aa) & 0xFFFFFFFF
        b = (b + bb) & 0xFFFFFFFF
        c = (c + cc) & 0xFFFFFFFF
        d = (d + dd) & 0xFFFFFFFF

    return "".join(x.to_bytes(4, byteorder="little").hex() for x in [a, b, c, d])
