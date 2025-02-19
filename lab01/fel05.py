import re
import string

# def decode(text, key):
#     abc = string.ascii_uppercase
#     new_text = ""
#     for c in text:
#         if re.match(r'[A-Z]', c):
#             ind = (abc.index(c) - key) % 26
#             new_text += abc[ind]
#         else:
#             new_text += c
#     return new_text

def decode(text, key):
    abc = string.ascii_letters + "? "
    shifted_abc = abc[key:] + abc[:key]  # Az ABC eltolása
    trans_table = str.maketrans(shifted_abc, abc)  # Fordított eltolás

    return text.translate(trans_table)

if __name__ == '__main__':
    with open('file05.txt', "r") as fin:
        text = fin.read()

    texts = ""

    for i in range(53):
        d_text = decode(text, i)
        texts += str(i) + "\n" + d_text + "\n\n"
    
    with open('out05.txt', 'w') as fout:
        fout.write(texts)

