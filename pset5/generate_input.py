#! /usr/bin/env python3

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
inputs["problem1"] = {
    "key": secrets.token_bytes(64).hex(),
    "message": random_animals(5),
}

# Problem 2
inputs["problem2"] = 32 + secrets.randbelow(64)

# Problem 3
inputs["problem3"] = random_animals(5)

# Problem 4
inputs["problem4"] = random_animals(5)

print(json.dumps(inputs, indent="  "))
