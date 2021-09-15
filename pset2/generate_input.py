#! /usr/bin/env python3

import binascii
import json
from nacl.secret import SecretBox
import secrets

# CAUTION: `random` isn't cryptographically secure. In general, prefer to use
# `secrets`. But `secrets` currently lacks a shuffle() function, so we just
# import that specific function from `random`.
from random import shuffle

animals = [
    "aardvark",
    "butterfly",
    "cat",
    "dog",
    "elephant",
    "fox",
    "giraffe",
    "hippopotamus",
    "iguana",
    "jaguar",
    "kangaroo",
    "llama",
    "manatee",
    "narwhal",
    "octopus",
    "pig",
    "quail",
    "rhinoceros",
    "sheep",
    "turkey",
    "unicorn",
    "vulture",
    "wombat",
    "xenoceratops",
    "yak",
    "zebra",
]


def random_animals(n):
    return " ".join(secrets.choice(animals) for _ in range(n))


def xor_bytes(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


inputs_obj = {}

# Problem 1
inputs_obj["problem1"] = random_animals(3)

# Problem 2
plaintext = random_animals(3).encode()
pad = secrets.token_bytes(len(plaintext))
inputs_obj["problem2"] = {
    "pad": pad.hex(),
    "ciphertext": xor_bytes(plaintext, pad).hex(),
}

# Problem 3
plaintext2 = random_animals(3).encode()
plaintext1 = b"$" * len(plaintext2)
pad = secrets.token_bytes(len(plaintext2))
# Oops!
inputs_obj["problem3"] = [
    xor_bytes(plaintext1, pad).hex(),
    xor_bytes(plaintext2, pad).hex(),
]

# Problem 4
inputs_obj["problem4"] = [random_animals(3) for _ in range(3)]

# Problem 5
plaintexts = [random_animals(3).encode() for _ in range(3)]
ciphertexts = []
key = b"B" * 32
nonce = 0
for p in plaintexts:
    c = SecretBox(key).encrypt(p, nonce.to_bytes(24, "little")).ciphertext
    ciphertexts.append(c.hex())
    nonce += 1
inputs_obj["problem5"] = ciphertexts

# Problem 6
plaintext2 = random_animals(3).encode()
plaintext1 = b"$" * len(plaintext2)
key = secrets.token_bytes(32)
nonce = secrets.token_bytes(24)
# Oops!
inputs_obj["problem6"] = [
    SecretBox(key).encrypt(plaintext1, nonce).ciphertext.hex(),
    SecretBox(key).encrypt(plaintext2, nonce).ciphertext.hex(),
]

# Problem 7
inputs_obj["problem7"] = [random_animals(3) for _ in range(3)]

# Problem 8
plaintexts = [random_animals(3).encode() for _ in range(3)]
ciphertexts = []
key = b"C" * 32
for p in plaintexts:
    nonce = secrets.token_bytes(24)
    c = SecretBox(key).encrypt(p, nonce).ciphertext
    c = nonce + c
    ciphertexts.append(c.hex())
inputs_obj["problem8"] = ciphertexts

print(json.dumps(inputs_obj, indent="  "))
