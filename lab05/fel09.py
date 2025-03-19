import os
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 8  # DES3 blokk mérete (64 bit)

# ---- Segédfüggvények ----
def pad(data):
    """PKCS7 padding a blokkméret eléréséhez"""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    """PKCS7 padding eltávolítása"""
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_CBC_BMP(input_file, output_file, key, iv):
    """BMP állomány titkosítása DES3-CBC módban"""
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        header = src.read(54)  # BMP fejléc elmentése (54 bájt)
        data = src.read()
        data = pad(data)  # Padding hozzáadása

        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(data)

        dst.write(header + encrypted_data)  # Fejléc + titkosított adat

def decrypt_CBC_BMP(input_file, output_file, key, iv):
    """BMP állomány visszafejtése DES3-CBC módban"""
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        header = src.read(54)
        encrypted_data = src.read()

        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data))

        dst.write(header + decrypted_data)

def encrypt_ECB_BMP(input_file, output_file, key):
    """BMP állomány titkosítása DES3-ECB módban (Megfigyelhető, hogy nem véd jól!)"""
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        header = src.read(54)
        data = src.read()
        data = pad(data)

        cipher = DES3.new(key, DES3.MODE_ECB)
        encrypted_data = cipher.encrypt(data)

        dst.write(header + encrypted_data)

def decrypt_ECB_BMP(input_file, output_file, key):
    """BMP állomány visszafejtése DES3-ECB módban"""
    with open(input_file, "rb") as src, open(output_file, "wb") as dst:
        header = src.read(54)
        encrypted_data = src.read()

        cipher = DES3.new(key, DES3.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data))

        dst.write(header + decrypted_data)

# ---- Titkosítás és visszafejtés ----
key = DES3.adjust_key_parity(get_random_bytes(24))  # DES3 kulcs generálás
iv = get_random_bytes(8)  # CBC módhoz IV

encrypt_CBC_BMP("image.bmp", "encrypted_CBC.bmp", key, iv)
decrypt_CBC_BMP("encrypted_CBC.bmp", "decrypted_CBC.bmp", key, iv)

encrypt_ECB_BMP("image.bmp", "encrypted_ECB.bmp", key)
decrypt_ECB_BMP("encrypted_ECB.bmp", "decrypted_ECB.bmp", key)

print("Titkosítás és visszafejtés kész!")
