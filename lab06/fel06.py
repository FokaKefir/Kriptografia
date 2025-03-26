import os
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY_FILE = "aes_gcm_key.txt"

def encrypt_file(input_file, output_file):
    key = get_random_bytes(32)  # AES-256
    nonce = get_random_bytes(12)  # GCM 12 bájtos ajánlott nonce

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    # Beolvasás és titkosítás
    with open(input_file, "rb") as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    # Fájl felépítése: [nonce][ciphertext][tag]
    with open(output_file, "wb") as f:
        f.write(nonce + ciphertext + tag)

    # Kulcs mentése base64 formátumban
    with open(KEY_FILE, "w") as f:
        f.write(base64.b64encode(key).decode())

    print(f"Titkosítva: {output_file}")
    print(f"Kulcs elmentve: {KEY_FILE}")

def decrypt_file(encrypted_file, output_file):
    # Kulcs betöltése
    with open(KEY_FILE, "r") as f:
        key = base64.b64decode(f.read())

    with open(encrypted_file, "rb") as f:
        data = f.read()

    nonce = data[:12]
    tag = data[-16:]
    ciphertext = data[12:-16]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        with open(output_file, "wb") as f:
            f.write(plaintext)
        print(f"Visszafejtés sikeres: {output_file}")
    except ValueError:
        print("HIBA: A hitelesítési tag érvénytelen – a fájl módosult vagy sérült!")

# Példafutás
encrypt_file("kecske1.txt", "example_encrypted.aesgcm")
decrypt_file("example_encrypted.aesgcm", "kecske1_decrypted.txt")
