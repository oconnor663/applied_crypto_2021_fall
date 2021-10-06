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


inputs = {}

# Problem 1
inputs["problem1"] = random_animals(3)

# Problem 2
inputs["problem2"] = None

# Problem 3
inputs["problem3"] = [
    "0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef",
    "0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef",
]
assert inputs["problem3"][0] != inputs["problem3"][1]

# Problem 4
inputs["problem4"] = None

# Problem 5
inputs["problem5"] = secrets.randbits(32)

print(json.dumps(inputs, indent="  "))
