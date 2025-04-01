from Crypto.Util.number import inverse, long_to_bytes
import os

# 1. RSA modulus beolvasása
with open("rsa_n.txt", "r") as f:
    n = int(f.read().strip())


# 2. Prímszámok beolvasása és p megtalálása
with open("keys.txt", "r") as f:
    primes = [int(line.strip()) for line in f.readlines()[::2]]


p = None
for prime in primes:
    if n % prime == 0:
        p = prime
        break

if not p:
    raise ValueError("Nem található megfelelő prímszám a keys.txt fájlban!")

q = n // p
phi = (p - 1) * (q - 1)
e = 65537
d = inverse(e, phi)

print("RSA paraméterek:")
print(f"p = {p}")
print(f"q = {q}")
print(f"d = {d}")

# 3. Titkosított fájl beolvasása
with open("cryptedRSA", "rb") as f:
    ciphertext = f.read()

# 4. RSA visszafejtés blokkosan
# A blokk mérete a modulus bájtos hossza
block_size = (n.bit_length() + 7) // 8  # kerekítve felfelé
blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]

decrypted = b""
for block in blocks:
    c = int.from_bytes(block, byteorder='big')
    m = pow(c, d, n)
    decrypted += long_to_bytes(m)

# 5. Csak az első 44 bájt kell
original = decrypted[:44]

print("\nVisszafejtett üzenet:")
print(original.decode(errors='replace'))

# Írd ki fájlba a visszafejtett tartalmat
with open("decrypted_output.bin", "wb") as f:
    f.write(original)

print("A visszafejtett fájl elmentve: decrypted_output.bin")