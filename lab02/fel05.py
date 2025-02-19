import math


def affin_decrypt(data, key, mod):
    a, b = key
    a_inv = pow(a, -1, mod)
    return bytes(a_inv * (d + mod - b) % mod for d in data)

if __name__ == '__main__':

    with open('cryptAffine', 'rb') as fin:
        encrypted_data = fin.read()

    mod = 256
    decrypted_data = None
    key = None

    for a in range(2, mod):
        if math.gcd(a, mod) != 1:
            continue

        for b in range(0, mod):
            d_data_head = affin_decrypt(encrypted_data[:2], (a, b), mod)
            if d_data_head[:2] == bytes([0xFF, 0xD8]):                
                decrypted_data = affin_decrypt(encrypted_data, (a, b), mod)
                key = (a, b)
                break
        if decrypted_data:
            break
    
    
    if decrypted_data:
        with open('decrypted.jpg', 'wb') as fout:
            fout.write(decrypted_data)

        print(f'Megfelelő kulcs: a={key[0]}, b={key[1]}')
    else:
        print("Nem találtunk megfelelő kulcsot.")

