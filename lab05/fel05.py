# EZ NEM JOOO basszam meg

import numpy as np

# ---- Hill Cipher Segédfüggvények ----
def mod_inv_matrix(matrix, mod=256):
    """Moduláris mátrixinverz kiszámítása mod 256 szerint"""
    det = int(round(np.linalg.det(matrix)))  # Mátrix determinánsa
    det_inv = None
    for i in range(mod):
        if (det * i) % mod == 1:
            det_inv = i
            break
    if det_inv is None:
        raise ValueError("A Hill-kulcsmátrix nem invertálható mod 256 szerint!")

    # Kofaktor mátrix és transzponálás
    adjugate_matrix = np.round(det_inv * np.linalg.inv(matrix) * det).astype(int) % mod
    return adjugate_matrix

def decrypt_hill(block, key_inv):
    """Hill titkosítás visszafejtése egy 4 bájtos blokkra"""
    block_vec = np.array([b for b in block]).reshape(-1, 1)
    decrypted_vec = (key_inv @ block_vec) % 256
    return bytes(decrypted_vec.flatten())

# ---- Fájlkezelési Függvények ----
def load_hill_key(file):
    """Beolvassa a Hill CBC kulcsmátrixot"""
    with open(file, "r") as f:
        lines = f.readlines()
    key_matrix = np.array([[int(num) for num in line.split()] for line in lines[1:]])  # Mátrix olvasás
    print(f"Betöltött Hill-kulcsmátrix:\n{key_matrix}")
    return key_matrix

def decrypt_hill_cbc(cipher_file, output_file, key_file):
    """Hill CBC visszafejtés JPG fájlhoz"""
    key_matrix = load_hill_key(key_file)
    key_inv = mod_inv_matrix(key_matrix)  # Kulcs mátrix inverz kiszámítása
    print(f"Inverz Hill-mátrix:\n{key_inv}")

    with open(cipher_file, "rb") as src:
        data = src.read()

    if len(data) < 4:
        raise ValueError("A titkosított állomány túl kicsi!")

    IV = data[-4:]  # IV az utolsó 4 bájt
    data = data[:-4]  # IV nélküli adatok

    print(f"Betöltött IV: {list(IV)}")

    decrypted_data = bytearray()
    prev_cipher_block = IV

    for i in range(0, len(data), 4):
        block = data[i:i+4]
        if len(block) < 4:
            print("FIGYELMEZTETÉS: Az utolsó blokk kisebb, padding feltételezhető!")
            block = block.ljust(4, b'\x00')  # Padding szükség esetén

        decrypted_block = decrypt_hill(block, key_inv)  # Hill visszafejtés
        plain_block = bytes(a ^ b for a, b in zip(decrypted_block, prev_cipher_block))  # CBC mód XOR
        prev_cipher_block = block  # Frissítjük a CBC láncot
        decrypted_data.extend(plain_block)

    with open(output_file, "wb") as dst:
        dst.write(decrypted_data)

    print("A JPG visszafejtése sikeres!")

# ---- Futtatás ----
decrypt_hill_cbc("cryptHillCBC_Ikrek", "decrypted.jpg", "keyHillCBC.txt")
