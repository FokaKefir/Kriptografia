import os
import base64
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

KEY_FILE = "chacha_key.txt"

def encrypt_file(input_file, output_file):
    key = get_random_bytes(32)  # 256-bit kulcs
    cipher = ChaCha20_Poly1305.new(key=key)
    nonce = cipher.nonce

    with open(input_file, "rb") as f:
        plaintext = f.read()

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    with open(output_file, "wb") as f:
        f.write(nonce + ciphertext + tag)

    # Kulcs mentése base64-ben
    with open(KEY_FILE, "w") as f:
        f.write(base64.b64encode(key).decode())

    print(f"Titkosítva: {output_file}")
    print(f"Kulcs elmentve: {KEY_FILE}")

def decrypt_file(encrypted_file, output_file):
    with open(KEY_FILE, "r") as f:
        key = base64.b64decode(f.read())

    with open(encrypted_file, "rb") as f:
        data = f.read()

    nonce = data[:12]              # 12 bájt
    tag = data[-16:]               # 16 bájt hitelesítő tag
    ciphertext = data[12:-16]      # középső rész

    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)

    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        with open(output_file, "wb") as f:
            f.write(plaintext)
        print(f"Visszafejtés sikeres: {output_file}")
    except ValueError:
        print("HIBA: A hitelesítő tag érvénytelen — a fájl sérült vagy manipulált.")

# Példa használat
encrypt_file("kecske1.txt", "encrypted.chacha20")
decrypt_file("encrypted.chacha20", "kecske1_chacha20_decrypted.txt")
