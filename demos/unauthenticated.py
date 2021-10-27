#! /usr/bin/env python3

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def AES_CBC_encrypt(key, iv, plaintext):
    return (
        Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
        .encryptor()
        .update(plaintext)
    )


def AES_CBC_decrypt(key, iv, ciphertext):
    return (
        Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
        .decryptor()
        .update(ciphertext)
    )


def AES_CTR_encrypt(key, nonce, plaintext):
    return (
        Cipher(algorithms.AES(key), modes.CTR(nonce + b"\0" * 4), default_backend())
        .encryptor()
        .update(plaintext)
    )


def AES_CTR_decrypt(key, nonce, ciphertext):
    return (
        Cipher(algorithms.AES(key), modes.CTR(nonce + b"\0" * 4), default_backend())
        .decryptor()
        .update(ciphertext)
    )


def flip_bits(ciphertext):
    # Note that this function doesn't know or use the key!
    mutated = bytearray(ciphertext)
    mutated[27] ^= ord("d") ^ ord("n")
    mutated[28] ^= ord("a") ^ ord("o")
    mutated[29] ^= ord("w") ^ ord("o")
    return bytes(mutated)


def flip_bits_in_previous_block(ciphertext):
    # Note that this function doesn't know or use the key!
    mutated = bytearray(ciphertext)
    mutated[11] ^= ord("d") ^ ord("n")
    mutated[12] ^= ord("a") ^ ord("o")
    mutated[13] ^= ord("w") ^ ord("o")
    return bytes(mutated)


def main():
    plaintext = b"Our battle plan: attack at dawn!"

    print("===== CTR mode flipping bits =====")
    key = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    print("The plaintext:          ", plaintext)
    print()
    ciphertext = AES_CTR_encrypt(key, nonce, plaintext)
    print("The ciphertext:         ", ciphertext.hex())
    mutated = flip_bits(ciphertext)
    print("The modified ciphertext:", mutated.hex())
    print(80 * " " + "^ ^ ^")
    print("The resulting plaintext:", AES_CTR_decrypt(key, nonce, mutated))
    print()
    print()

    print("===== CBC mode flipping bits =====")
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    print("The plaintext:          ", plaintext)
    print()
    ciphertext = AES_CBC_encrypt(key, iv, plaintext)
    print("The ciphertext:         ", ciphertext.hex())
    mutated = flip_bits(ciphertext)
    print("The modified ciphertext:", mutated.hex())
    print(80 * " " + "^ ^ ^")
    print("The resulting plaintext:", AES_CBC_decrypt(key, iv, mutated))
    print()
    print()

    print("===== CBC mode flipping bits in the previous block =====")
    key = secrets.token_bytes(16)
    iv = secrets.token_bytes(16)
    print("The plaintext:          ", plaintext)
    print()
    ciphertext = AES_CBC_encrypt(key, iv, plaintext)
    print("The ciphertext:         ", ciphertext.hex())
    mutated = flip_bits_in_previous_block(ciphertext)
    print("The modified ciphertext:", mutated.hex())
    print(48 * " " + "^ ^ ^")
    print("The resulting plaintext:", AES_CBC_decrypt(key, iv, mutated))


if __name__ == "__main__":
    main()
