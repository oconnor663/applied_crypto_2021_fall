#! /usr/bin/env python3

from hashlib import md5, sha1, sha256, sha3_256
import json
from os import path
import sys


inputs = json.load(sys.stdin)
outputs = {}

# Problem 1
s1 = inputs["problem1"].encode()
outputs["problem1"] = {
    "md5": md5(s1).hexdigest(),
    "sha1": sha1(s1).hexdigest(),
    "sha256": sha256(s1).hexdigest(),
    "sha3_256": sha3_256(s1).hexdigest(),
}

# Problem 2
s2 = bytearray(s1)
s2[0] = ord("?")
outputs["problem2"] = {
    "md5": md5(s2).hexdigest(),
    "sha1": sha1(s2).hexdigest(),
    "sha256": sha256(s2).hexdigest(),
    "sha3_256": sha3_256(s2).hexdigest(),
}

# Problem 3
collision1, collision2 = inputs["problem3"]
assert collision1 != collision2
hash1 = md5(bytes.fromhex(collision1)).hexdigest()
hash2 = md5(bytes.fromhex(collision2)).hexdigest()
assert hash1 == hash2
outputs["problem3"] = hash1

# Problem 4
expected = "38762cf7f55934b34d179ae6a4c80cadccbb7f0a"
if path.exists("shattered-1.pdf"):
    bytes1 = open("shattered-1.pdf", "rb").read()
    bytes2 = open("shattered-2.pdf", "rb").read()
    assert bytes1 != bytes2
    assert sha1(bytes1).hexdigest() == sha1(bytes2).hexdigest()
    assert sha1(bytes1).hexdigest() == expected
outputs["problem4"] = expected

# Problem 5
initial_counter = inputs["problem5"]
counter = initial_counter
while True:
    counter_bytes = counter.to_bytes(8, "little")
    output = sha256(counter_bytes).hexdigest()
    if output.startswith("000000"):
        break
    counter += 1
outputs["problem5"] = {
    "lucky_hash": output,
    "tries": counter - initial_counter + 1,
}

# Output
print(json.dumps(outputs, indent="  "))
