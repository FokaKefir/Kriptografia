import base64
from collections import defaultdict
import ast

# Fájl beolvasása
with open("PasswdSHA256.txt", "r") as f:
    lines = f.readlines()

# Hash → Nevek hozzárendelés
password_map = defaultdict(list)

for line in lines:
    entry = ast.literal_eval(line.strip())  # Szöveg → dictionary
    name = entry['name']
    password_hash = entry['password']
    password_map[password_hash].append(name)

# Csak azokat írjuk ki, ahol több név tartozik ugyanahhoz a hash-hez
for hash_value, names in password_map.items():
    if len(names) > 1:
        print(f"Hash: {hash_value}")
        print("Azonos jelszót használók:")
        for name in names:
            print(f" - {name}")
        print()
