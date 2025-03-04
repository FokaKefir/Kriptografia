import struct

def xor_blocks(block1, block2):
    """Két 64 bites blokk XOR művelete"""
    return block1 ^ block2

def decrypt_lfsr_file(crypt_file, output_file, keystream):
    """Bináris fájl visszafejtése a kiszámított kulcsfolyammal"""
    keystream_bytes = struct.pack(">Q", keystream)  # 64 bit, big-endian formátumban

    with open(crypt_file, "rb") as f_in, open(output_file, "wb") as f_out:
        crypt_data = f_in.read()
        
        # Visszafejtés XOR-ral a kiszámított kulcsfolyammal
        decrypted_data = bytearray()
        for i in range(len(crypt_data)):
            decrypted_data.append(crypt_data[i] ^ keystream_bytes[i % len(keystream_bytes)])

        f_out.write(decrypted_data)

# Ismert plaintext és ciphertext blokkok
plaintext_chunk = 0xe0ffd8ff464a1000
ciphertext_chunk = 0x880006b0de683e80

# 1. Kulcsfolyam visszanyerése
keystream = xor_blocks(plaintext_chunk, ciphertext_chunk)
print(f"Visszanyert kulcsfolyam: {keystream:016x}")

# 2. Fájl visszafejtése
decrypt_lfsr_file("cryptLFSR", "recovered.jpg", keystream)

print("A fájl sikeresen visszafejtve: recovered.jpg")
