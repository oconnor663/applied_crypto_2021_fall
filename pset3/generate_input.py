#! /usr/bin/env python3

import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import json
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


def random_string(length):
    return random_animals(length)[:length]


def xor_bytes(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


def AES_encrypt_block(key, block):
    assert len(key) == 16
    assert len(block) == 16
    return Cipher(algorithms.AES(key), modes.ECB()).encryptor().update(block)


inputs = {}

# Problem 1
inputs["problem1"] = random_string(16)

# Problem 2
key = b"A" * 16
inputs["problem2"] = AES_encrypt_block(key, random_string(16).encode()).hex()

# Problem 3
plaintext_len = (secrets.randbelow(4) + 2) * 16
plaintext = random_string(plaintext_len)
assert len(plaintext) % 16 == 0
inputs["problem3"] = plaintext

# Problem 4
plaintext_len = (secrets.randbelow(3) + 2) * 16
plaintext = random_string(plaintext_len)
assert len(plaintext) % 16 == 0
ciphertext = (
    Cipher(algorithms.AES(key), modes.ECB()).encryptor().update(plaintext.encode())
)
assert len(plaintext) == len(ciphertext)
inputs["problem4"] = ciphertext.hex()

# Problem 5
inputs["problem5"] = [
    s.encode().hex()
    for s in [
        "z" * 15,
        random_animals(3),
        random_animals(4),
        "z" * 32,
    ]
]

# Problem 6
strings = [random_animals(3).encode().hex() for _ in range(3)]
inputs["problem6"] = []
for i in range(len(strings)):
    s = bytes.fromhex(strings[i])
    padding = 16 - (len(s) % 16)
    s += bytes([padding] * padding)
    inputs["problem6"].append(s.hex())

# Problem 7
lyrics = "John Jacob Jingleheimer Schmidt! His name is my name too. Whenever we go out the people always shout there goes John Jacob Jingleheimer Schmidt! Nanananananana..."
inputs["problem7"] = {
    "lyrics": lyrics,
    "key": secrets.token_bytes(16).hex(),
}

# Problem 8
inputs["problem8"] = {
    "key": secrets.token_bytes(16).hex(),
    "nonce": secrets.token_bytes(12).hex(),
    "plaintext": random_animals(5),
}

# Problem 9
inputs["problem9"] = secrets.token_bytes(16).hex()

print(json.dumps(inputs, indent="  "))
