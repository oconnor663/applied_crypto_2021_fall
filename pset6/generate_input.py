#! /usr/bin/env python3

import json
from nacl.public import Box, PrivateKey
from nacl.signing import SigningKey
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
alice_keypair = PrivateKey.generate()
inputs["problem1"] = alice_keypair.public_key.encode().hex()

# Problem 2
message = random_animals(5).encode()
your_public_key = PrivateKey(b"A" * 32).public_key
inputs["problem2"] = (
    Box(alice_keypair, your_public_key).encrypt(message, b"C" * 24).ciphertext.hex()
)

# Problem 3
inputs["problem3"] = None

# Problem 4
inputs["problem4"] = random_animals(5)

# Problem 5
candidates = [random_animals(5) for _ in range(5)]
message = secrets.choice(candidates).encode()
signing_keypair = SigningKey.generate()
inputs["problem5"] = {
    "candidates": candidates,
    "signing_public_key": signing_keypair.verify_key.encode().hex(),
    "signature": signing_keypair.sign(message).signature.hex(),
}

print(json.dumps(inputs, indent="  "))
