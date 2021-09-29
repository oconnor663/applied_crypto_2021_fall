#! /usr/bin/env python3

from nacl.secret import SecretBox
import secrets
import sys
import json


def xor_bytes(a, b):
    assert len(a) == len(b)
    # the one-liner version, using a "generator expression" and the "zip iterator"
    return bytes(x ^ y for x, y in zip(a, b))


inputs = json.load(sys.stdin)
outputs = {}

# Problem 1
plaintext = inputs["problem1"].encode()
pad = secrets.token_bytes(len(plaintext))
outputs["problem1"] = {
    "pad": pad.hex(),
    "ciphertext": xor_bytes(plaintext, pad).hex(),
}

# Problem 2
pad = bytes.fromhex(inputs["problem2"]["pad"])
ciphertext = bytes.fromhex(inputs["problem2"]["ciphertext"])
outputs["problem2"] = xor_bytes(pad, ciphertext).decode()

# Problem 3
ciphertext1, ciphertext2 = inputs["problem3"]
plaintext_xor = xor_bytes(bytes.fromhex(ciphertext1), bytes.fromhex(ciphertext2))
plaintext = xor_bytes(plaintext_xor, b"$" * len(plaintext_xor))
outputs["problem3"] = plaintext.decode()

# Problem 4
key = b"A" * 32
nonce = 0
ciphertexts = []
for p in inputs["problem4"]:
    c = SecretBox(key).encrypt(p.encode(), nonce.to_bytes(24, "little")).ciphertext
    ciphertexts.append(c.hex())
    nonce += 1
outputs["problem4"] = ciphertexts

# Problem 5
key = b"B" * 32
nonce = 0
plaintexts = []
for c in inputs["problem5"]:
    p = SecretBox(key).decrypt(bytes.fromhex(c), nonce.to_bytes(24, "little"))
    plaintexts.append(p.decode())
    nonce += 1
outputs["problem5"] = plaintexts

# Problem 6
ciphertext1, ciphertext2 = inputs["problem6"]
plaintext_xor = xor_bytes(bytes.fromhex(ciphertext1), bytes.fromhex(ciphertext2))
plaintext = xor_bytes(plaintext_xor, b"$" * len(plaintext_xor))
outputs["problem6"] = plaintext[16:].decode()

# Problem 7
key = b"C" * 32
ciphertexts = []
for p in inputs["problem7"]:
    nonce = secrets.token_bytes(24)
    c = SecretBox(key).encrypt(p.encode(), nonce).ciphertext
    c = nonce + c
    ciphertexts.append(c.hex())
outputs["problem7"] = ciphertexts

# Problem 8
key = b"C" * 32
plaintexts = []
for c in inputs["problem8"]:
    c = bytes.fromhex(c)
    nonce = c[:24]
    rest = c[24:]
    p = SecretBox(key).decrypt(rest, nonce)
    plaintexts.append(p.decode())
outputs["problem8"] = plaintexts

# Output
print(json.dumps(outputs, indent="  "))
