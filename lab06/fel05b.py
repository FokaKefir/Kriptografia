import json
import base64
import hashlib
import time


# Top jelszavak beolvasása
with open("10-million-password-list-top-10000.txt", "r", encoding="utf-8") as f:
    common_passwords = [line.strip() for line in f]

# Scrypt hash-elt fájl beolvasása
with open("PasswdScrypt.json", "r") as f:
    scrypt_users = json.load(f)

for user in scrypt_users:
    name = user["name"]
    salt = base64.b64decode(user["salt"])
    target_hash = base64.b64decode(user["password"])

    start = time.time()
    found = False

    for pw in common_passwords:
        try:
            test_hash = hashlib.scrypt(
                pw.encode(),
                salt=salt,
                n=2**14,
                r=8,
                p=1,
                dklen=32
            )
            if test_hash == target_hash:
                duration = time.time() - start
                print(f" {name} jelszava megtalálva: {pw}, {duration:.2f} mp")
                found = True
                break
        except Exception as e:
            print(" Hiba:", e)
            break

    if not found:
        print(f"{name} jelszava nem található (scrypt).")
