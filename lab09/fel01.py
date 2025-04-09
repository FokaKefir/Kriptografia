import json
from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256

def load_key(filename, passphrase=None):
    with open(filename, "rt") as f:
        return ECC.import_key(f.read(), passphrase=passphrase)

def find_owner(ca_public_key, public_key_pem, signature_list):
    public_key_hash = SHA512.new(public_key_pem.encode()).digest()

    for entry in signature_list:
        name = entry["name"]
        signature = bytes.fromhex(entry["signature"])
        verifier = eddsa.new(ca_public_key, 'rfc8032')
        try:
            verifier.verify(public_key_hash, signature)
            return name
        except ValueError:
            continue
    return None

def generate_shared_secret(private_key, peer_public_key):
    # ECC key agreement: shared point = priv * pub
    shared_point = peer_public_key.pointQ * private_key.d
    shared_x = int(shared_point.x).to_bytes(32, byteorder='big')
    # Derive 32-byte key using HKDF
    return HKDF(shared_x, 32, b"", SHA256)

def main():
    # 1. Központi hatóság publikus kulcsának betöltése
    ca_public_key = load_key("publicKeyECC_CA_9_1.pem")

    # 2. Ellenőrizendő publikus kulcs betöltése
    with open("publicKeyECC_B_9_1.pem", "rt") as f:
        public_key_b_pem = f.read()
        public_key_b = ECC.import_key(public_key_b_pem)

    # 3. Aláírások betöltése
    with open("signatures9_1.json", "rt") as f:
        signatures = json.load(f)

    # 4. Tulajdonos meghatározása
    owner = find_owner(ca_public_key, public_key_b_pem, signatures)
    if not owner:
        print("Nem található érvényes aláírás a kulcshoz.")
        return
    print(f"A kulcs tulajdonosa: {owner}")

    # 5. Saját privát kulcs betöltése jelszóval
    private_key_a = load_key("privateKeyECC_A_9_1.pem", passphrase="pasword_A_9_1")

    # 6. Közös titkos kulcs meghatározása
    shared_key = generate_shared_secret(private_key_a, public_key_b)
    print(f"Létrehozott közös titkos kulcs (32 bájt): {shared_key.hex()}")

if __name__ == "__main__":
    main()
