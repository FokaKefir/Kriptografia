import sympy as sp
import math 

def invMat(key, mod):
    det = key.det() % mod
    if math.gcd(det, mod) != 1:
        print("nincs inverz determinans")
        return None
    else:
        det1 = pow(det, -1, mod)
        keyA = key.adjugate()
        key1 = (keyA * det1) % mod
        return key1
    
if __name__ == "__main__":
    mod = 256

    m = sp.Matrix([[0x28], [0x03]])
    c = sp.Matrix([[0x09], [0xb7]])

    mh = sp.Matrix([[0xff], [0xd9]])
    ch = sp.Matrix([[0xac], [0xfb]])

    mMat = sp.Matrix([[m[0], mh[0]], [m[1], mh[1]]])
    invMMat = invMat(mMat, mod)

    cMat = sp.Matrix([[c[0], ch[0]], [c[1], ch[1]]])
    key = (cMat * invMMat) % mod
    invKey = invMat(key, mod)

    with open("cryptHill", 'rb') as f:
        temp = f.read()

    lst = []

    for i in range(0, len(temp), 2):
        m = sp.Matrix([[temp[i]], [temp[i + 1]]])
        c = (invKey * m) % mod
        lst += c[0], c[1]
    d_data = bytes(lst)

    with open("d.jpg", "wb") as fout:
        fout.write(d_data)
        