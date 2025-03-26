import json
import hashlib
import base64

# 1. JSON beolvasása
with open("PasswdSHA256.json", "r") as f:
    users = json.load(f)

# 2. Top 10 000 jelszó betöltése
with open("10-million-password-list-top-10000.txt", "r", encoding="utf-8") as f:
    common_passwords = [line.strip() for line in f]

# 3. Hash → jelszó párok előállítása
hash_to_password = {}
for pw in common_passwords:
    digest = hashlib.sha3_256(pw.encode()).digest()
    b64_hash = base64.b64encode(digest).decode()
    hash_to_password[b64_hash] = pw

# 4. Ellenőrzés: felhasználók hash-e szerepel-e az előállítottak között
for user in users:
    name = user["name"]
    hash_val = user["password"]
    if hash_val in hash_to_password:
        print(f"{name} jelszava: {hash_to_password[hash_val]}")
