# Paraméterek
A = 157
B = 45
IV = 19

# Modulo 256 szerinti inverz kiszámítása
def mod_inv(a, m=256):
    """Kiszámítja a modulo inverzét A^(-1) mod 256 szerint"""
    for x in range(256):
        if (a * x) % m == 1:
            return x
    return None  # Ha nincs inverz

A_inv = mod_inv(A)
if A_inv is None:
    raise ValueError("Nincs inverz az adott A értékre!")

def decrypt_affine_CBC(cipher_file, output_file, IV, A_inv, B):
    """Affine CBC visszafejtés JPG fájlokhoz"""
    with open(cipher_file, "rb") as src, open(output_file, "wb") as dst:
        prev_cipher_byte = IV  # Kezdeti IV érték
        while byte := src.read(1):
            C = byte[0]
            P = (A_inv * ((C - B) % 256)) % 256  # Affine visszafejtés
            P ^= prev_cipher_byte  # CBC mód XOR művelet
            prev_cipher_byte = C  # Következő iterációhoz eltároljuk a jelenlegi C-t
            dst.write(bytes([P]))

# Futtatás
decrypt_affine_CBC("cryptAffine256_Tanacs", "decrypted.jpg", IV, A_inv, B)
print("A JPG visszafejtése sikeres!")
