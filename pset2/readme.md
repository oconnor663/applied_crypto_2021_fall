# Coding Problem Set 2: Randomness

A 13m31s walkthrough of the new autograder output and some common JSON mistakes to avoid:

<a href="http://www.youtube.com/watch?v=ggxynlq6FmM">
  <img src="http://img.youtube.com/vi/ggxynlq6FmM/maxresdefault.jpg" alt="walkthrough video" width="400">
</a>

Example input:

```json
{
  "problem1": "sheep cat rhinoceros",
  "problem2": {
    "pad": "ee4a1c78ed39161f52e51c11a85fd3ed9893af3fd093acc30d",
    "ciphertext": "9925711a8c4d367d27916874da39bf94b8f8ce51b7f2deac62"
  },
  "problem3": [
    "9a31167bc4cd24dd95aa4d53e6d938ac8d184b43d1dfd1e7bbaa1b7c1c06",
    "c6705c30838c7298c5e11904e2937dfade540e0bd59980b7ebeb4d3e545b"
  ],
  "problem4": [
    "iguana jaguar cat",
    "turkey narwhal turkey",
    "aardvark llama iguana"
  ],
  "problem5": [
    "56fd5c6607ab3e356e759351745c6dd44d03c045c318e25ff351a937f56b29405d1d9f",
    "c07bf0b21831c709fa15f487c5cc25d60390ca307e1ae230055f2a6865e0d2620d9f8669af42aec6a1cf755e518c19",
    "6f7e2e7c0c3eab29a45d3d4379706095a53356927033dad827915cda1fb7a62c46d4"
  ],
  "problem6": [
    "cd7e1bef27f766976efd1ee3d73584152f78f10ed72daac831449e706c554cb985d8f276e0270014",
    "ee1baa3829a2cc481346874fce414ff2663dbb4b876cebcc6315d6203d030dbdc490b322ac624a44"
  ],
  "problem7": [
    "giraffe butterfly dog",
    "wombat unicorn fox",
    "hippopotamus xenoceratops manatee"
  ],
  "problem8": [
    "f67c3f2187514cbdcd2eae87dc6bbed4cbce07a8327f9dbd1dedabde2b6568a25249c771cb1621555875a2085e0f03e99aebf84eb2",
    "00a4ec1dd07ba36a3d5e1b73b0598ac709d3552306fdecb3e8317c828aca50518ebed8c1727cb585baaf0b16c028ab5fd1d55db6ea8ef8d8a5",
    "b5ab7b32b10c2a3f5953d45c73f4bd7c63196eaef87edfb0dd688d3c123d3acbf3a5633cbbaa815ffca5e5a4db8273316f14bc737d02cb7e91"
  ]
}
```

Example output:

```json
{
  "problem1": {
    "pad": "9fe23b4361f637cbd3ae10a281be212982fd2b14",
    "ciphertext": "ec8a5e2611d654aaa78e62cae8d04e4ae78f4467"
  },
  "problem2": "wombat butterfly kangaroo",
  "problem3": "xenoceratops narwhal butterfly",
  "problem4": [
    "a1387edae3d03643204b1eb86039d604f62b8e942598980ffd4c1f5c9811472a9c",
    "e5b89aad267e7c369e53326e200a503aed06b26599803086719b5f0b22aedd9b639e700cfd",
    "c7453a9d3c5a73f0a8e7ef407f9ae569a824bd57f493fad81c083414aacd13cb76e3d89f41"
  ],
  "problem5": [
    "yak kangaroo jaguar",
    "hippopotamus vulture rhinoceros",
    "quail llama iguana"
  ],
  "problem6": "manatee vulture elephant",
  "problem7": [
    "23338577c487823367c70c680086b7d3d24cc223fb1b382fc3d1e24115057879b2758dc0e4e0036fbeb66abfcda16dfe38c7789b7c8712465b0b7c0ac1",
    "6482625c19ce2fb575ed8cb5999fe5064f601349770f2f559461d5d31655f0a744496ebd1119b49c8cc37c5991c049552b7a2674fb509cc4085a",
    "844c0f7dfffb47e2e50a41ef8736fc6b6e586e7cea1395ac55b437bc1493ae1ec054eb1a1521b41a0c59371e201e9bb0cd5f90d1025a74867ee1134555d8c811fa83f4be153337dccd"
  ],
  "problem8": [
    "fox yak sheep",
    "pig llama narwhal",
    "vulture dog quail"
  ]
}
```

## Problem 1: one-time pad encryption

In the last problem set, we got started with secretbox decryption. We'll get
back to secretbox in the second half of this problem set, but first let's do a
few exercises with one-time pads. We don't often use one-time pads in practice,
but they do work, and understanding how they work will be helpful when we get
to stream ciphers in Chapter 5 of *Serious Cryptography*. They're also a good
place to get started with randomness.

Your input is a plaintext string. Generate a random one-time pad of the same
length as the string. In Python, use
[`secrets.token_bytes`](https://docs.python.org/3/library/secrets.html#secrets.token_bytes)
for this. Encrypt the string, by xor'ing (`^`) each byte of the string with the
corresponding byte of the pad. Your output should be an object with two fields,
`"pad"` containing the hex-encoded pad that you generated, and `"ciphertext"`
containing the hex-encoded result of encryption.

You can write a [one-liner](https://stackoverflow.com/a/29409299/823869) for
xor'ing `bytes` or `bytearray` objects in Python, if you're comfortable with
iterators and "generator expressions". But here's the simplest way to do it:

```python
def xor_bytes(a, b):
    assert len(a) == len(b)
    output = bytearray(len(a))
    for i in range(len(a)):
        output[i] = a[i] ^ b[i]
    return output
```

Because this problem involves generating your own randomness, the grading
program won't expect your outputs to be equal to anything in particular.
Instead, it'll check that it when it decrypts your ciphertext using your pad,
the original input comes back out.

**Input:** an ASCII string to be encrypted

**Output:** an object with two fields, `"pad"` and `"ciphertext"`, each hex-encoded strings

**CAUTION:** As we've discussed in class, there's a crucial difference between
"cryptographic" and "non-cryptographic" random number generators. The latter
have output which _looks_ random, but they can be predictable if you know how
they work. Unfortunately, the standard randomness functions in many popular
programming languages are non-cryptographic, and these legacy APIs usually
can't be fixed without breaking backwards compatibility. The best we can do is
document them with scary warnings, like this one from Python's
[`random`](https://docs.python.org/3/library/random.html) module:

> **Warning:** The pseudo-random generators of this module should not be used
> for security purposes. For security or cryptographic uses, see the
> [`secrets`](https://docs.python.org/3/library/secrets.html#module-secrets)
> module.

But of course [no one reads warnings](https://youtu.be/LeFYiHsPpug?t=530), and
using non-cryptographic RNGs in a cryptographic setting remains a common
mistake. When you're reviewing crypto code, this is one of the first things you
should check. From now on, whenever you see a function with "random" in its
name, always ask yourself, "Is this cryptographic randomness or not?"

## Problem 2: one-time pad decryption

This is the inverse of Problem 1. Your input is an object with two hex-encoded
fields, `"pad"` and `"ciphertext"`, of the same form as your output above.
Hex-decode those strings and decrypt the ciphertext by xor'ing it with the pad.
Your output should be the resulting plaintext, as an ASCII string.

When you're done, notice how your decryption code in this problem looks just
like your encryption code in the previous problem. That's interesting. Keep
that symmetry in mind for the next problem.

**Input:** an object with two fields, `"ciphertext"` and `"pad"`, each hex-encoded strings

**Output:** the decrypted plaintext, an ASCII string

## Problem 3: What happens when you reuse a one-time pad?

One-time pads have a fundamental rule, which is right there in the name: You
can only use a given pad once. To get a sense of just how important this rule
is, let's see what happens when we break it.

Your input is two hex-encoded ciphertexts of the same length, which have been
encrypted with the same one-time pad. (Oops!) You don't know anything about the
pad, but you do know that the first plaintext consists entirely of `$` (0x24)
characters. Using just this fact, *decrypt the second plaintext.*

Remember that for any byte (or bit or int) `x`, we know that `x ^ 0 == x` and
`x ^ x == 0`. If this is your first time seeing these rules, play with an
example or two to convince yourself that they work. When faced with a more
complicated expression like `a ^ p ^ b ^ p`, we can rearrange it like this:

```
a ^ p ^ b ^ p == a ^ b ^ p ^ p
              == a ^ b ^ 0
              == a ^ b
```

If `a` and `b` here represent two plaintext bytes, and `p` represents a pad
byte, then this xor procedure will "cancel out the pad". (Then you have to
figure out what to do with `a ^ b`.) An alternative approach to this problem is
to figure out how to "recover the pad" from the first plaintext. (Then you can
decrypt the second ciphertext as you did in Problem 2 above.) If you have time,
experiment with both approaches.

**Input:** a list of two hex-encoded ciphertexts of the same length

**Output:** the second decrypted plaintext, an ASCII string

When you've finished this problem, take a moment to appreciate the impact of
what you've done. In theory, one-time pads provide _perfect secrecy_. In
practice, if we use them incorrectly, we get no secrecy whatsoever. Now you
know why. Think about how easy it would be to make a mistake like this. All it
takes is a one-letter typo; maybe someone accidentally types `pad1` when they
mean `pad2`. What's worse, look at the ciphertexts themselves. Do they look
broken? I certainly can't tell. To me, they look just as random as anything
else. This is why crypto is hard: It's easy to make mistakes like this, and
it's hard to notice our mistakes until someone exploits them.

## Problem 4: secretbox encryption with a sequential nonce

Ok, let's get back to secretbox, which we met in the first problem set.
Practical ciphers like secretbox are less restrictive than one-time pads. They
let us reuse the same secret key to encrypt many messages. To make this work,
they accept an extra parameter called a "nonce". (You can remember this as a
"number" that you only use "once", but that's [probably not the actual origin
of the word](https://en.wiktionary.org/wiki/nonce#Etymology_1).) The
fundamental rule of nonces, similar to the fundamental rule of one-time pads,
is that we must never reuse the same nonce with the same key. Luckily, our
nonces don't need to be secret, just unique.

The simplest way to encrypt many secretbox messages with the same key is to use
a counter nonce. The first message gets nonce 0, the second message gets nonce
1, and so on. The secretbox nonce parameter is 24 bytes long, so we're
certainly not going to overflow this counter anytime soon. (Take a moment to
figure out how many years it would take to overflow a 24-byte counter if you
encrypted one message every second.)

Your input for this problem is a list of strings. Encrypt each string using
[`nacl.secret.SecretBox.encrypt`](https://pynacl.readthedocs.io/en/latest/secret/#nacl.secret.SecretBox.encrypt)
(in Python/PyNaCl) or any other equivalent of the libsodium
[`crypto_secretbox_easy`](https://doc.libsodium.org/secret-key_cryptography/secretbox)
function. The key for every message is thirty-two `A` (0x41) bytes. For the
nonce, use an incrementing counter, 0 for the first string, 1 for the second
string, and so on. Encode each counter value as twenty-four bytes in
[little-endian order](https://en.wikipedia.org/wiki/Endianness), that is `[0,
0, ..., 0]`, `[1, 0, ..., 0]`, and so on. In Python, if you have an integer
variable called `counter`, you can use the expression `counter.to_bytes(24,
"little")`. Your output should be the list of these ciphertexts, each encoded
as a hex string.

If you're using Python/PyNaCl, note that the `nacl.secret.SecretBox.encrypt`
method prepends the nonce bytes to the ciphertext by default. We'll see why it
does that shortly, but for now that's not what we want. You can get the
unaltered ciphertext bytes from the `ciphertext` field of the returned object.
So where you would write:

```python
SecretBox(key).encrypt(message, nonce)
```

...expand that to:

```python
SecretBox(key).encrypt(message, nonce).ciphertext
```

Take a few moments to play with `encrypt` in the interpreter, to make sure the
difference between those two things is clear. If you're using a language
besides Python, your libsodium bindings might or might not do something
similar. You'll need to play with them and see.

**Input:** a list of ASCII strings to be encrypted

**Output:** a list of hex-encoded ciphertexts, made with the nonce schedule described above

## Problem 5: secretbox decryption with a sequential nonce

This is the inverse of Problem 4. Given a list of messages of the same form as
your previous output, encrypted with a key of thirty-two `B` (0x42) bytes and a
sequential nonce starting from 0, decrypt the messages.

Note that the key in this problem is _not the same_ as the key in Problem 4. If
it was, we'd be breaking the nonce rule! You should never, ever break that
rule, and I'm never going to break it in this class...except in the very next
problem...

**Input:** a list of hex-encoded ciphertexts to be decrypted, made with the same nonce schedule as in Problem 4

**Output:** a list of decrypted plaintexts, all ASCII strings

## Problem 6: What happens when you reuse a nonce?

Reusing a nonce with the same key is always bad, but exactly how bad it is
depends on what cipher you're using. For the XSalsa20 stream cipher that
secretbox is based on, it turns out it's just as bad as it was with the
one-time pad. Which is to say, really *really* bad!

Your input for this problem is a pair of hex-encoded secretbox messages, which
have been encrypted with the same key and nonce. (Oops!) Similar to Problem 3,
you don't know anything about the key or the nonce, but you do know that the
first plaintext consists entirely of `$` (0x24) characters. It turns out you
can decrypt the second plaintext using the same procedure as in Problem 3.
Close your eyes and pretend that these two ciphertexts were encrypted with the
same one-time pad, and then repeat the xor attack. The only difference this
time is that the first 16 bytes of each secretbox ciphertext are random-looking
junk that you should strip off and ignore for now. (Specifically, they're
Poly1305 authenticator tags. We'll talk more about these when we get to
Chapters 7 and 8 of *Serious Cryptography*.)

**Input:** a list of two hex-encoded secretbox ciphertexts of the same length

**Output:** the second decrypted plaintext, an ASCII string

Is it surprising that this works? Secretbox isn't a one-time pad, but it turns
out that they have a lot in common. We'll talk all about this when we get to
stream ciphers in Chapter 5 of *Serious Cryptography*.

**CAUTION:** The one-time pad reuse mistake we saw in Problem 3 isn't very
common in practice, because we don't often use one-time pads directly. But
nonce reuse mistakes like this one are quite common. Secretbox is a widely-used
standard -- recommended in [Cryptographic Right
Answers](https://latacora.micro.blog/2018/04/03/cryptographic-right-answers.html)!
-- and many other common standards behave similarly. Nonce reuse is a frequent
source of vulnerabilities in real-world applications, [even ones written by
experts](https://www.daemonology.net/blog/2011-01-18-tarsnap-critical-security-bug.html).
If bad randomness is the first thing you should look for when you're reviewing
crypto code, then nonce reuse is the second.

## Problem 7: secretbox encryption with a random nonce

Counter nonces are straightforward, and for keys that are generated randomly
and never saved anywhere ("ephemeral" or "session" keys), it's no big deal to
keep a counter. But for keys that get reused over time, or keys that are
derived from some other long-term secret like a password, or keys that are
shared across many machines, managing a counter might not be practical or safe.
Even something as simple as saving a counter to disk might fail, if the disk
happens to be full, or if today just isn't your day.

Luckily there's another generic approach that works better in these cases:
random nonces. When you use random nonces that are at least 24 bytes long, it's
vanishingly unlikely that you'll ever pick the same nonce twice. That means you
don't have to worry about nonce reuse, even between uncoordinated senders
sharing a key. However, because the recipient can't know what nonce you
generated, you do need to send the nonce along with the ciphertext. It doesn't
need to be secret, so typically you'll just prepend it. (This is why
`nacl.secret.SecretBox.encrypt` prepends your nonce to your ciphertext by
default. It assumes you're taking this approach.)

Let's try it out. Your input for this problem is a list of ASCII strings to be
encrypted. Encrypt each of them with secretbox using a key consisting of
thirty-two `C` (0x43) bytes, and a (distinct!) random nonce. Prepend each nonce
to the ciphertext that was encrypted with it, or allow PyNaCl to do that for
you by writing `.encrypt(...)` instead of `.encrypt(...).ciphertext`. Your
output should be the list of hex-encoded ciphertexts.

Remember that in Python, byte strings (like regular strings) can be
"concatenated" using the `+` operator.

Because this problem involves generating your own randomness, the grading
program won't expect your outputs to be equal to anything in particular.
Instead, it'll check that it when it decrypts your ciphertext using the nonce
you've prepended, the original input comes back out.

**Input:** a list of ASCII strings to be encrypted

**Output:** a list of hex-encoded ciphertexts, with their random nonces prepended prior to hex-encoding

## Problem 8: secretbox decryption with a random nonce

This is the inverse of Problem 7. Your input is a list of hex-encoded
ciphertexts, with 24-byte random nonces prepended, of the same form as your
output above. Hex-decode each ciphertext, extract the 24-byte nonce from the
front (or allow PyNaCl to do it for you by omitting the nonce argument), and
decrypt with the same key consisting of thirty-two `C` (0x43) bytes. Your
output should be the list of decrypted plaintexts, all ASCII strings.

Remember that in Python, you can get the first 24 bytes of `some_bytes` by
writing `some_bytes[0:24]` or just `some_bytes[:24]`, and you can get all the
rest by writing `some_bytes[24:len(some_bytes)]` or just `some_bytes[24:]`.

**Input:** a list of hex-encoded ciphertexts, with their random nonces prepended prior to hex-encoding

**Output:** a list of decrypted plaintexts, all ASCII strings

"Secretbox plus a random nonce" is a robust way to encrypt many messages with
the same key. This is a very important tool to have in your cryptographic
toolbox. **CAUTION** however: Many encryption algorithms, including other
widespread standards like AES-GCM and ChaCha20-Poly1305, have nonces that are
shorter than 24 bytes. Using random nonces with these algorithms is
problematic, because it [puts a limit on the number of messages you can encrypt
with the same key](https://en.wikipedia.org/wiki/Birthday_attack). When you're
considering a new cipher that has a nonce parameter, pay careful attention to
the size of the nonce.
