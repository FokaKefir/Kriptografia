import os
import numpy as np

# Binaris fajlok generalasa kulonbozo meretekkel
file_sizes = {
    "test1.bin": 1024,        # 1 KB
    "test2.bin": 1024 * 100,  # 100 KB
    "test3.bin": 1024 * 1024, # 1 MB
    "test4.bin": 1024 * 10,   # 10 KB
    "test5.bin": 1024 * 500   # 500 KB
}

# Binaris fajlok letrehozasa
for file_name, size in file_sizes.items():
    with open(file_name, "wb") as f:
        f.write(os.urandom(size))  # Veletlenszeru bajtok

# A generalt fajlok listazasa
file_sizes
