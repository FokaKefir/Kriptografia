from Crypto.Util import number
import hashlib
import os
import random

# 1. DH paraméterek generálása
def generate_dh_params(bits=2048):
    q = number.getPrime(256)
    while True:
        k = number.getRandomRange(2**(bits - 256 - 1), 2**(bits - 256))
        p = q * k + 1
        if number.isPrime(p):
            break
    for g in range(2, p):
        if pow(g, k, p) != 1:
            return p, q, g
    raise Exception("Nem sikerült generátort találni.")

# 2. Paraméterek mentése fájlba
def save_dh_params(filename, p, q, g):
    with open(filename, "w") as f:
        f.write(f"{p}\n{q}\n{g}\n")

# 3. Schnorr aláírás
def schnorr_sign(message: bytes, p, q, g, x):
    k = random.randint(1, q - 1)
    r = pow(g, k, p)
    r_bytes = r.to_bytes((p.bit_length() + 7) // 8, "big")
    e = int.from_bytes(hashlib.sha256(r_bytes + message).digest(), "big") % q
    s = (k + x * e) % q
    return (e, s)

# 4. Schnorr ellenőrzés
def schnorr_verify(message: bytes, e, s, p, q, g, y):
    gs = pow(g, s, p)
    ye = pow(y, e, p)
    r_check = (gs * number.inverse(ye, p)) % p
    r_bytes = r_check.to_bytes((p.bit_length() + 7) // 8, "big")
    e_check = int.from_bytes(hashlib.sha256(r_bytes + message).digest(), "big") % q
    return e == e_check

# 5. Főprogram
if __name__ == "__main__":
    print("2048 bites DH paraméterek generálása...")
    p, q, g = generate_dh_params()
    save_dh_params("dh_params.txt", p, q, g)
    print("Paraméterek elmentve fájlba: dh_params.txt")

    # Kulcspár generálása
    x = random.randint(1, q - 1)  # privát kulcs
    y = pow(g, x, p)              # publikus kulcs

    # Teszt üzenet (bármilyen bináris adat lehet)
    message = b"Schnorr test message: digital signature on this content."

    # Aláírás
    e, s = schnorr_sign(message, p, q, g, x)
    print(f"Aláírás kész!\n  e = {e}\n  s = {s}")

    # Ellenőrzés
    valid = schnorr_verify(message, e, s, p, q, g, y)
    print("Az aláírás helyes." if valid else "Az aláírás hibás.")


# EZ SE MEGY JOL