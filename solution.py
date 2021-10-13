#! /usr/bin/env python3

from nacl.secret import SecretBox
import secrets
import sys
import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def AES_encrypt_block(key, block):
    assert len(key) == 16
    assert len(block) == 16
    # If you'd like to understand these two lines, come back after Problem 4.
    cipher = Cipher(algorithms.AES(key), modes.ECB(), default_backend())
    return cipher.encryptor().update(block)

def xor_bytes(a, b):
    assert len(a) == len(b)
    # the one-liner version, using a "generator expression" and the "zip iterator"
    return bytes(x ^ y for x, y in zip(a, b))

def AES_decrypt_block(key, block):
    assert len(key) == 16
    assert len(block) == 16
    # If you'd like to understand these two lines, come back after Problem 4.
    cipher = Cipher(algorithms.AES(key), modes.ECB(), default_backend())
    return cipher.decryptor().update(block)


inputs = json.load(sys.stdin)
outputs = {}

# Problem 1
'''
Your input is a 16-character ASCII string. 
Convert this string to bytes and encrypt it with the AES block cipher, using a key consisting of sixteen A bytes (b"A" * 16). 
Your output should be the encrypted block, encoded as hex.
'''
plaintext = inputs["problem1"].encode()
key = b"A" * 16
outputs["problem1"] = AES_encrypt_block(key, plaintext).hex()


# Problem 2
'''
Your input is a hex-encoded encrypted string, of the same form as your output in Problem 1. 
Hex-decode it and decrypt it with the AES block cipher using the same key. 
Your output should be the decrypted plaintext, an ASCII string.
'''
ciphertext = bytes.fromhex(inputs["problem2"])
key = b"A" * 16
outputs["problem2"] = AES_decrypt_block(key, ciphertext).decode()


# Problem 3
'''
 Implement ECB mode encryption by looping over 16-byte blocks of the input and encrypting each of them with the AES block cipher, 
 using the same key as above (b"A" * 16). 
 Your output should be the encrypted ciphertext, encoded as hex.
'''
plaintext = inputs["problem3"].encode()
key = b"A" * 16
blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
enc_blocks = ''.join([AES_encrypt_block(key,block).hex() for block in blocks])
outputs["problem3"] = enc_blocks

# Problem 4
'''
Your input is a hex-encoded encrypted string, of the same form as your output in Problem 3. 
Implement ECB mode decryption, this time by looping over 16-byte blocks of the ciphertext and decrypting each one, again using the same key. 
Your output should be the decrypted plaintext, an ASCII string.
'''
plaintext = bytes.fromhex(inputs["problem4"])
key = b"A" * 16
blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
enc_blocks = ''.join([AES_decrypt_block(key,block).decode() for block in blocks])
outputs["problem4"] = enc_blocks


# Problem 5
'''
Hex-decode each input string into bytes, pad its length to an even multiple of 16 using PKCS#7 padding, 
and re-encode the result as hex. Your output should be the list of these padded, hex-encoded strings.
'''
#bytes.fromhex(s).decode()
padded = []
for s in inputs["problem5"]:
    l = 16 - ((len(bytes.fromhex(s).decode())) % 16)
    if l == 0:
        l = 16
    padding = bytes([l]*l)
    padded.append((bytes.fromhex(s) + padding).hex())
outputs["problem5"] = padded


# Problem 6
'''
Decode each of the hex strings into bytes, undo the PKCS#7 padding, and convert the result into an ASCII string. 
Your input should be the list of these strings.
'''
unpadded = []
for enc_padded in inputs["problem6"]:
    padl = bytes.fromhex(enc_padded)[-1]
    unpadded_dec = bytes.fromhex(enc_padded)[:len(bytes.fromhex(enc_padded)) - padl].decode()
    unpadded.append(unpadded_dec)
outputs["problem6"] = unpadded





# # Problem 3
# ciphertext1, ciphertext2 = inputs["problem3"]
# plaintext_xor = xor_bytes(bytes.fromhex(ciphertext1), bytes.fromhex(ciphertext2))
# plaintext = xor_bytes(plaintext_xor, b"$" * len(plaintext_xor))
# outputs["problem3"] = plaintext.decode()
#
# # Problem 4
# key = b"A" * 32
# nonce = 0
# ciphertexts = []
# for p in inputs["problem4"]:
#     c = SecretBox(key).encrypt(p.encode(), nonce.to_bytes(24, "little")).ciphertext
#     ciphertexts.append(c.hex())
#     nonce += 1
# outputs["problem4"] = ciphertexts
#
# # Problem 5
# key = b"B" * 32
# nonce = 0
# plaintexts = []
# for c in inputs["problem5"]:
#     p = SecretBox(key).decrypt(bytes.fromhex(c), nonce.to_bytes(24, "little"))
#     plaintexts.append(p.decode())
#     nonce += 1
# outputs["problem5"] = plaintexts
#
# # Problem 6
# ciphertext1, ciphertext2 = inputs["problem6"]
# plaintext_xor = xor_bytes(bytes.fromhex(ciphertext1), bytes.fromhex(ciphertext2))
# plaintext = xor_bytes(plaintext_xor, b"$" * len(plaintext_xor))
# outputs["problem6"] = plaintext[16:].decode()
#
# # Problem 7
# key = b"C" * 32
# ciphertexts = []
# for p in inputs["problem7"]:
#     nonce = secrets.token_bytes(24)
#     c = SecretBox(key).encrypt(p.encode(), nonce).ciphertext
#     c = nonce + c
#     ciphertexts.append(c.hex())
# outputs["problem7"] = ciphertexts
#
# # Problem 8
# key = b"C" * 32
# plaintexts = []
# for c in inputs["problem8"]:
#     c = bytes.fromhex(c)
#     nonce = c[:24]
#     rest = c[24:]
#     p = SecretBox(key).decrypt(rest, nonce)
#     plaintexts.append(p.decode())
# outputs["problem8"] = plaintexts

# Output
print(json.dumps(outputs, indent="  "))