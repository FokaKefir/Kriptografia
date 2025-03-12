import os
import time
import numpy as np

class A51:
    def __init__(self, key):
        """A5/1 inicializálása egy 64 bites kulccsal."""
        self.R1 = int.from_bytes(key[:3], "big") & 0x7FFFF  # 19 bit
        self.R2 = int.from_bytes(key[2:5], "big") & 0x3FFFFF  # 22 bit
        self.R3 = int.from_bytes(key[4:8], "big") & 0x7FFFFF  # 23 bit

    def majority(self):
        """A többségi bit meghatározása a vezérlő bitekből."""
        return (self.R1 >> 8 & 1) + (self.R2 >> 10 & 1) + (self.R3 >> 10 & 1) >= 2

    def step(self):
        """A5/1 egy lépése, új kulcsbit generálása."""
        maj = self.majority()

        if (self.R1 >> 8 & 1) == maj:
            new_bit = (self.R1 >> 18) ^ (self.R1 >> 17) ^ (self.R1 >> 16) ^ (self.R1 >> 13) & 1
            self.R1 = ((self.R1 << 1) | new_bit) & 0x7FFFF

        if (self.R2 >> 10 & 1) == maj:
            new_bit = (self.R2 >> 21) ^ (self.R2 >> 20) & 1
            self.R2 = ((self.R2 << 1) | new_bit) & 0x3FFFFF

        if (self.R3 >> 10 & 1) == maj:
            new_bit = (self.R3 >> 22) ^ (self.R3 >> 21) ^ (self.R3 >> 20) ^ (self.R3 >> 7) & 1
            self.R3 = ((self.R3 << 1) | new_bit) & 0x7FFFFF

        return (self.R1 ^ self.R2 ^ self.R3) & 1

    def generate_keystream(self, length):
        """Generál egy adott hosszúságú kulcsfolyamot."""
        return bytes([sum(self.step() << (7 - i) for i in range(8)) for _ in range(length)])

def a51_encrypt_decrypt(input_file, output_file, key):
    """A5/1 titkosítás és visszafejtés bináris fájlokhoz."""
    cipher = A51(key)

    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        data = fin.read()
        keystream = cipher.generate_keystream(len(data))
        fout.write(bytes(a ^ b for a, b in zip(data, keystream)))

def measure_encryption_time(input_file, key_file):
    """Titkosítási és visszafejtési idő mérése."""
    with open(key_file, "rb") as f:
        key = f.read(8)  # 64 bites kulcs

    encrypted_file = input_file + ".enc"
    decrypted_file = input_file + ".dec"

    start_time = time.time()
    a51_encrypt_decrypt(input_file, encrypted_file, key)
    enc_time = time.time() - start_time
    print(f"{input_file} titkosítása: {enc_time:.6f} másodperc")

    start_time = time.time()
    a51_encrypt_decrypt(encrypted_file, decrypted_file, key)
    dec_time = time.time() - start_time
    print(f"{input_file} visszafejtése: {dec_time:.6f} másodperc")

    # Ellenőrzés
    with open(input_file, "rb") as f1, open(decrypted_file, "rb") as f2:
        assert f1.read() == f2.read(), f"Hiba a visszafejtésben: {input_file}"
    print(f"{input_file} sikeresen visszafejtve!\n")

if __name__ == "__main__":
    # Kulcs generálása
    key_file = "a51_key.bin"
    with open(key_file, "wb") as f:
        f.write(os.urandom(8))  # 64 bites véletlenszerű kulcs

    # Fájlgenerálás és teszt
    file_sizes = {
        "test1.bin": 1024,        # 1 KB
        "test2.bin": 1024 * 100,  # 100 KB
        "test3.bin": 1024 * 1024, # 1 MB
        "test4.bin": 1024 * 10,   # 10 KB
        "test5.bin": 1024 * 500   # 500 KB
    }

    # Bináris fájlok létrehozása
    for file_name, size in file_sizes.items():
        with open(file_name, "wb") as f:
            f.write(os.urandom(size))

    # Titkosítási és visszafejtési idő mérése
    for file in file_sizes.keys():
        measure_encryption_time(file, key_file)
