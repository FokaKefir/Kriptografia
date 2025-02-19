import string
import math
import re

def affin_decode(text, key, mod):
    a, b = key 
    a_inv = pow(a, -1, mod)

    abc = string.ascii_uppercase
    new_text = ""
    for c in text:
        if re.match(r'[A-Z]', c):
            ind = a_inv * (abc.index(c) + mod - b) % mod
            new_text += abc[ind]
        else:
            new_text += c
    return new_text

if __name__ == '__main__':
    text = "EX GKLGTGWRGW BE HGDPGAODRG KIRZEX EKIH WIVERREW, RGK VEDRE E PEVOWTE. BGTEWDGIHYAX"
    mod = 26

    decoded_text = ""

    for a in range(2, mod):
        if math.gcd(a, mod) != 1:
            continue

        for b in range(0, mod):
            d_text = affin_decode(text, (a, b), mod)
            if d_text[:2] == 'AZ':
                decoded_text = d_text
                key = (a, b)
                break
        if decoded_text != '':
            break
    
    
    a, b = key
    print(f'a={a} b={b}')
    print(decoded_text)



