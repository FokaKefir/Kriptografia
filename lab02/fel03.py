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
            ind = a_inv * (abc.index(c) + mod - b) % 26
            new_text += abc[ind]
        else:
            new_text += c
    return new_text



if __name__ == '__main__':
    text = "EX GKLGTGWRGW BE HGDPGAODRG KIRZEX EKIH WIVERREW, RGK VEDRE E PEVOWTE. BGTEWDGIHYAX"
    mod = 26

    texts = ""

    for a in range(2, mod):
        if math.gcd(a, mod) != 1:
            continue

        for b in range(0, 26):
            d_text = affin_decode(text, (a, b), mod)
            texts += f'a={a} b={b}\n' + d_text + "\n\n"


    with open('out03.txt', 'w') as fout:
        fout.write(texts)