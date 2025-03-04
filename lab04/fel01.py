import base64
import time

def rc4_init(key):
    """RC4 kulcs inicializálása"""
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) & 255
        S[i], S[j] = S[j], S[i]
    return S

def rc4_output(S):
    """RC4 key stream generátor"""
    i, j = 0, 0
    while True:
        i = (i + 1) & 255
        j = (j + S[i]) & 255
        S[i], S[j] = S[j], S[i]
        yield S[(S[i] + S[j]) & 255]

def read_key_from_file(filename):
    """Kulcs beolvasása és dekódolása base64 formátumból"""
    with open(filename, "r") as f:
        encoded_key = f.read().strip()
    return base64.b64decode(encoded_key)

def rc4_encrypt_decrypt(input_file, output_file, key):
    """Bináris fájl titkosítása és visszafejtése RC4 algoritmussal"""
    S = rc4_init(key)
    key_stream = rc4_output(S)

    # Kihagyjuk az első 1024 bájtot a key stream-ből
    for _ in range(1024):
        next(key_stream)

    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        while (byte := fin.read(1)):  # 1 bájtot olvasunk be
            fout.write(bytes([byte[0] ^ next(key_stream)]))

def measure_encryption_time(input_file, key_file):
    """Időmérés a titkosítás során"""
    key = read_key_from_file(key_file)
    output_file = input_file + ".enc"

    start_time = time.time()
    rc4_encrypt_decrypt(input_file, output_file, key)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"{input_file} titkosítása: {elapsed_time:.6f} másodperc")

if __name__ == "__main__":
    # Példa kulcsfájl (base64-ben tárolt kulcsot kell beleírni)
    key_file = "key1.txt"

    # Példa fájlok titkosítása és visszafejtése
    test_files = ["test1.bin", "test2.bin", "test3.bin", "test4.bin", "test5.bin"]  # Különböző méretű fájlok

    for file in test_files:
        measure_encryption_time(file, key_file)

        # Visszafejtés ellenőrzése
        decrypted_file = file + ".dec"
        rc4_encrypt_decrypt(file + ".enc", decrypted_file, read_key_from_file(key_file))

        # Összehasonlítás az eredeti fájl és a visszafejtett fájl között
        with open(file, "rb") as f1, open(decrypted_file, "rb") as f2:
            assert f1.read() == f2.read(), f"Hiba a visszafejtésben: {file}"
        print(f"{file} sikeresen titkosítva és visszafejtve!\n")
