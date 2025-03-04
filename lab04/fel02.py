def xor_files(input1, input2, output):
    """Két bináris fájl XOR művelete és kiírás egy új fájlba."""
    with open(input1, "rb") as f1, open(input2, "rb") as f2, open(output, "wb") as fout:
        data1 = f1.read()
        data2 = f2.read()
        
        # Két fájl hosszát egyeztetni kell
        min_length = min(len(data1), len(data2))
        result = bytes([data1[i] ^ data2[i] for i in range(min_length)])

        fout.write(result)

# 1. Kulcs visszanyerése
xor_files("cryptOTP_Massag", "OTP_Massag.jpg", "recovered_key")

# 2. HB.docx visszafejtése
xor_files("cryptHB", "recovered_key", "HB.docx")

print("HB.docx sikeresen visszafejtve!")