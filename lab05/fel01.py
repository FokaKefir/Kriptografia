import os
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes

# TEA kulcs (előre ismert)
TEA_KEY = [0x0123, 0x4567, 0x89ab, 0xcdef]
BLOCK_SIZE = 8  # TEA 64 bites (8 byte-os) blokkokkal dolgozik

mask = 0xFFFFFFFF

def encrypt_tea(L, R, Key):
    """TEA titkosítás egyetlen 64 bites blokkon"""
    delta = 0x9e3779b9
    sum = 0
    for _ in range(32):
        sum = (sum + delta) & mask
        L = (L + (((R << 4) + Key[0]) ^ (R + sum) ^ ((R >> 5) + Key[1]))) & mask
        R = (R + (((L << 4) + Key[2]) ^ (L + sum) ^ ((L >> 5) + Key[3]))) & mask
    return L, R

def decrypt_tea(L, R, Key):
    """TEA visszafejtés egyetlen 64 bites blokkon"""
    delta = 0x9e3779b9
    sum = (delta << 5) & mask
    for _ in range(32):
        R = (R - (((L << 4) + Key[2]) ^ (L + sum) ^ ((L >> 5) + Key[3]))) & mask
        L = (L - (((R << 4) + Key[0]) ^ (R + sum) ^ ((R >> 5) + Key[1]))) & mask
        sum = (sum - delta) & mask
    return L, R

def byte_to_lr(byte_block):
    """64 bites blokkot (8 byte) bont le bal és jobb részre"""
    L = int.from_bytes(byte_block[:4], "big")
    R = int.from_bytes(byte_block[4:], "big")
    return L, R

def lr_to_byte(L, R):
    """Bal és jobb részt visszaalakít 8 byte-os blokká"""
    return L.to_bytes(4, "big") + R.to_bytes(4, "big")

def decrypt_tea_ecb(infile, outfile):
    """TEA visszafejtés ECB módban (első 80 bájt érintetlen marad)"""
    with open(infile, "rb") as fin, open(outfile, "wb") as fout:
        header = fin.read(80)  # Első 80 bájt érintetlen
        fout.write(header)
        
        while block := fin.read(8):
            if len(block) < 8:  # Ha a blokk kisebb, pótoljuk
                block = block.ljust(8, b'\x00')
            
            L, R = byte_to_lr(block)
            L, R = decrypt_tea(L, R, TEA_KEY)
            fout.write(lr_to_byte(L, R))

def encrypt_des3_cbc(infile, outfile, key, iv):
    """Visszafejtett fájl újratitkosítása DES3-CBC módban"""
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    
    with open(infile, "rb") as fin, open(outfile, "wb") as fout:
        data = fin.read()
        
        # PKCS7 padding
        pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        data += bytes([pad_len] * pad_len)
        
        fout.write(iv)  # IV-t is elmentjük az elejére
        fout.write(cipher.encrypt(data))

def process_files():
    """Visszafejtés TEA-ECB módban, majd újratitkosítás DES3-CBC módban"""
    decrypted_file = "decrypted.bmp"
    encrypted_file = "encrypted_cbc.bmp"

    # TEA visszafejtés
    decrypt_tea_ecb("crypt.bmp", decrypted_file)
    print("TEA-ECB visszafejtés kész!")

    # DES3-CBC titkosítás
    key = get_random_bytes(24)  # DES3 kulcs (192 bit)
    iv = get_random_bytes(8)  # 8 bájtos IV
    encrypt_des3_cbc(decrypted_file, encrypted_file, key, iv)
    print("DES3-CBC titkosítás kész!")

    # Kulcs és IV mentése
    with open("des3_key_iv.txt", "wb") as f:
        f.write(key + iv)

    print("DES3 kulcs és IV mentve: des3_key_iv.txt")

if __name__ == "__main__":
    process_files()
