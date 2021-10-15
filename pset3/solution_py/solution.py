#! /usr/bin/env python3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
import sys
import json


def xor_bytes(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


def AES_encrypt_block(key, block):
    assert len(key) == 16
    assert len(block) == 16
    # If you'd like to understand these two lines, come back after Problem 4.
    cipher = Cipher(algorithms.AES(key), modes.ECB(), default_backend())
    return cipher.encryptor().update(block)


def AES_decrypt_block(key, block):
    assert len(key) == 16
    assert len(block) == 16
    # If you'd like to understand these two lines, come back after Problem 4.
    cipher = Cipher(algorithms.AES(key), modes.ECB(), default_backend())
    return cipher.decryptor().update(block)


def AES_ECB_encrypt(key, plaintext):
    assert len(plaintext) % 16 == 0
    i = 0
    ciphertext = bytearray()
    while i < len(plaintext):
        ciphertext.extend(AES_encrypt_block(key, plaintext[i : i + 16]))
        i += 16
    # Check the ciphertext against the cryptography library's implementation of
    # ECB. These three lines are an "assert". This is me double checking my
    # work, for debugging purposes. You could remove these three lines without
    # changing the behavior of the function.
    assert ciphertext == Cipher(
        algorithms.AES(key), modes.ECB(), default_backend()
    ).encryptor().update(plaintext)
    return ciphertext


def AES_ECB_decrypt(key, ciphertext):
    assert len(ciphertext) % 16 == 0
    i = 0
    plaintext = bytearray()
    while i < len(ciphertext):
        plaintext.extend(AES_decrypt_block(key, ciphertext[i : i + 16]))
        i += 16
    # Check the plaintext against the cryptography library's implementation of
    # ECB. These three lines are an "assert". This is me double checking my
    # work, for debugging purposes. You could remove these three lines without
    # changing the behavior of the function.
    assert plaintext == Cipher(
        algorithms.AES(key), modes.ECB(), default_backend()
    ).decryptor().update(ciphertext)
    return plaintext


def PKCS7_pad(b):
    needed = 16 - (len(b) % 16)
    # This is the bytes([...]) syntax described in the text of Problem 5.
    return b + bytes([needed] * needed)


def PKCS7_unpad(b):
    # b[-1] would also work here.
    n = b[len(b) - 1]
    # Similarly, b[:-n] would also work here.
    return b[: len(b) - n]


def AES_CTR_stream(key, nonce, n):
    assert len(nonce) == 12
    output = bytearray()
    blocknum = 0
    remaining = n
    while remaining > 0:
        input_block = nonce + blocknum.to_bytes(4, "big")
        output_block = AES_encrypt_block(key, input_block)
        output.extend(output_block[:remaining])
        remaining -= 16
        blocknum += 1
    # Check the stream against the cryptography library's implementation of
    # CTR. These three lines are an "assert". This is me double checking my
    # work, for debugging purposes. You could remove these three lines without
    # changing the behavior of the function.
    assert output == Cipher(
        algorithms.AES(key), modes.CTR(nonce + b"\0" * 4), default_backend()
    ).encryptor().update(b"\0" * n)
    return output


def AES_CTR_xor(key, nonce, m):
    return xor_bytes(m, AES_CTR_stream(key, nonce, len(m)))


inputs = json.load(sys.stdin)
outputs = {}

# Problem 1
key = b"A" * 16
outputs["problem1"] = AES_encrypt_block(key, inputs["problem1"].encode()).hex()

# Problem 2
outputs["problem2"] = AES_decrypt_block(key, bytes.fromhex(inputs["problem2"])).decode()

# Problem 3
outputs["problem3"] = AES_ECB_encrypt(key, inputs["problem3"].encode()).hex()

# Problem 4
outputs["problem4"] = AES_ECB_decrypt(key, bytes.fromhex(inputs["problem4"])).decode()

# Problem 5
# This [ ... for X in ... ] pattern is called a "list comprehension".
# https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
# You could also use a regular for-loop here, calling .append() to build the
# list, as I do in Problem 9 below.
outputs["problem5"] = [PKCS7_pad(bytes.fromhex(s)).hex() for s in inputs["problem5"]]

# Problem 6
# This is another list comprehension, see above.
outputs["problem6"] = [
    PKCS7_unpad(bytes.fromhex(s)).decode() for s in inputs["problem6"]
]

# Problem 7
lyrics = inputs["problem7"]["lyrics"].encode()
key = bytes.fromhex(inputs["problem7"]["key"])
ciphertext = AES_ECB_encrypt(key, PKCS7_pad(lyrics)).hex()
outputs["problem7"] = {
    "ciphertext": ciphertext,
    "repeats": [ciphertext[0:32], ciphertext[32:64]],
}

# Problem 8
key = bytes.fromhex(inputs["problem8"]["key"])
nonce = bytes.fromhex(inputs["problem8"]["nonce"])
plaintext = inputs["problem8"]["plaintext"].encode()
outputs["problem8"] = AES_CTR_xor(key, nonce, plaintext).hex()

# Problem 9
key = bytes.fromhex(inputs["problem9"])
stream = AES_CTR_stream(key, b"\0" * 12, 40)
ints = []
for i in range(5):
    ints.append(int.from_bytes(stream[8 * i : 8 * i + 8], "little"))
outputs["problem9"] = ints

# Output
print(json.dumps(outputs, indent="  "))
