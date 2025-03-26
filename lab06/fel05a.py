import json
import base64
import hashlib
from Crypto.Random import get_random_bytes

# Feltört jelszavak
cracked_passwords = {
    "Kiss Attila": "123456",
    "Szabo Peter": "password",
    "Nagy Istvan": "qwerty",
    "Szekely Piroska": "letmein",
    "Laszlo Edit": "123456789"
}

new_data_scrypt = []

for name, password in cracked_passwords.items():
    salt = get_random_bytes(16)
    hashed_pw = hashlib.scrypt(
        password.encode(),
        salt=salt,
        n=2**14,  # CPU/memória nehézségi paraméter
        r=8,
        p=1,
        dklen=32
    )
    new_data_scrypt.append({
        "name": name,
        "password": base64.b64encode(hashed_pw).decode(),
        "salt": base64.b64encode(salt).decode(),
        "method": "scrypt"
    })

# JSON mentés
with open("PasswdScrypt.json", "w") as f:
    json.dump(new_data_scrypt, f, indent=4)

print("Scrypt hash-ek elmentve.")
