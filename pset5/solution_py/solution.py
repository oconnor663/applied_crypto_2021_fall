#! /usr/bin/env python3

from cryptography.hazmat.primitives.poly1305 import Poly1305
from cryptography.exceptions import InvalidSignature
from pure_salsa20 import xsalsa20_stream
from hashlib import sha256
import json
import secrets
import sys


def xor_bytes(a, b):
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


def hmac(key, message):
    ipad = b"\x36" * 64
    opad = b"\x5c" * 64
    padded_key = key + (b"\x00" * (64 - len(key)))
    first_input = xor_bytes(padded_key, ipad) + message
    second_input = xor_bytes(padded_key, opad) + sha256(first_input).digest()
    return sha256(second_input).digest()


# This is a test function. If you want to run it (and the other test below),
# install pytest with `pip install pytest` and then run `pytest solution.py`.
def test_hmac():
    from hmac import digest as builtin_hmac

    key = b"hello world"
    message = b"goodnight moon"
    assert hmac(key, message) == builtin_hmac(key, message, sha256)


def secretbox_encrypt(key, nonce, plaintext):
    assert len(key) == 32
    assert len(nonce) == 24
    stream = xsalsa20_stream(key, nonce, len(plaintext) + 32)
    encrypted = xor_bytes(stream[32:], plaintext)
    tag = Poly1305.generate_tag(stream[:32], encrypted)
    return tag + encrypted


def secretbox_decrypt(key, nonce, ciphertext):
    assert len(key) == 32
    assert len(nonce) == 24
    tag = ciphertext[:16]
    encrypted = ciphertext[16:]
    stream = xsalsa20_stream(key, nonce, len(encrypted) + 32)
    Poly1305.verify_tag(stream[:32], encrypted, tag)
    plaintext = xor_bytes(stream[32:], encrypted)
    return plaintext


# This is a test function. If you want to run it (and the other test above),
# install pytest with `pip install pytest` and then run `pytest solution.py`.
def test_secretbox():
    from nacl.secret import SecretBox

    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(24)
    plaintext = b"hello world"
    mine = secretbox_encrypt(key, nonce, plaintext)
    theirs = SecretBox(key).encrypt(plaintext, nonce).ciphertext
    assert mine == theirs
    assert plaintext == secretbox_decrypt(key, nonce, mine)
    bad_ciphertext = bytearray(mine)
    bad_ciphertext[-1] ^= 1
    try:
        secretbox_decrypt(key, nonce, bytes(bad_ciphertext))
        assert False, "should fail on the line above"
    except InvalidSignature:
        pass


def main():
    inputs = json.load(sys.stdin)
    outputs = {}

    # Problem 1
    key = bytes.fromhex(inputs["problem1"]["key"])
    message = inputs["problem1"]["message"].encode()
    outputs["problem1"] = hmac(key, message).hex()

    # Problem 2
    key = b"D" * 32
    nonce = b"E" * 24
    num_bytes = inputs["problem2"]
    outputs["problem2"] = xsalsa20_stream(key, nonce, num_bytes).hex()

    # Problem 3
    key = b"F" * 32
    message = inputs["problem3"].encode()
    outputs["problem3"] = Poly1305.generate_tag(key, message).hex()

    # Problem 4
    key = b"G" * 32
    nonce = b"H" * 24
    message = inputs["problem4"].encode()
    outputs["problem4"] = secretbox_encrypt(key, nonce, message).hex()

    print(json.dumps(outputs, indent="  "))


if __name__ == "__main__":
    main()
