#! /usr/bin/env python3
# fmt: off

from nacl.public import PrivateKey, Box
from nacl.secret import SecretBox
from nacl.signing import SigningKey

# =============== public key encryption with Diffie-Hellman ================
# ======== technically elliptic curve Diffie-Hellman over Curve25519 =======
#
# https://pynacl.readthedocs.io/en/latest/public/
# https://libsodium.gitbook.io/doc/public-key_cryptography/authenticated_encryption

keypair_alice = PrivateKey.generate()
print("alice private key:", keypair_alice.encode().hex())
print("alice  public key:", keypair_alice.public_key.encode().hex(), "\n")

keypair_bob = PrivateKey.generate()
print("  bob private key:", keypair_bob.encode().hex())
print("  bob  public key:", keypair_bob.public_key.encode().hex(), "\n")

message = b"hello world"
nonce = b"X" * 24

ciphertext_alice = Box(
    keypair_alice,
    keypair_bob.public_key,
).encrypt(message, nonce).ciphertext
print("alice encrypts:", ciphertext_alice.hex())
ciphertext_bob = Box(
    keypair_bob,
    keypair_alice.public_key,
).encrypt(message, nonce).ciphertext
print("  bob encrypts:", ciphertext_bob.hex(), "\n")

# ========== "Box" is actually a thin wrapper around "SecretBox" ==============

shared_secret = Box(keypair_alice, keypair_bob.public_key).encode()
print("shared secret:", shared_secret.hex(), "\n")

secretbox_ciphertext = SecretBox(shared_secret).encrypt(message, nonce).ciphertext
print("secretbox ciphertext:", secretbox_ciphertext.hex(), "\n")

print("-------------------------------------\n")

# =================== public key signing ===============================
# ======== technically elliptic curve DSA over Ed25519 =================
#
# https://pynacl.readthedocs.io/en/latest/signing/
# https://libsodium.gitbook.io/doc/public-key_cryptography/public-key_signatures

signing_keypair = SigningKey.generate()
print("signing private key:", signing_keypair.encode().hex())
print("signing  public key:", signing_keypair.verify_key.encode().hex(), "\n")

signature = signing_keypair.sign(message).signature

print("signature:", signature.hex(), "\n")

print('verifying the signature against "hello world"...')
signing_keypair.verify_key.verify(b"hello world", signature)
print("ok", "\n")

print('verifying the signature against "jello world"...')
# This line will throw an exception.
signing_keypair.verify_key.verify(b"jello world", signature)
