#! /usr/bin/env python3

import binascii
import json
from nacl.secret import SecretBox
import secrets

# CAUTION: `random` isn't cryptographically secure. In general, prefer to use
# `secrets`. But `secrets` currently lacks a shuffle() function, so we just
# import that specific function from `random`.
from random import shuffle

inputs_obj = {}

# Problem 1
inputs_obj["problem1"] = [secrets.randbelow(10) + 1 for _ in range(5)]

# Problem 2
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


animals_answer = random_animals(5)
inputs_obj["problem2"] = animals_answer.encode().hex()

# Problem 3
animals_input = random_animals(5)
inputs_obj["problem3"] = animals_input

# Problem 4
plaintext = random_animals(5)
key = b"A" * 32
nonce = b"B" * 24
ciphertext = SecretBox(key).encrypt(plaintext.encode(), nonce).ciphertext
inputs_obj["problem4"] = ciphertext.hex()

# Problem 5
plaintext = random_animals(5)
key = b"C" * 32
nonce = b"D" * 24
ciphertext = SecretBox(key).encrypt(plaintext.encode(), nonce).ciphertext
ciphertext_list = [ciphertext.hex()]
for _ in range(9):
    ciphertext_list.append(secrets.token_bytes(len(ciphertext)).hex())
shuffle(ciphertext_list)
inputs_obj["problem5"] = ciphertext_list

print(json.dumps(inputs_obj, indent="  "))
