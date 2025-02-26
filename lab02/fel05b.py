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

    c1, c2 = encrypted_data[:2]
    m1, m2 = 0xFF, 0xD8

    temp1, temp2 = pow(m1 - m2, -1, mod), c1 - c2
    a = (temp1 * temp2) & 255
    b = (c1 - (m1 * a)) & 255
    key = (a, b)

    decrypted_data = affin_decrypt(encrypted_data, key, mod)
    
    if decrypted_data:
        with open('decrypted.jpg', 'wb') as fout:
            fout.write(decrypted_data)

        print(f'Megfelelő kulcs: a={key[0]}, b={key[1]}')
    else:
        print("Nem találtunk megfelelő kulcsot.")

