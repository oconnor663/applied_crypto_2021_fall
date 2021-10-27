#! /usr/bin/env python3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
import string
import sys
import time


SECRET_KEY = secrets.token_bytes(16)


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def PKCS7_pad(b):
    needed = 16 - (len(b) % 16)
    return b + bytes([needed] * needed)


def AES_CBC_encrypt(iv, plaintext):
    padded = PKCS7_pad(plaintext)
    return (
        Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), default_backend())
        .encryptor()
        .update(padded)
    )


def is_padding_valid(iv, ciphertext):
    padded = (
        Cipher(algorithms.AES(SECRET_KEY), modes.CBC(iv), default_backend())
        .decryptor()
        .update(ciphertext)
    )
    n = padded[-1]
    return 0 < n and n <= 16 and padded.endswith(bytes([n] * n))


def pretty_print(candidate):
    c = chr(candidate)
    printable = set(string.ascii_letters + string.digits + string.punctuation)
    if c not in printable:
        c = "�"
    print(c, end="")
    sys.stdout.flush()
    time.sleep(0.01)


def padding_oracle_attack(iv, ciphertext):
    # Note that this function does *not* look at SECRET_KEY! It only calls
    # is_padding_valid().

    # Note that we discover bytes starting at the end and working back, so this
    # list of discovered bytes is in reverse order compared to the plaintext.
    discovered = []

    # Loop over each byte in the last block, starting from the back.
    for discovery_i in range(16):
        # Using all the bytes we've discovered so far, tweak the penultimate
        # block to change the padding of the final block.
        print("trying: ", end="")
        target_padding_byte = discovery_i + 1
        penultimate_block = ciphertext[-32:-16]
        repadded_block = bytearray(penultimate_block)
        for padding_i in range(discovery_i):
            padding_mask = discovered[padding_i] ^ target_padding_byte
            repadded_block[15 - padding_i] ^= padding_mask
        # Now the byte we want to discover appears to be the first padding
        # byte. Tweak its value (again by modifying the penultimate block)
        # until the padding is valid.
        for candidate_byte in range(256):
            pretty_print(candidate_byte)
            candidate_block = bytearray(repadded_block)
            candidate_mask = candidate_byte ^ target_padding_byte
            candidate_block[15 - discovery_i] ^= candidate_mask
            modified_ciphertext = bytearray(ciphertext)
            modified_ciphertext[-32:-16] = candidate_block
            if is_padding_valid(iv, modified_ciphertext):
                # We found a byte value that leads to valid padding. This
                # confirms the value of the byte we were trying to discover.
                # Make a note of it, move on to the next byte.
                discovered.append(candidate_byte)
                print(
                    f"\n{bytes([candidate_byte])} in position {15 - discovery_i} is valid"
                )
                break
        else:
            assert False, "the candidate loop should always break"

    discovered.reverse()
    print("found last block:", bytes(discovered))


def main():
    message = b"Our battle plan: attack at dawn"
    iv = secrets.token_bytes(16)
    ciphertext = AES_CBC_encrypt(iv, message)

    padding_oracle_attack(iv, ciphertext)


if __name__ == "__main__":
    main()
