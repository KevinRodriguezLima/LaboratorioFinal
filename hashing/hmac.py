
import struct

H0 = [
    0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19
]

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

def right_rotate(value, shift):
    return ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF

def sha256(message: bytes) -> str:
    if isinstance(message, str):
        message = message.encode()

    message_len_bits = len(message) * 8

    message += b'\x80'
    while (len(message) % 64) != 56:
        message += b'\x00'

    message += struct.pack('>Q', message_len_bits)

    h = H0.copy()

    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = list(struct.unpack('>16L', chunk))

        for j in range(16, 64):
            s0 = right_rotate(w[j-15], 7) ^ right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
            s1 = right_rotate(w[j-2], 17) ^ right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
            w.append((w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF)

        a, b, c, d, e, f, g, hh = h

        for j in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (hh + S1 + ch + K[j] + w[j]) & 0xFFFFFFFF
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            hh = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        h = [(x + y) & 0xFFFFFFFF for x, y in zip(h, [a, b, c, d, e, f, g, hh])]

    return ''.join(f'{x:08x}' for x in h)


BLOCK_SIZE = 64

def hmac_sha256(key, message):
    if isinstance(key, str): key = key.encode()
    if isinstance(message, str): message = message.encode()

    if len(key) > BLOCK_SIZE:
        key = bytes.fromhex(sha256(key))
    if len(key) < BLOCK_SIZE:
        key = key + b'\x00' * (BLOCK_SIZE - len(key))

    o_key_pad = bytes([k ^ 0x5C for k in key])
    i_key_pad = bytes([k ^ 0x36 for k in key])

    inner = sha256(i_key_pad + message)
    final = sha256(o_key_pad + bytes.fromhex(inner))

    return final


if __name__ == "__main__":
    print("HMAC-SHA256:", hmac_sha256("key", "Hola Mundo"))
