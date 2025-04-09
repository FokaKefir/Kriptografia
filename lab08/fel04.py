from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import os

# 1. RSA kulcspár generálása és mentése
def generate_and_save_keys():
    key = RSA.generate(2048)

    with open("private_key.pem", "wb") as f:
        f.write(key.export_key())

    with open("public_key.pem", "wb") as f:
        f.write(key.publickey().export_key())

    print("Kulcsok elmentve: private_key.pem, public_key.pem")

# 2. Bináris fájl aláírása
def sign_file(filename, private_key_path, signature_path):
    with open(filename, "rb") as f:
        data = f.read()

    key = RSA.import_key(open(private_key_path, "rb").read())
    h = SHA256.new(data)
    signature = pkcs1_15.new(key).sign(h)

    with open(signature_path, "wb") as f:
        f.write(signature)

    print(f"Aláírás elmentve: {signature_path}")

# 3. Aláírás ellenőrzése
def verify_signature(filename, public_key_path, signature_path):
    with open(filename, "rb") as f:
        data = f.read()

    with open(signature_path, "rb") as f:
        signature = f.read()

    key = RSA.import_key(open(public_key_path, "rb").read())
    h = SHA256.new(data)

    try:
        pkcs1_15.new(key).verify(h, signature)
        print("Az aláírás érvényes.")
    except (ValueError, TypeError):
        print("Az aláírás érvénytelen.")

# Futtatás
if __name__ == "__main__":
    # Teszt bináris állomány (ha nincs)
    test_file = "testdata.bin"
    if not os.path.exists(test_file):
        with open(test_file, "wb") as f:
            f.write(get_random_bytes(512))

    generate_and_save_keys()
    sign_file(test_file, "private_key.pem", "signature.bin")
    verify_signature(test_file, "public_key.pem", "signature.bin")
