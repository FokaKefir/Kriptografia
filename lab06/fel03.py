import json
import base64
import hashlib

# 1. JSON beolvasása
with open("PasswdSHA256Salt.json", "r") as f:
    users = json.load(f)

# 2. Top 10 000 jelszó betöltése
with open("10-million-password-list-top-10000.txt", "r", encoding="utf-8") as f:
    common_passwords = [line.strip() for line in f]

# 3. Felhasználók jelszavainak feltörése
for user in users:
    name = user["name"]
    stored_hash = base64.b64decode(user["password"])
    salt = base64.b64decode(user["salt"])

    for pw in common_passwords:
        test_hash = hashlib.pbkdf2_hmac(
            'sha3_256',
            pw.encode(),
            salt,
            1000
        )
        if test_hash == stored_hash:
            print(f"{name} jelszava: {pw}")
            break  # Ha megtaláltuk, nem kell tovább próbálkozni
