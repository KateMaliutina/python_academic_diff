import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    keyword = chr(shift + 65)
    if ord(keyword) > 90:
        keyword = chr(ord(keyword) - 26)
    if len(plaintext) != len(keyword):
        for i in range(0, len(plaintext) - len(keyword)):
            keyword = keyword + keyword[i]
    for i in range(0, len(plaintext)):
        if 64 < ord(plaintext[i]) < 91:
            if ord(keyword[i]) > 91:
                sm = ord(keyword[i]) - 32
            else:
                sm = ord(keyword[i])
            my_sum = sm - 65 + ord(plaintext[i])
            if my_sum > 90:
                my_sum = my_sum - 26
            ciphertext = ciphertext + chr(my_sum)
        elif 96 < ord(plaintext[i]) < 123:
            if ord(keyword[i]) < 96:
                sm = ord(keyword[i]) + 32
            else:
                sm = ord(keyword[i])
            my_sum = sm - 97 + ord(plaintext[i])
            if my_sum > 122:
                my_sum = my_sum - 26
            ciphertext = ciphertext + chr(my_sum)

        else:
            ciphertext = ciphertext + plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    keyword = chr(shift + 65)
    if ord(keyword) > 90:
        keyword = chr(ord(keyword) - 26)
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


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    return best_shift
