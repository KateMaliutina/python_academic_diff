def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    if len(plaintext) != len(keyword):
        for i in range(0, len(plaintext) - len(keyword)):
            keyword = keyword + keyword[i]
    for i in range(0, len(plaintext)):
        if 64 < ord(plaintext[i]) < 91:
            if ord(keyword[i]) > 91:
                sm = ord(keyword[i]) - 32
            else:
                sm = ord(keyword[i])
            sym = sm - 65 + ord(plaintext[i])
            if sym > 90:
                sym = sym - 26
            ciphertext = ciphertext + chr(sym)
        elif 96 < ord(plaintext[i]) < 123:
            if ord(keyword[i]) < 96:
                sm = ord(keyword[i]) + 32
            else:
                sm = ord(keyword[i])
            sym = sm - 97 + ord(plaintext[i])
            if sym > 122:
                sym = sym - 26
            ciphertext = ciphertext + chr(sym)
        else:
            ciphertext = ciphertext + plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    if len(ciphertext) != len(keyword):
        for i in range(0, len(ciphertext) - len(keyword)):
            keyword = keyword + keyword[i]
    for i in range(0, len(ciphertext)):
        if 64 < ord(ciphertext[i]) < 91:
            if ord(keyword[i]) > 91:
                sm = ord(keyword[i]) - 32
            else:
                sm = ord(keyword[i])
            sym = ord(ciphertext[i]) - sm + 65
            if sym < 65:
                sym = sym + 26
            plaintext = plaintext + chr(sym)
        elif 96 < ord(ciphertext[i]) < 123:
            if ord(keyword[i]) < 96:
                sm = ord(keyword[i]) + 32
            else:
                sm = ord(keyword[i])
            sym = ord(ciphertext[i]) - sm + 97
            if sym < 97:
                sym = sym + 26
            plaintext = plaintext + chr(sym)
        else:
            plaintext = plaintext + ciphertext[i]
    return plaintext
