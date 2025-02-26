import sympy as sp
import math 

def myCode(x):
    return ord(x) - 65

def myDecode(x):
    return chr(x + 65)

if __name__ == '__main__':
    encrypted_text = "AOGWEPOFKHSVRWYUKDAZKVYYNGYPQFKAWROZIEATIYROLMYYOSNRLIACOFJAGIUT"
    decrypted_text = ""
    mod = 26
    key = sp.Matrix([[6, 13], [7, 8]])
    det = key.det() % mod
    if math.gcd(det, mod) != 1:
        print("nincs inverz determinans")
    else:
        det1 = pow(det, -1, mod)
        keyA = key.adjugate()
        key1 = (keyA * det1) % mod
        print(key1)
        print((key * key1) % mod)

        for i in range(0, len(encrypted_text), 2):
            m1 = myCode(encrypted_text[i])
            m2 = myCode(encrypted_text[i + 1])
            m = sp.Matrix([[m1], [m2]])
            c = (key1 * m) % mod
            c1, c2 = myDecode(c[0]), myDecode(c[1])
            decrypted_text += c1 + c2

    if decrypted_text != "":
        print(decrypted_text)

    