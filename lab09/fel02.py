import json
import base64
from Crypto.Signature import eddsa
from Crypto.PublicKey import ECC

# Beállítások
CA_PRIVATE_KEY_FILE = "privateKeyECC_CA_9_2.pem"
CA_PASSWORD = b"CA_Password9_2"
INPUT_FILE = "pk9_2.json"
OUTPUT_FILE = "signed_servers.json"

# 1. CA privát kulcs betöltése
with open(CA_PRIVATE_KEY_FILE, "rt") as f:
    ca_private_key = ECC.import_key(f.read(), passphrase=CA_PASSWORD)

signer = eddsa.new(ca_private_key, 'rfc8032')

# 2. Szerverek adatainak betöltése
with open(INPUT_FILE, "r") as f:
    servers = json.load(f)

# 3. Minden szerver kulcsának aláírása
signed_servers = []
for server in servers:
    name = server["name"]
    public_key_hex = server["publicKey"]
    public_key_bytes = bytes.fromhex(public_key_hex)

    # Digitális aláírás (raw kulcsra)
    signature = signer.sign(public_key_bytes)

    # JSON-ba base64 kódolva tesszük
    server_signed = {
        "name": name,
        "publicKey": public_key_hex,
        "signature": base64.b64encode(signature).decode()
    }
    signed_servers.append(server_signed)

# 4. Eredmény mentése
with open(OUTPUT_FILE, "w") as f:
    json.dump(signed_servers, f, indent=4)

print(f"Sikeresen aláírtad a publikus kulcsokat. Kimeneti fájl: {OUTPUT_FILE}")
