import json
import base64
import hashlib
from Crypto.Random import get_random_bytes

# Feltört jelszavak innen származnak (az előző feladat alapján)
cracked_passwords = {
    "Szabo Peter": "mypassword",
    "Nagy Istvan": "qwerty",
    "Szekely Piroska": "little1",
    "Laszlo Edit": "miriam"
}

new_data = []

for name, password in cracked_passwords.items():
    salt = get_random_bytes(32)
    hashed_pw = hashlib.pbkdf2_hmac('sha3_256', password.encode(), salt, 1_000_000)
    new_data.append({
        "name": name,
        "password": base64.b64encode(hashed_pw).decode(),
        "salt": base64.b64encode(salt).decode(),
        "iterations": 1_000_000
    })

# Mentés új JSON állományba
with open("PasswdSHA256Salt_hardened.json", "w") as f:
    json.dump(new_data, f, indent=4)

print("Új jelszóhash-ek elmentve 1 millió iterációval.")
