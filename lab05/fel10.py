import os
import time
from Crypto.Cipher import AES
from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes
import matplotlib.pyplot as plt

# ---- Konstansok ----
FILE_SIZES = [1 * 1024 * 1024, 10 * 1024 * 1024, 100 * 1024 * 1024]  # 1MB, 10MB, 100MB
KEY_AES = get_random_bytes(32)  # AES-256 kulcs
KEY_SALSA = get_random_bytes(32)  # Salsa20 kulcs
IV_AES = get_random_bytes(16)  # AES IV

def generate_random_file(filename, size):
    """Véletlenszerű fájl generálása a megadott mérettel"""
    with open(filename, "wb") as f:
        f.write(os.urandom(size))

def encrypt_AES(data):
    """AES-256 CBC titkosítás"""
    cipher = AES.new(KEY_AES, AES.MODE_CBC, IV_AES)
    padded_data = data + b"\x00" * (16 - len(data) % 16)  # Padding
    return cipher.encrypt(padded_data)

def encrypt_Salsa20(data):
    """Salsa20 titkosítás"""
    cipher = Salsa20.new(key=KEY_SALSA)
    return cipher.nonce + cipher.encrypt(data)

def measure_encryption_time():
    """Titkosítási sebességek mérése különböző fájlméreteken"""
    aes_times = []
    salsa_times = []

    for size in FILE_SIZES:
        filename = f"test_{size}.bin"
        generate_random_file(filename, size)

        with open(filename, "rb") as f:
            data = f.read()

        # AES időmérés
        start = time.time()
        encrypt_AES(data)
        aes_time = time.time() - start
        aes_times.append(aes_time)

        # Salsa20 időmérés
        start = time.time()
        encrypt_Salsa20(data)
        salsa_time = time.time() - start
        salsa_times.append(salsa_time)

        print(f"{size // (1024*1024)}MB - AES: {aes_time:.4f} sec, Salsa20: {salsa_time:.4f} sec")

    return aes_times, salsa_times

# ---- Teszt futtatása ----
aes_times, salsa_times = measure_encryption_time()

# ---- Grafikon megjelenítése ----
plt.figure(figsize=(8, 5))
plt.plot([size // (1024*1024) for size in FILE_SIZES], aes_times, marker="o", label="AES-256 CBC")
plt.plot([size // (1024*1024) for size in FILE_SIZES], salsa_times, marker="s", label="Salsa20")
plt.xlabel("Fájlméret (MB)")
plt.ylabel("Titkosítási idő (másodperc)")
plt.title("AES-256 vs. Salsa20 Titkosítási Idő")
plt.legend()
plt.grid()
plt.show()
