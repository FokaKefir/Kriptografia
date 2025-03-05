import sympy as sp

def xor_blocks(block1, block2):
    """Két 64 bites blokk XOR művelete"""
    return block1 ^ block2

def lfsr_output(keytemp, cVect):
    for k in range(32):
        bit = 0
        for i in range(32):
            if cVect[i] == 1:
                bit = bit ^ (keytemp >> (31 - i))
        bit = bit & 1
        keytemp = (keytemp << 1) | bit
    return keytemp & 0xFFFFFFFF
        


# Ismert plaintext és ciphertext blokkok
plaintext_chunk = 0xe0ffd8ff464a1000
ciphertext_chunk = 0x880006b0de683e80

keystream = xor_blocks(plaintext_chunk, ciphertext_chunk)

print(f"Visszanyert kulcsfolyam: {keystream:016x}")


mat = sp.Matrix([[0 for _ in range(32)] for _ in range(32)])
vect = sp.Matrix([[0 for _ in range(32)]])

lst = []
for i in range(64):
    bit = keystream & 1
    lst = [bit] + lst
    keystream >>= 1

print(lst)
vect = sp.Matrix(lst[32 : 64]).rot90(k=3)
print(vect)

for i in range(32):
    mat[i] = sp.Matrix(lst[i : i + 32])

mod = 2
invMat = mat.inv_mod(mod)
cVect = (vect * invMat) % mod
print(cVect)

with open("cryptLFSR", "rb") as fin:
    cData = fin.read()

plaintext_chunk = 0xe0ffd8ff#464a1000
ciphertext_chunk = 0x880006b0#de683e80

keystream = xor_blocks(plaintext_chunk, ciphertext_chunk)

c = bytearray()
for i in range(0, len(cData), 4):
    m = int.from_bytes(cData[i : i+4], byteorder='little')
    ctemp = keystream ^ m
    cb = ctemp.to_bytes(4, byteorder='little')
    c += cb
    keystream = lfsr_output(keystream, cVect)

with open('recovered_lfsr.jpg', "wb") as fout:
    fout.write(c)