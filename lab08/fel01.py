import os
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# 1. Diffie-Hellman paraméterek betöltése
with open("generatorsDH.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]
    p = int(lines[0])  # modulusp
    generators = list(map(int, lines[1:]))  # lehetséges generátorok

g = generators[0]  # válasszuk az első generátort
print(f"DH modulus p = {p}")
print(f"DH generator g = {g}")

# 2. Alice és Bob kulcscsere
alice_private = int.from_bytes(get_random_bytes(32), 'big') % p
bob_private = int.from_bytes(get_random_bytes(32), 'big') % p

alice_public = pow(g, alice_private, p)
bob_public = pow(g, bob_private, p)

shared_secret_alice = pow(bob_public, alice_private, p)
shared_secret_bob = pow(alice_public, bob_private, p)

assert shared_secret_alice == shared_secret_bob
print("Közös DH kulcs sikeresen létrejött!")

# 3. AES kulcs származtatása SHA-256 hashből
shared_key = sha256(str(shared_secret_alice).encode()).digest()
print("AES kulcs (SHA-256):", base64.b64encode(shared_key).decode())

# 4. Fájl titkosítása AES-GCM móddal
def encrypt_file(input_path, output_path, key):
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    with open(input_path, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)

    with open(output_path, 'wb') as f:
        f.write(nonce + ciphertext + tag)

def decrypt_file(encrypted_path, output_path, key):
    with open(encrypted_path, 'rb') as f:
        file_content = f.read()
    
    nonce = file_content[:12]
    tag = file_content[-16:]
    ciphertext = file_content[12:-16]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    except ValueError:
        print("A fájl módosult vagy a tag nem érvényes!")
        return

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

# 5. Futtatás egy példa fájlra
input_file = "bigfile.txt"
enc_file = "bigfile_encrypted.bin"
dec_file = "bigfile_decrypted.bin"

encrypt_file(input_file, enc_file, shared_key)
decrypt_file(enc_file, dec_file, shared_key)

# 6. Ellenőrzés
with open(input_file, 'rb') as f1, open(dec_file, 'rb') as f2:
    if f1.read() == f2.read():
        print("Titkosítás és visszafejtés sikeres!")
    else:
        print("Hiba a visszafejtésben!")
