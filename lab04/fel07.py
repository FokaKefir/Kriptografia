from Crypto.Cipher import ChaCha20_Poly1305
import binascii

def verify_chacha20_poly1305(key, nonce, ciphertext, tag):
    """Ellenőrzi a ChaCha20-Poly1305 titkosítás hitelességét."""
    try:
        cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return True, plaintext.decode(errors="ignore")  # Visszafejtett szöveg
    except ValueError:
        return False, None  # Hitelesítés sikertelen

def process_poly1305_file(filename):
    """Beolvassa a poly1305.txt fájlt és ellenőrzi a hitelességet."""
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    for i in range(0, len(lines), 5):
        key = binascii.unhexlify(lines[i])       # Kulcs dekódolása
        nonce = binascii.unhexlify(lines[i+1])   # Nonce dekódolása
        ciphertext = binascii.unhexlify(lines[i+2])  # Titkosított szöveg dekódolása
        tag = binascii.unhexlify(lines[i+3])     # Hitelesítési tag dekódolása

        is_valid, plaintext = verify_chacha20_poly1305(key, nonce, ciphertext, tag)
        
        print(f"🔹 Blokk {i//5 + 1}: {'✅ Hiteles' if is_valid else '❌ Érvénytelen'}")
        if is_valid:
            print(f"  📜 Visszafejtett szöveg: {plaintext}")

if __name__ == "__main__":
    process_poly1305_file("poly1305.txt")
