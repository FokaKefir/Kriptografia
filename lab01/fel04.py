import os

def is_valid_text(data):
    """
    Ellenőrzi, hogy a szöveg csak nyomtatható ASCII karaktereket és \n (10) vagy \r (13) karaktereket tartalmaz-e.
    """
    return all(32 <= b <= 126 or b in (10, 13) for b in data)

def caesar_decrypt(data, key):
    """Végrehajtja a Caesar visszafejtést bájtokon."""
    return bytes((b - key) % 256 for b in data)

if __name__ == '__main__':
    input_file = 'cryptCaesar2'
    output_file = 'decrypted.txt'
    
    with open(input_file, 'rb') as fin:
        encrypted_data = fin.read()
    
    for key in range(256):  # Mivel bájtokon dolgozunk, az összes kulcsot (0-255) végig kell próbálni
        decrypted_data = caesar_decrypt(encrypted_data, key)
        
        if is_valid_text(decrypted_data):
            with open(output_file, 'wb') as fout:
                fout.write(decrypted_data)
            print(f'Megfelelő kulcs: {key}')
            break  # Megtaláltuk az eredeti állományt