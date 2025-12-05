MASK_32 = 0xFFFFFFFF

def _right_rotate(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK_32

def sha256(message):
    if isinstance(message, str):
        message = message.encode()

    # Constantes SHA-256
    K = [
        0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
        0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
        0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
        0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
        0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
        0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
        0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
        0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
    ]

    # Valores iniciales
    h0 = 0x6A09E667
    h1 = 0xBB67AE85
    h2 = 0x3C6EF372
    h3 = 0xA54FF53A
    h4 = 0x510E527F
    h5 = 0x9B05688C
    h6 = 0x1F83D9AB
    h7 = 0x5BE0CD19

    orig_len_bits = len(message) * 8
    message += b"\x80"
    while (len(message) % 64) != 56:
        message += b"\x00"
    message += orig_len_bits.to_bytes(8, 'big')

    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        w = [int.from_bytes(chunk[i:i+4], 'big') for i in range(0, 64, 4)]

        for i in range(16, 64):
            s0 = _right_rotate(w[i-15], 7) ^ _right_rotate(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = _right_rotate(w[i-2], 17) ^ _right_rotate(w[i-2], 19) ^ (w[i-2] >> 10)
            w.append((w[i-16] + s0 + w[i-7] + s1) & MASK_32)

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        for i in range(64):
            S1 = _right_rotate(e, 6) ^ _right_rotate(e, 11) ^ _right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + K[i] + w[i]) & MASK_32
            S0 = _right_rotate(a, 2) ^ _right_rotate(a, 13) ^ _right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & MASK_32

            h = g
            g = f
            f = e
            e = (d + temp1) & MASK_32
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & MASK_32

        h0 = (h0 + a) & MASK_32
        h1 = (h1 + b) & MASK_32
        h2 = (h2 + c) & MASK_32
        h3 = (h3 + d) & MASK_32
        h4 = (h4 + e) & MASK_32
        h5 = (h5 + f) & MASK_32
        h6 = (h6 + g) & MASK_32
        h7 = (h7 + h) & MASK_32

    return ''.join(f"{x:08x}" for x in [h0, h1, h2, h3, h4, h5, h6, h7])
