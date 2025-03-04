def recover_key(crypt_file, known_plaintext):
    """Visszanyeri a 16 bájtos kulcsot az ismert szövegrészlet alapján."""
    with open(crypt_file, "rb") as f:
        crypt_data = f.read(len(known_plaintext))  # Első 16 bájt beolvasása

    key = bytes([crypt_data[i] ^ known_plaintext[i] for i in range(16)])
    return key

def decrypt_file(crypt_file, output_file, key):
    """A teljes fájlt visszafejti a megtalált 16 bájtos kulccsal."""
    key_length = len(key)
    
    with open(crypt_file, "rb") as f_in, open(output_file, "wb") as f_out:
        crypt_data = f_in.read()
        
        decrypted_data = bytes([crypt_data[i] ^ key[i % key_length] for i in range(len(crypt_data))])
        
        f_out.write(decrypted_data)

# Ismert első 16 bájt
known_plaintext = b"<!DOCTYPE html>\n"

# 1. Kulcs visszanyerése
recovered_key = recover_key("cryptOTP", known_plaintext)
print(f"Visszanyert kulcs: {recovered_key.hex()}")

# 2. Fájl visszafejtése
decrypt_file("cryptOTP", "recovered.html", recovered_key)
print("A HTML fájl sikeresen visszafejtve: recovered.html")
