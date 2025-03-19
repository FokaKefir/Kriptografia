import os
import struct
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 8  # TEA 64 bites (8 byte) blokkokkal dolgozik
DELTA = 0x9E3779B9  # TEA titkosító állandó

# ---- TEA Alapfüggvények ----
def encrypt_tea(L, R, key):
    """TEA titkosítás egyetlen 64 bites blokkon"""
    sum_val = 0
    for _ in range(32):
        sum_val = (sum_val + DELTA) & 0xFFFFFFFF
        L = (L + (((R << 4) + key[0]) ^ (R + sum_val) ^ ((R >> 5) + key[1]))) & 0xFFFFFFFF
        R = (R + (((L << 4) + key[2]) ^ (L + sum_val) ^ ((L >> 5) + key[3]))) & 0xFFFFFFFF
    return L, R

def decrypt_tea(L, R, key):
    """TEA visszafejtés egyetlen 64 bites blokkon"""
    sum_val = (DELTA << 5) & 0xFFFFFFFF
    for _ in range(32):
        R = (R - (((L << 4) + key[2]) ^ (L + sum_val) ^ ((L >> 5) + key[3]))) & 0xFFFFFFFF
        L = (L - (((R << 4) + key[0]) ^ (R + sum_val) ^ ((R >> 5) + key[1]))) & 0xFFFFFFFF
        sum_val = (sum_val - DELTA) & 0xFFFFFFFF
    return L, R

# ---- Segédfüggvények ----
def bytes_to_blocks(data):
    """64 bites blokkot (8 byte) bont le bal és jobb részre"""
    L, R = struct.unpack(">2I", data)
    return L, R

def blocks_to_bytes(L, R):
    """Bal és jobb részt visszaalakít 8 byte-os blokká"""
    return struct.pack(">2I", L, R)

# ---- TEA-CBC Mód ----
def encrypt_tea_cbc(input_file, output_file, key):
    """TEA-CBC fájl titkosítása"""
    iv = get_random_bytes(BLOCK_SIZE)  # Véletlen IV generálása
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        dst.write(iv)  # IV mentése
        prev_block = iv
        while chunk := src.read(BLOCK_SIZE):
            if len(chunk) < BLOCK_SIZE:
                chunk = chunk.ljust(BLOCK_SIZE, b'\x00')  # Padding
            L, R = bytes_to_blocks(bytes(a ^ b for a, b in zip(chunk, prev_block)))
            L, R = encrypt_tea(L, R, key)
            prev_block = blocks_to_bytes(L, R)
            dst.write(prev_block)

def decrypt_tea_cbc(input_file, output_file, key):
    """TEA-CBC fájl visszafejtése"""
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        iv = src.read(BLOCK_SIZE)  # IV beolvasása
        prev_block = iv
        while chunk := src.read(BLOCK_SIZE):
            L, R = bytes_to_blocks(chunk)
            L, R = decrypt_tea(L, R, key)
            decrypted_block = bytes(a ^ b for a, b in zip(blocks_to_bytes(L, R), prev_block))
            prev_block = chunk
            dst.write(decrypted_block.rstrip(b'\x00'))  # Padding eltávolítása

# ---- TEA-CTR Mód ----
def encrypt_tea_ctr(input_file, output_file, key):
    """TEA-CTR fájl titkosítása"""
    nonce = get_random_bytes(BLOCK_SIZE // 2)  # Véletlen nonce generálása
    counter = 0
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        dst.write(nonce)  # Nonce mentése
        while chunk := src.read(BLOCK_SIZE):
            counter_block = nonce + counter.to_bytes(BLOCK_SIZE // 2, "big")
            L, R = bytes_to_blocks(counter_block)
            L, R = encrypt_tea(L, R, key)
            keystream_block = blocks_to_bytes(L, R)
            encrypted_block = bytes(a ^ b for a, b in zip(chunk.ljust(BLOCK_SIZE, b'\x00'), keystream_block))
            dst.write(encrypted_block)
            counter += 1

def decrypt_tea_ctr(input_file, output_file, key):
    """TEA-CTR fájl visszafejtése"""
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        nonce = src.read(BLOCK_SIZE // 2)  # Nonce beolvasása
        counter = 0
        while chunk := src.read(BLOCK_SIZE):
            counter_block = nonce + counter.to_bytes(BLOCK_SIZE // 2, "big")
            L, R = bytes_to_blocks(counter_block)
            L, R = encrypt_tea(L, R, key)
            keystream_block = blocks_to_bytes(L, R)
            decrypted_block = bytes(a ^ b for a, b in zip(chunk, keystream_block))
            dst.write(decrypted_block.rstrip(b'\x00'))  # Padding eltávolítása
            counter += 1

# ---- Futtatható Kód ----
def encrypt_decrypt_tea(input_file):
    """Fájl titkosítása és visszafejtése TEA algoritmussal"""
    key = [int.from_bytes(get_random_bytes(4), "big") for _ in range(4)]  # 128 bites kulcs
    print(f"Generalt TEA kulcs: {key}")

    encrypted_cbc = "encrypted_tea_cbc"
    decrypted_cbc = "decrypted_tea_cbc"
    encrypted_ctr = "encrypted_tea_ctr"
    decrypted_ctr = "decrypted_tea_ctr"

    # TEA-CBC titkosítás és visszafejtés
    encrypt_tea_cbc(input_file, encrypted_cbc, key)
    decrypt_tea_cbc(encrypted_cbc, decrypted_cbc, key)

    # TEA-CTR titkosítás és visszafejtés
    encrypt_tea_ctr(input_file, encrypted_ctr, key)
    decrypt_tea_ctr(encrypted_ctr, decrypted_ctr, key)

    # Ellenőrzés
    for mode, dec_file in [("TEA-CBC", decrypted_cbc), ("TEA-CTR", decrypted_ctr)]:
        with open(input_file, "rb") as orig, open(dec_file, "rb") as dec:
            assert orig.read() == dec.read(), f"Hiba a visszafejtésben: {mode}"
        print(f"✅ {mode} sikeresen visszafejtve!")

if __name__ == "__main__":
    encrypt_decrypt_tea("test1.bin")
