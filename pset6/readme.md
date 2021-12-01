# Coding Problem Set 6:<br>Asymmetric Encryption and Signing

Example input:

```json
{
  "problem1": "9e05900de9e1a6f575768c274562b7155c05d856f804b993172942cfabb1e716",
  "problem2": "bdb323116f131971e3a7014aae30a23f5a7862e25b1ea21d23e4df7628a974f7bf1763d9ea39480f2001c31c7c4dbfb8106f04b9",
  "problem3": null,
  "problem4": "hippopotamus dog pig unicorn narwhal",
  "problem5": {
    "candidates": [
      "quail butterfly dog fox manatee",
      "sheep vulture llama kangaroo zebra",
      "wombat aardvark pig elephant aardvark",
      "wombat aardvark octopus butterfly dog",
      "aardvark dog elephant octopus dog"
    ],
    "signing_public_key": "45588a131029f816f3767ca7b8090c3612fff11e9f91e96966e21b087b2acb90",
    "signature": "33e0008377d23e8abc661cd5445599f83411479210a5e1dda04195773e0ec682d0c06c0863c536456900b2a85d97753560283d8ed38f9453c2bb225fb494b506"
  }
}
```

Example output:

```json
{
  "problem1": "8e8577fc3b3b408133da62be6c1ead25728f6d1e9d64df42dbd90a",
  "problem2": "jaguar narwhal kangaroo llama iguana",
  "problem3": "d68cf934ecfb1f21f783c3f289a8571f3f2558b3312a511e3c905f566d3b3ab0",
  "problem4": "e97ebf97133badb40e1b10fe6bf35676e9ed8584e6a25e8a098504f6b9a12216c45fb15e0fdd11e9fdc4f8c08541fa38603bc432f9aa4e4b01687b952bd5b60e",
  "problem5": "wombat aardvark octopus butterfly dog"
}
```

## Problem 1: Encrypting with `Box`

The headline feature of the original NaCl library is
[`Box`](https://pynacl.readthedocs.io/en/latest/public/), or
[`crypto_box`](https://libsodium.gitbook.io/doc/public-key_cryptography/authenticated_encryption)
as it's called in C. It combines the XSalsa20 stream cipher and Poly1305 MAC
that we're familiar with, with elliptic curve Diffie-Hellman over Curve25519.
That's a lot of moving parts, but the API is surprisingly simple to use.

In practice, encrypting with `Box` is a lot like encrypting with `SecretBox`.
The difference is that rather than sharing one secet key, each party generates
their own public/private "keypair", and only the public halves of those
keypairs are shared. It's the magic of (elliptic curve) Diffie-Hellman that
makes this possible.

Before you dive into this problem, take a few minutes to read [the PyNaCl
documentation for `Box`](https://pynacl.readthedocs.io/en/latest/public/), and
review [the demo we did in
class](https://github.com/oconnor663/applied_crypto_2021_fall/blob/main/demos/asymmetric.py).
The code in that demo will be very similar to your solutions for all of these
problems, and we'll refer back to it several times.

For this problem, and for problems 2 and 3 below, use `b"A" * 32` as the bytes
of your private key. The demo used random private keys, so this is a little
different. Here's an example of constructing your `PrivateKey` using PyNaCl:

```python
>>> from nacl.public import PrivateKey
>>> my_keypair = PrivateKey(b"A" * 32)
>>> my_keypair
<nacl.public.PrivateKey object at 0x7f27cc958850>
>>> my_keypair.encode()
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
```

Constructing someone else's `PublicKey` is similar:

```python
>>> from nacl.public import PublicKey
>>> their_public_key = PublicKey(...)  # their public key bytes go here
>>> their_public_key
<nacl.public.PublicKey object at 0x7f27cc95ba90>
>>> their_public_key.encode()
...  # whatever public key bytes you input above
```

Refer back to [the PyNaCl documentation for
Box](https://pynacl.readthedocs.io/en/latest/public/) and [the demo we did in
class](https://github.com/oconnor663/applied_crypto_2021_fall/blob/main/demos/asymmetric.py)
for examples of using `Box`, `PrivateKey`, and `PublicKey` to encrypt a
message.

Your input for this problem is Alice's public key bytes, encoded as hex.
Hex-decode these and then construct a PyNaCl `PublicKey` object from them.
Using `Box` with your `PrivateKey` (from above), Alice's `PublicKey`, and the
nonce `b"B" * 24`, encrypt the message `b"hello world"` for Alice. Your output
for this problem should be the resulting ciphertext, encoded as hex.

**Input:** Alice's public key bytes, encoded as hex

**Output:** the hex-encoded `Box` ciphertext of the `b"hello world"` message

## Problem 2: Decrypting with `Box`

This is the inverse of problem 1 above. Alice has encrypted a message for you.
She used the same keypairs as above (but from her perspective, using her
private key and your public key) and the nonce `b"C" * 24`. Your input for this
problem is the hex-encoded ciphertext of Alice's message. Hex-decode it and
decrypt it using `Box`. Your output should be the resulting ASCII string.

**Input:** a hex-encoded `Box` ciphertext from Alice

**Output:** the decrypted plaintext, an ASCII string

## Problem 3: The Diffie-Hellman shared secret

The regular `Box` API keeps the Diffie-Hellman shared secret under the covers,
but we can get our hands on it by calling `Box(private_key,
public_key).encode()`. We might do this for performance reasons — the DH step
is often more expensive than the encryption step — or because we need the
shared secret for some more complex protocol.

Using the your private key and Alice's public key from above, obtain the shared
secret with `Box.encode`. Your output should be that shared secret, encoded as
hex. There isn't any new input for this problem.

**Input:** none

**Output:** the shared secret between you and Alice, encoded as hex

Once you've got the secret, try using it with `SecretBox` to decrypt the
ciphertext from problem 2, and also to encrypt the `b"hello world"` message
from problem 1. You'll find you get the same answers that you originally got
with `Box`. And that's what `Box(...).encrypt(...)` is doing: it's computing a
shared secret with elliptic curve Diffie-Hellman, and then it's using that
secret as a key for `SecretBox`.

## Problem 4: Signing

In addition to asymmetric encryption, PyNaCl (and libsodium and NaCl) also
support asymmetric signatures. Signing involves a public/private sender keypair
just like encryption does, but this time there's no recipient keypair, and the
signature is verifiable by anyone who has the sender's public key. The
algorithm under the covers is EdDSA, a variant of elliptic curve DSA, again
using Curve25519.

For encryption, we used PyNaCl's `PrivateKey` and `PublicKey` types. For
signing, our key types are called `SigningKey` and `VerifyKey`, but they work
similarly. Here's how you create a `SigningKey` from its bytes:

```python
>>> from nacl.signing import SigningKey
>>> my_keypair = SigningKey(b"D" * 32)
>>> my_keypair
<nacl.signing.SigningKey object at 0x7f1d4431ceb0>
>>> my_keypair.encode()
b'DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
```

See [the PyNaCl documentation for
`SigningKey`](https://pynacl.readthedocs.io/en/latest/signing/) and [the demo
we did in
class](https://github.com/oconnor663/applied_crypto_2021_fall/blob/main/demos/asymmetric.py)
for examples of using `SigningKey` to sign a message.

Your input for this problem is an ASCII string. Use the bytes `b"D" * 32` as
your private signing key, and construct the PyNaCl `SigningKey` object as in
the example above. Convert the input to ASCII bytes, and use your `SigningKey`
to sign those bytes. Your output should be the resulting 64-byte signature,
encoded as hex.

**Input:** an ASCII string to be signed

**Output:** the signature of that string, encoded as hex

## Problem 5: Verifying a signature

This is the inverse of problem 4 above. You have a list of messages, one of
which is from Alice, but you're not sure which one it is. You'll need to use
Alice's signature to figure out which message was actually written by her.

Constructing Alice's `VerifyKey` (that is, her signing public key) is similar
to the other keys we've constructed so far:

```python
>>> from nacl.signing import VerifyKey
>>> their_public_key = VerifyKey(...)  # their public key bytes go here
>>> their_public_key
<nacl.signing.VerifyKey object at 0x7f1d44541a90>
>>> their_public_key.encode()
...  # whatever public key bytes you input above
```

See [the PyNaCl documentation for
`VerifyKey`](https://pynacl.readthedocs.io/en/latest/signing/) and [the demo we
did in
class](https://github.com/oconnor663/applied_crypto_2021_fall/blob/main/demos/asymmetric.py)
for examples of using `VerifyKey` to verify a signature.

Your input for this problem is an object with three fields. The `"candidates"`
field contains a list of ASCII strings, only one of which has actually been
signed by Alice. The `"signing_public_key"` field contains the bytes of Alice's
public key, encoded as hex. And the `"signature"` field contains the bytes of
the signature that Alice made, encoded as hex. To figure out which candidate
message matches the signature, write a loop over all of them, and try to
validate Alice's signature against each one. Only one of them will succeed
(i.e. not throw an exception). Your output for this problem should be that one
authentic message.

You'll need to use the `try` and `except` keywords in Python. It might be
helpful to refer back to the solution of problem 5 from the first problem set,
where we wrote a similar loop.

**Input:** an object with three fields, `"candidates"`, `"signing_public_key"`, and `"signature"`

**Output:** the candidate message that matches that signature

## Conclusion

By this point we've collected quite a few tools in our cryptographic toolbox.
Here's some of the things we've learned how to do:

- encrypt things with a secret key using ciphers (XSalsa20 via `SecretBox`)
- authenticate things with a secret key using keyed hashes (Poly1305 via
  `SecretBox`)
- exchange secret keys over an insecure channel using Diffie-Hellman (ECDH via
  `Box`)
- sign things that anyone can verify (EdDSA via `SigningKey`)

As you read about TLS in Chapter 13, think about all the asymmetric operations
that happen during the handshake, and all the symmetric operations that happen
for each data record that comes after. These things are no longer magic to you.
Now you can do all of these things yourself. If you keep going with this, it
won't be long before you can write your own TLS implementation, or design an
entirely new protocol using the same basic building blocks.
