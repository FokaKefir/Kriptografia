import os
from Crypto.Cipher import DES3, AES, Blowfish
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter

BLOCK_SIZE = 16  # AES és Blowfish esetén (128 bit)
DES3_BLOCK_SIZE = 8  # DES3 esetén (64 bit)
BS = 1024  # Fájlolvasási blokk

def pad(data, block_size):
    """PKCS7 padding a blokkméret eléréséhez"""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    """PKCS7 padding eltávolítása"""
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_CBC(source, destination, key, iv, cipher_class):
    """Titkosítás CBC módban (DES3, AES, Blowfish)"""
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        cipher = cipher_class.new(key, cipher_class.MODE_CBC, iv)
        dst.write(iv)  # IV-t mentjük
        while chunk := src.read(BS):
            chunk = pad(chunk, len(iv))  # Az IV mérete alapján kell padding
            dst.write(cipher.encrypt(chunk))

def decrypt_CBC(source, destination, key, cipher_class):
    """Visszafejtés CBC módban (DES3, AES, Blowfish)"""
    block_size = cipher_class.block_size  # DES3: 8 bájt, AES: 16 bájt
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        iv = src.read(block_size)  # IV beolvasása
        cipher = cipher_class.new(key, cipher_class.MODE_CBC, iv)

        # Fájl teljes beolvasása a padding ellenőrzése miatt
        ciphertext = src.read()

        # Teljes fájl visszafejtése
        plaintext = cipher.decrypt(ciphertext)

        # Padding eltávolítása
        plaintext = unpad(plaintext)  

        # Kiírás a visszafejtett fájlba
        dst.write(plaintext)


def encrypt_CTR(source, destination, key, cipher_class):
    """Titkosítás CTR módban megfelelő blokkmérettel"""
    block_size = cipher_class.block_size  # DES3: 8 bájt, AES: 16 bájt
    nonce = get_random_bytes(block_size // 2)  # DES3: 4 bájt, AES: 8 bájt

    # DES3 esetén 8 bites (64 bit) számláló, AES esetén 16 bites (128 bit)
    if cipher_class == DES3:
        ctr = Counter.new(64, initial_value=int.from_bytes(nonce, byteorder="big"))
    else:
        ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder="big"))

    cipher = cipher_class.new(key, cipher_class.MODE_CTR, counter=ctr)

    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        dst.write(nonce)  # Nonce mentése
        while chunk := src.read(BS):
            dst.write(cipher.encrypt(chunk))

def decrypt_CTR(source, destination, key, cipher_class):
    """Visszafejtés CTR módban megfelelő blokkmérettel"""
    block_size = cipher_class.block_size  # DES3: 8 bájt, AES: 16 bájt
    with open(source, 'rb') as src, open(destination, 'wb') as dst:
        nonce = src.read(block_size // 2)  # DES3: 4 bájt, AES: 8 bájt

        # DES3 esetén 8 bites (64 bit) számláló, AES esetén 16 bites (128 bit)
        if cipher_class == DES3:
            ctr = Counter.new(64, initial_value=int.from_bytes(nonce, byteorder="big"))
        else:
            ctr = Counter.new(128, initial_value=int.from_bytes(nonce, byteorder="big"))

        cipher = cipher_class.new(key, cipher_class.MODE_CTR, counter=ctr)
        while chunk := src.read(BS):
            dst.write(cipher.decrypt(chunk))


def encrypt_decrypt_all_algorithms(input_file):
    """Titkosítás és visszafejtés minden algoritmussal"""
    # Kulcsok és IV generálása
    key_des3 = get_random_bytes(24)  # DES3 192 bit
    key_aes = get_random_bytes(32)   # AES 256 bit
    key_blowfish = get_random_bytes(16)  # Blowfish 128 bit
    iv_des3 = get_random_bytes(8)   # DES3 IV (8 bájt)
    iv_aes = get_random_bytes(16)   # AES IV (16 bájt)
    iv_blowfish = get_random_bytes(8)  # Blowfish IV (8 bájt)

    # Fájlnevek
    encrypted_files = {
        "des3_cbc": "encrypted_des3_cbc",
        "des3_ctr": "encrypted_des3_ctr",
        "aes_cbc": "encrypted_aes_cbc",
        "aes_ctr": "encrypted_aes_ctr",
        "blowfish_cbc": "encrypted_blowfish_cbc"
    }
    decrypted_files = {k: f"decrypted_{k}" for k in encrypted_files}

    # Titkosítás
    encrypt_CBC(input_file, encrypted_files["des3_cbc"], key_des3, iv_des3, DES3)
    encrypt_CTR(input_file, encrypted_files["des3_ctr"], key_des3, DES3)
    encrypt_CBC(input_file, encrypted_files["aes_cbc"], key_aes, iv_aes, AES)
    encrypt_CTR(input_file, encrypted_files["aes_ctr"], key_aes, AES)  
    encrypt_CBC(input_file, encrypted_files["blowfish_cbc"], key_blowfish, iv_blowfish, Blowfish)

    print("Titkosítás befejezve!")

    # Visszafejtés
    decrypt_CBC(encrypted_files["des3_cbc"], decrypted_files["des3_cbc"], key_des3, DES3)
    decrypt_CTR(encrypted_files["des3_ctr"], decrypted_files["des3_ctr"], key_des3, DES3)
    decrypt_CBC(encrypted_files["aes_cbc"], decrypted_files["aes_cbc"], key_aes, AES)
    decrypt_CTR(encrypted_files["aes_ctr"], decrypted_files["aes_ctr"], key_aes, AES)
    decrypt_CBC(encrypted_files["blowfish_cbc"], decrypted_files["blowfish_cbc"], key_blowfish, Blowfish)

    print("Visszafejtés befejezve!")

    # Ellenőrzés
    for key in encrypted_files.keys():
        with open(input_file, "rb") as orig, open(decrypted_files[key], "rb") as dec:
            assert orig.read() == dec.read(), f"Hiba a visszafejtésben: {key}"
        print(f"{key} sikeresen visszafejtve!")

if __name__ == "__main__":
    encrypt_decrypt_all_algorithms("test1.bin")
