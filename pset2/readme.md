# Coding Problem Set 2: Randomness

Example input:

```json
{
  "problem1": "zebra hippopotamus yak",
  "problem2": {
    "pad": "861064c995db4ef2331197b006c93870d176c95a0ec7edff73",
    "ciphertext": "f06508bde0a92bd25478e5d160af5d50b303bd2e6bb58b930a"
  },
  "problem3": [
    "ddadb3d736b5578e444effa4c42c5dcefb8608d2821899c0c4",
    "97e8e5847af01f8a1202b2ee8f6b1c98b0d10c81c951df8594"
  ],
  "problem4": [
    "jaguar rhinoceros butterfly",
    "manatee llama quail",
    "narwhal dog elephant"
  ],
  "problem5": [
    "c8614be36608f575def5be10837bdf41f02f8f9a3b8ccb45ff4a1e1d9959412e98",
    "fc070700995010a48727e29c32901941ef06ac7a898b75c877805a0225a498cf71856908e26f37",
    "a6f05c747a06042ee83c684bfec2994da424a152f697ed934c0d3f55aacd5dc365f3dc"
  ],
  "problem6": [
    "19cb5853deeee788223eadf0ae15b1b0890170f2c3a92ad5722d3d5bdab186b1d4632f",
    "43e6335320e8f607ecfea0d78db71ebbc0443ab793e86bd125617c1a8eb5d3e0912e67"
  ],
  "problem7": [
    "kangaroo kangaroo sheep",
    "jaguar aardvark aardvark",
    "hippopotamus llama elephant"
  ],
  "problem8": [
    "1155384ba10ebc98ed5f90c7edc5838892a3400d48c39d9e4ec1b9a21c9595d78d1a01fb141bb3c306e096ece342133e0333fd224131241de2",
    "29282748ad89052cac79285eed183549842fb6004357a7fd627a2dc4631a03e19524b4e23f5ba64697919fbf087b76e226bbabf78605cdf8924f2b0ccdc6",
    "6b90216949ba64f519ccc3bfef7a6db40ad5c95d1f4e565713727f5a329c456652218dbc6734cde6656cc521eba28b82c7bf0ee61d432f05edd3"
  ]
}
```

Example output:

```json
{
  "problem1": {
    "pad": "52bc13142c98384d45ad95c3829f870158e983d01f66",
    "ciphertext": "28d971664db8502435ddfab3edebe66c2d9aa3a97e0d"
  },
  "problem2": "vulture giraffe butterfly",
  "problem3": "narwhal rhinoceros wombat",
  "problem4": [
    "84fae54aa7abce4daeecd908411da478f52d9c802a8b9817f4420452895456249b552b8c5d463e1f52a3ed",
    "2dbbeb3ad7a2994232c6a868d1b31791f412ae6f889c75c87c85490e22e28c9a778577",
    "d3bd36aac6abaea92d2c07aedff9baf8a724bd44ea93e493580b3f55a2c056d279f7d785"
  ],
  "problem5": [
    "octopus cat sheep",
    "vulture giraffe giraffe",
    "manatee pig manatee"
  ],
  "problem6": "manatee sheep quail",
  "problem7": [
    "a9eafdff4c685a6c7260cbc15e7a7accd7ddfe76211876b881fcee8574b0a7de2b53d7897867587f505d0470f34a52e2385c2a740811aaef420191b3332d81",
    "4f6e8d1baa502105f6674ebef3a05e05406c18eb8cb8f321b11c9cf244ac16e271a808b1e2715d43b4edc8de7adc18045bb0c8fa712fb9890a832957d4447279",
    "b12b3e31f4abc64c9ec6a70f1f844c56833c30edb8fdb7e478ad295da624b3b408de29c4fa647dbd4f187123b55c4ef4e469c26afe21e05cbdce3e5fed720d5b6ccd2f"
  ],
  "problem8": [
    "quail giraffe yak",
    "llama pig xenoceratops",
    "kangaroo dog llama"
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
Decode those strings and decrypt the ciphertext by xor'ing it with the pad.
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
**little-endian** order, that is `[0, 0, ..., 0]`, `[1, 0, ..., 0]`, and so on.
In Python, if you have an integer variable called `counter`, you can use the
expression `counter.to_bytes(24, "little")`. Your output should be the list of
these ciphertexts, each encoded as a hex string.

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
it were, we'd be breaking the nonce rule! You should never, ever break that
rule, and I'm never going to break it in this class...except in the very next
problem...

**Input:** a list of hex-encoded ciphertexts to be decrypted, made with the nonce schedule described above

**Output:** a list of decrypted plaintexts, all ASCII strings

## Problem 6: What happens when you reuse a nonce?

Reusing a nonce with the same key is always bad, but exactly how bad it is
depends on what cipher you're using. For the XSalsa20 cipher that secretbox is
based on, it turns out it's just as bad as it was with the one-time pad. Which
is to say, really *really* bad!

Your input for this problem is a pair of hex-encoded secretbox messages, which
have been encrypted with the same key and nonce. (Oops!) Similar to Problem 3,
you don't know anything about the key or the nonce, but you do know that the
first plaintext consists entirely of `$` (0x24) characters. It turns out you
can decrypt the second plaintext using the same procedure as in Problem 3. The
only difference is that the first 16 bytes of each secretbox ciphertext are
random-looking junk that you should strip off and ignore for now.
(Specifically, they're Poly1305 authenticator tags. We'll talk more about these
when we get to Chapters 7 and 8 of *Serious Cryptography*.)

**Input:** a list of two hex-encoded secretbox ciphertexts of the same length

**Output:** the second decrypted plaintext, an ASCII string

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
you. Your output should be the list of hex-encoded ciphertexts.

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
