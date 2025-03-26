import json
import base64
import hashlib

# Új JSON beolvasása
with open("PasswdSHA256Salt_hardened.json", "r") as f:
    hardened_users = json.load(f)

# Top jelszavak beolvasása
with open("10-million-password-list-top-10000.txt", "r", encoding="utf-8") as f:
    common_passwords = [line.strip() for line in f]

import time

for user in hardened_users:
    name = user["name"]
    salt = base64.b64decode(user["salt"])
    target_hash = base64.b64decode(user["password"])
    iterations = user["iterations"]

    start = time.time()
    found = False

    for pw in common_passwords:
        test_hash = hashlib.pbkdf2_hmac('sha3_256', pw.encode(), salt, iterations)
        if test_hash == target_hash:
            duration = time.time() - start
            print(f"{name} jelszava újra megtalálva: {pw} {duration:.2f} mp")
            found = True
            break

    if not found:
        print(f"{name} jelszava nem található 1 millió iterációval.")
