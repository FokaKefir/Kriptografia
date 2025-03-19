# EZ IS HIBAS basszameg

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
    """Hill titkosítás visszafejtése egy 2 bájtos blokkra"""
    block_vec = np.array([b for b in block]).reshape(-1, 1)
    decrypted_vec = (key_inv @ block_vec) % 256
    return bytes(decrypted_vec.flatten())

# ---- Fájlkezelési Függvények ----
def decrypt_hill_cbc(cipher_file, output_file, key_matrix, IV):
    """Hill CBC visszafejtés GIF fájlhoz (2x2 Hill mátrix)"""
    key_inv = mod_inv_matrix(key_matrix)  # Kulcs mátrix inverz kiszámítása
    print(f"Inverz Hill-mátrix:\n{key_inv}")

    with open(cipher_file, "rb") as src:
        data = src.read()

    print(f"Betöltött IV: {list(IV)}")

    decrypted_data = bytearray()
    prev_cipher_block = bytes(IV)

    for i in range(0, len(data), 2):
        block = data[i:i+2]
        if len(block) < 2:
            print("⚠️ FIGYELMEZTETÉS: Az utolsó blokk kisebb, padding feltételezhető!")
            block = block.ljust(2, b'\x00')  # Padding szükség esetén

        decrypted_block = decrypt_hill(block, key_inv)  # Hill visszafejtés
        plain_block = bytes(a ^ b for a, b in zip(decrypted_block, prev_cipher_block))  # CBC mód XOR
        prev_cipher_block = block  # Frissítjük a CBC láncot
        decrypted_data.extend(plain_block)

    with open(output_file, "wb") as dst:
        dst.write(decrypted_data)

    print("A GIF visszafejtése sikeres!")

# ---- Konstansok ----
IV = (129, 131)  # IV értékek
key_matrix = np.array([[27, 131], [22, 101]])  # Hill titkosító kulcs (2x2 mátrix)

# ---- Futtatás ----
decrypt_hill_cbc("cryptHillCBC_TheCircleIsComplete", "decrypted.gif", key_matrix, IV)
