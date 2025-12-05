MASK_32 = 0xFFFFFFFF


def _left_rotate(x, amount):
    return ((x << amount) | (x >> (32 - amount))) & MASK_32


def md4(message):
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
        return (x & y) | (x & z) | (y & z)

    def h(x, y, z):
        return x ^ y ^ z

    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        x = [int.from_bytes(chunk[i:i + 4], byteorder="little") for i in range(0, 64, 4)]

        aa, bb, cc, dd = a, b, c, d

        # Round 1
        a = _left_rotate((a + f(b, c, d) + x[0]) & MASK_32, 3)
        d = _left_rotate((d + f(a, b, c) + x[1]) & MASK_32, 7)
        c = _left_rotate((c + f(d, a, b) + x[2]) & MASK_32, 11)
        b = _left_rotate((b + f(c, d, a) + x[3]) & MASK_32, 19)

        a = _left_rotate((a + f(b, c, d) + x[4]) & MASK_32, 3)
        d = _left_rotate((d + f(a, b, c) + x[5]) & MASK_32, 7)
        c = _left_rotate((c + f(d, a, b) + x[6]) & MASK_32, 11)
        b = _left_rotate((b + f(c, d, a) + x[7]) & MASK_32, 19)

        a = _left_rotate((a + f(b, c, d) + x[8]) & MASK_32, 3)
        d = _left_rotate((d + f(a, b, c) + x[9]) & MASK_32, 7)
        c = _left_rotate((c + f(d, a, b) + x[10]) & MASK_32, 11)
        b = _left_rotate((b + f(c, d, a) + x[11]) & MASK_32, 19)

        a = _left_rotate((a + f(b, c, d) + x[12]) & MASK_32, 3)
        d = _left_rotate((d + f(a, b, c) + x[13]) & MASK_32, 7)
        c = _left_rotate((c + f(d, a, b) + x[14]) & MASK_32, 11)
        b = _left_rotate((b + f(c, d, a) + x[15]) & MASK_32, 19)

        # Round 2
        a = _left_rotate((a + g(b, c, d) + x[0] + 0x5A827999) & MASK_32, 3)
        d = _left_rotate((d + g(a, b, c) + x[4] + 0x5A827999) & MASK_32, 5)
        c = _left_rotate((c + g(d, a, b) + x[8] + 0x5A827999) & MASK_32, 9)
        b = _left_rotate((b + g(c, d, a) + x[12] + 0x5A827999) & MASK_32, 13)

        a = _left_rotate((a + g(b, c, d) + x[1] + 0x5A827999) & MASK_32, 3)
        d = _left_rotate((d + g(a, b, c) + x[5] + 0x5A827999) & MASK_32, 5)
        c = _left_rotate((c + g(d, a, b) + x[9] + 0x5A827999) & MASK_32, 9)
        b = _left_rotate((b + g(c, d, a) + x[13] + 0x5A827999) & MASK_32, 13)

        a = _left_rotate((a + g(b, c, d) + x[2] + 0x5A827999) & MASK_32, 3)
        d = _left_rotate((d + g(a, b, c) + x[6] + 0x5A827999) & MASK_32, 5)
        c = _left_rotate((c + g(d, a, b) + x[10] + 0x5A827999) & MASK_32, 9)
        b = _left_rotate((b + g(c, d, a) + x[14] + 0x5A827999) & MASK_32, 13)

        a = _left_rotate((a + g(b, c, d) + x[3] + 0x5A827999) & MASK_32, 3)
        d = _left_rotate((d + g(a, b, c) + x[7] + 0x5A827999) & MASK_32, 5)
        c = _left_rotate((c + g(d, a, b) + x[11] + 0x5A827999) & MASK_32, 9)
        b = _left_rotate((b + g(c, d, a) + x[15] + 0x5A827999) & MASK_32, 13)

        # Round 3
        a = _left_rotate((a + h(b, c, d) + x[0] + 0x6ED9EBA1) & MASK_32, 3)
        d = _left_rotate((d + h(a, b, c) + x[8] + 0x6ED9EBA1) & MASK_32, 9)
        c = _left_rotate((c + h(d, a, b) + x[4] + 0x6ED9EBA1) & MASK_32, 11)
        b = _left_rotate((b + h(c, d, a) + x[12] + 0x6ED9EBA1) & MASK_32, 15)

        a = _left_rotate((a + h(b, c, d) + x[2] + 0x6ED9EBA1) & MASK_32, 3)
        d = _left_rotate((d + h(a, b, c) + x[10] + 0x6ED9EBA1) & MASK_32, 9)
        c = _left_rotate((c + h(d, a, b) + x[6] + 0x6ED9EBA1) & MASK_32, 11)
        b = _left_rotate((b + h(c, d, a) + x[14] + 0x6ED9EBA1) & MASK_32, 15)

        a = _left_rotate((a + h(b, c, d) + x[1] + 0x6ED9EBA1) & MASK_32, 3)
        d = _left_rotate((d + h(a, b, c) + x[9] + 0x6ED9EBA1) & MASK_32, 9)
        c = _left_rotate((c + h(d, a, b) + x[5] + 0x6ED9EBA1) & MASK_32, 11)
        b = _left_rotate((b + h(c, d, a) + x[13] + 0x6ED9EBA1) & MASK_32, 15)

        a = _left_rotate((a + h(b, c, d) + x[3] + 0x6ED9EBA1) & MASK_32, 3)
        d = _left_rotate((d + h(a, b, c) + x[11] + 0x6ED9EBA1) & MASK_32, 9)
        c = _left_rotate((c + h(d, a, b) + x[7] + 0x6ED9EBA1) & MASK_32, 11)
        b = _left_rotate((b + h(c, d, a) + x[15] + 0x6ED9EBA1) & MASK_32, 15)

        a = (a + aa) & MASK_32
        b = (b + bb) & MASK_32
        c = (c + cc) & MASK_32
        d = (d + dd) & MASK_32

    return "".join(x.to_bytes(4, byteorder="little").hex() for x in [a, b, c, d])
