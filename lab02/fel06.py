

if __name__ == '__main__':

    with open('cryptAffinPA', 'rb') as fin:
        encrypted_data = fin.read()

    mod = 256
    decrypted_data = None
    key = (113, 223)
    a, b = key

    for a1 in range(3, mod):
        if a * a1 % mod == 1:
            a_inv = a1
            break

    decrypted_data = bytes(a_inv * (d + mod - b) % mod for d in encrypted_data)

    if decrypted_data:
        with open('decryptedPA.jpg', 'wb') as fout:
            fout.write(decrypted_data)