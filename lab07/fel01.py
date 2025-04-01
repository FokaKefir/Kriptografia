from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import secrets
import binascii

# Paraméterek
bit_length = 256  # minden prímszám 256 bites lesz
e = 65537

# 1. RSA kulcspár generálása kézzel
p = getPrime(bit_length)
q = getPrime(bit_length)
n = p * q
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

print(f"RSA modulus (n): {n.bit_length()} bit")

# 2. Véletlen ASCII szöveg generálása, ami belefér OAEP-be
rsa_bytes = n.bit_length() // 8
oaep_limit = rsa_bytes - 2 * 20 - 2  # SHA-1 hash miatt
message = ''.join(secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(oaep_limit))
m_bytes = message.encode()
m_int = bytes_to_long(m_bytes)

if m_int >= n:
    raise ValueError("A generált szöveg túl nagy az RSA modulushoz.")

print(f"\nEredeti üzenet: {message}")
print(f"Üzenet (int): {m_int}")
print(f"Üzenet hossza: {len(m_bytes)} bájt (OAEP max: {oaep_limit})")

# 3. Klasszikus RSA titkosítás
print("\nKlasszikus RSA titkosítás (5x):")
for i in range(5):
    c = pow(m_int, e, n)
    print(f"{i + 1}. titkosítás (hex): {hex(c)}")

# 4. RSA-OAEP titkosítás
print("\nRSA-OAEP titkosítás (5x):")
rsa_key = RSA.construct((n, e, d))
cipher_oaep = PKCS1_OAEP.new(rsa_key)  # SHA-1 a default

for i in range(5):
    ct = cipher_oaep.encrypt(m_bytes)
    print(f"{i + 1}. titkosítás (hex): {binascii.hexlify(ct).decode()}")

# 5. Visszafejtés ellenőrzése
# Klasszikus RSA
c_decrypted = pow(c, d, n)
decrypted_msg = long_to_bytes(c_decrypted)

print(f"\nKlasszikus RSA visszafejtett üzenet: {decrypted_msg.decode()}")

# RSA-OAEP
pt_oaep = cipher_oaep.decrypt(ct)
print(f"RSA-OAEP visszafejtett üzenet: {pt_oaep.decode()}")
