#! /usr/bin/env python3

import json
from nacl.exceptions import BadSignatureError
from nacl.public import Box, PrivateKey, PublicKey
from nacl.secret import SecretBox
from nacl.signing import SigningKey, VerifyKey
import secrets
import sys


inputs = json.load(sys.stdin)
outputs = {}

# Problem 1
my_keypair = PrivateKey(b"A" * 32)
alices_public_key = PublicKey(bytes.fromhex(inputs["problem1"]))
nonce1 = b"B" * 24
message1 = b"hello world"
ciphertext1 = Box(my_keypair, alices_public_key).encrypt(message1, nonce1).ciphertext
outputs["problem1"] = ciphertext1.hex()

# Problem 2
ciphertext2 = bytes.fromhex(inputs["problem2"])
nonce2 = b"C" * 24
plaintext2 = Box(my_keypair, alices_public_key).decrypt(ciphertext2, nonce2)
outputs["problem2"] = plaintext2.decode()

# Problem 3
shared_secret = Box(my_keypair, alices_public_key).encode()
outputs["problem3"] = shared_secret.hex()

# Some extra asserts to confirm that using this shared secret with SecretBox
# gives us the same results that we saw above with Box.
secretbox1 = SecretBox(shared_secret).encrypt(b"hello world", nonce1).ciphertext
assert ciphertext1 == secretbox1
secretbox2 = SecretBox(shared_secret).encrypt(plaintext2, nonce2).ciphertext
assert ciphertext2 == secretbox2

# Problem 4
my_signing_key = SigningKey(b"D" * 32)
message4 = inputs["problem4"]
outputs["problem4"] = my_signing_key.sign(message4.encode()).signature.hex()

# Problem 5
verify_key = VerifyKey(bytes.fromhex(inputs["problem5"]["signing_public_key"]))
signature = bytes.fromhex(inputs["problem5"]["signature"])
for candidate in inputs["problem5"]["candidates"]:
    try:
        verify_key.verify(candidate.encode(), signature)
        outputs["problem5"] = candidate
        break
    except BadSignatureError:
        pass
else:
    assert False, "the signature wasn't valid for any candidate"

print(json.dumps(outputs, indent="  "))
