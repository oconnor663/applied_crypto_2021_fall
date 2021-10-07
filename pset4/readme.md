# Coding Problem Set 4: Hash Functions

This problem set goes with *Serious Cryptography* Chapter 6. I recommending
reading through at least the definition of "collision resistance" on p. 109
before you start.

Example input:

```json
{
  "problem1": "unicorn cat hippopotamus",
  "problem2": null,
  "problem3": [
    "0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef",
    "0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef"
  ],
  "problem4": null,
  "problem5": 1466615157
}
```

Example output:

```json
{
  "problem1": {
    "md5": "cb6b0fd8aa7fbc4e5b189b17e01bdc7c",
    "sha1": "b5d871a54726a1be8fa594d011bd3610f283cb21",
    "sha256": "dd501852933e8f856c33fed4385c2b4ad0b64c513d0af8d3d3e315764986d73c",
    "sha3_256": "ca865b257e1ec4d9bab831ec6a1019def9d0d6092f4db95686db313f50d4325c"
  },
  "problem2": {
    "md5": "49a61fed1b219aaf1d7a0633379dd2a4",
    "sha1": "2e89691e494ad9d76265bae8d40eb4e089c1fef8",
    "sha256": "3b6369797c748f684439e9bb72f1ed44a2de3712a4adfd2da85aec7bac83b4ec",
    "sha3_256": "31b4b4645f2a9bdf0559fd75f0242e953cc2d4fa911f2208bee004b01eb69707"
  },
  "problem3": "cee9a457e790cf20d4bdaa6d69f01e41",
  "problem4": "38762cf7f55934b34d179ae6a4c80cadccbb7f0a",
  "problem5": {
    "lucky_hash": "000000738eaf4fdf4b40ea481ca808ff1330fea0f1c3fa0ddbaaae81eeaef91c",
    "tries": 2000000
  }
}
```

## Problem 1: Common standards, old and new

Unlike ciphers, where almost everything these days is based on just a couple of
primitives (AES and Salsa/ChaCha), hash functions show a bit more variety. Here
are some common standards that you're likely to see:

- [MD5](https://en.wikipedia.org/wiki/MD5), published in 1992, **☣️ broken ☣️**
  in 2004.
- [SHA-1](https://en.wikipedia.org/wiki/SHA-1), published in 1995, **☣️ broken
  ☣️** in 2017.
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2), published in 2001, still
  secure. The SHA-2 standard includes multiple functions, most importantly
  SHA-256 and SHA-512.
- [SHA-3](https://en.wikipedia.org/wiki/SHA-3), published in 2015, still
  secure. SHA-3 also supports different output lengths, and each variant has a
  name like SHA3-256.

All of these hash functions are available in the
[`hashlib`](https://docs.python.org/3/library/hashlib.html) module of the
Python standard library. For example, to hash the ASCII string `hello world`
using SHA-256, you can write something like this:

```python
import hashlib
hex_encoded_hash = hashlib.sha256(b"hello world").hexdigest()
print(hex_encoded_hash)
```

Let's get ourselves acquainted with these functions. Your input for this
problem is an ASCII string. Convert it to bytes and hash it four different
ways. Your output should be an object with four fields, `"md5"`, `"sha1"`,
`"sha256"`, and `"sha3_256"` (note the underscore), each containing the
corresponding hex-encoded hash of the input. These field names are the same as
the names of each of these functions in the `hashlib` module.

**Input:** an ASCII string to be hashed

**Output:** an object with 4 fields, `"md5"`, `"sha1"`, `"sha256"`, and `"sha3_256"`, each containing the corresponding hex-encoded hash of the input

## Problem 2: The "avalanche effect"

One of the important security properties of a cryptographic hash function is
that the output shouldn't reveal anything about the input. This is closely
related to "preimage resistance", and it means that even a tiny change in the
input needs to result in a totally different hash. We call this the ["avalanche
effect"](https://en.wikipedia.org/wiki/Avalanche_effect). Let's see it in
action.

Take the same input string you used in Problem 1 above, but change the first
character to be a `?`. You can do this with string slicing if you like, but to
get more practice working with bytes, I suggest doing it by assigning to a
`bytearray`, like this:

```python
original = b"hello world"
modified = bytearray(original)
modified[0] = ord("?")
assert modified == b"?ello world"
```

> Aside: If you haven't used the `ord` function in Python before, take a look
> at [the docs for `ord`](https://docs.python.org/3/library/functions.html#ord)
> and [the docs for
> `chr`](https://docs.python.org/3/library/functions.html#chr) and play with
> them for a few minutes. They're a really important part of the story of how
> bytes and strings relate to each other.

Your output for this problem should be another four-field object of the same
form as in Problem 1 above, with each hash using the modified bytestring as
input. Notice that even though we only made a one-character change to the
input, the outputs look totally different. This is the avalanche effect.

**Input:** none (modify the input from Problem 1 above)

**Output:** an object of the same form as in Problem 1 above

## Problem 3: A collision in MD5

MD5 ("Message Digest 5"), published in 1992, was designed to be a secure
cryptographic hash function. But today it's broken, because it has known
collisions. The first was [found in 2004 by Xiaoyun
Wang](https://web.archive.org/web/20160320040624/http://www.emc.com/emc-plus/rsa-labs/historical/collisions-but-sha1-secure.htm),
and many others have been found since, including the unusually short pair of
inputs shown here, which was [discovered in
2010](https://eprint.iacr.org/2010/643.pdf). These two colliding inputs are
almost identical, except for just two bits, which I've marked with lines:

```
0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef
                                           |                                          |
0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef
```

Having just talked about the avalance effect, we might expect these two changed
bits to result in a totally different hash. But these aren't just any old bits.
These two bits (in fact, all the bits of both inputs) have been carefully
selected to exploit weaknesses in the inner workings of MD5.

Your input for this problem is these two strings. You can either read them from
the input JSON, or just paste them from here into your code. Hex-decode them,
and compute the MD5 hashes of their decoded bytes. Take a look! It's the same
for both! MD5 is broken! Back in the day, this was big news.

**Input:** a list containing the two hex-encoded strings shown above

**Output:** the hex-encoded MD5 hash of those byte strings (they collide, so it doesn't matter which one)

Note that there's no random input for this problem. You can just hardcode the
answer if you like.

## Problem 4: A collision in SHA-1

SHA-1 ("Secure Hash Algorithm 1") was published in 1995. Like MD5, it's known
to be broken today, but it lasted quite a bit longer. The first collision was
[found by researchers at CWI and Google in 2017](https://shattered.io/). They
constructed two colliding PDF files, which are included in this problem set
directory ([`shattered-1.pdf`](./shattered-1.pdf) and
[`shattered-2.pdf`](./shattered-2.pdf)). Open them and take a look. They're
clearly different: one is red and the other is blue. But when you hash them
with SHA-1, they collide! Try it yourself and see.

These inputs are substantially larger that the ones above, over 400 KiB, so
I've left them out of the input JSON. To get their bytes, you'll need to read
them from the filesystem. You can read bytes from a file in Python like this:

```python
# This file path assumes you're running Python in the same directory as the PDF. Adjust as needed.
file_path = "./shattered-1.pdf"
# "rb" means "binary read mode", i.e. reading bytes instead of strings
file_bytes = open(file_path, "rb").read()
```

**Note that the filepath of these files in the grading environment probably
won't be the same. So once you've found the answer, just hardcode it and
comment out your file reading code.**

**Input:** none (read the PDF files provided)

**Output:** the hex-encoded SHA-1 hash of `shattered-1.pdf` and also `shattered-2.pdf` (again, they collide, so it doesn't matter which one)

As with Problem 3 above, there's no random input for this problem.

## Problem 4b: A collision in SHA-2

Just kidding. There aren't any known collisions in SHA-2 or SHA-3. That's the
main reason they're still considered secure. But if you do happen to find one,
let me know...

## Problem 5: How long does it take to brute force a specific hash?

For a secure cryptographic hash function, finding an input that gives exactly
the hash you want is prohibitively difficult. Hash outputs are pseudorandom,
and it's a security requirement that there shouldn't be any way to control
those outputs, other than by trying over and over again with different inputs
until you get lucky. For a hash like SHA-256, that's far too many bits to ever
get lucky enough to control the whole thing, or even half of it.

Let's get a sense for how hard this is by doing something similar but much
smaller. Let's try to control just the first three bytes of the hash — or
equivalently, the first six hexadecimal digits — and force them all to be zero.
For an unbroken cryptographic hash function, the only way to do this is to hash
a ton of different inputs, each time hoping to just get lucky and see these
zeros. We call this approach "brute force", because it doesn't rely on any
understanding or analysis of the hash function itself. We just throw CPU cycles
at it until the answer we want comes out.

How many hashes will we need to compute before we get lucky and find the zeros
that we're looking for? A bytestring of length 3 has 256<sup>3</sup> =
(2<sup>8</sup>)<sup>3</sup> = 2<sup>24</sup> possible values. Equivalently, a
six-character hex string also has 16<sup>6</sup> = (2<sup>4</sup>)<sup>6</sup>
= 2<sup>24</sup> possible values. Either way, we're looking at a probability of
1 in 2<sup>24</sup>, that is, 1 in 16,777,216. So we'll need to compute
something in the ballpark of 16 million hashes before we can expect to randomly
find one that starts with the zeros we're looking for. There's certainly no way
we could do that much work by hand, but let's make the computer do it.

The easiest way to generate millions of different inputs is to use a counter,
similar to the counter nonces we saw back in Problem Set 2. Start by writing an
infinite loop that increments a counter variable. Each time through the loop,
encode the counter to bytes and hash those bytes. For this problem, use **8
little-endian bytes** to encode your counter (remember that's `.to_bytes(8,
"little")`) and **hash those bytes with SHA-256**. If the result starts with
the zeros you're looking for, `break` out of your loop. If you're using the
hexadecimal representation of hashes returned by `.hexdigest()`, then the
simplest way to check for this condition is `my_hash.startswith("000000")`.

Your input for this problem is a number. Use this number as the starting value
of your counter. Your output should be an object with two fields: The
`"lucky_hash"` field should contain the hash you found, encoded as hex. And the
`"tries"` field should contain the total number of hashes had to try to find
it. (That is, your final counter value, minus your starting counter value, plus
one.)

**Input:** an initial value for your counter

**Output:** an object with two fields, `"lucky_hash"` and `"tries"`

Once you've got this working, make sure to try it with a few different starting
numbers. One way to do that is to pipe the output of the provided
`generate_input.py` script into your `solution.py`:

```
python3 generate_input.py | python3 solution.py
```

On my laptop, this search takes about a second to run with the example input
(which I've deliberately chosen to not take too long), but some other random
inputs take almost half a minute. It's not very often that we get to write code
that really strains our CPU like this.

If this is how long it takes to find 3 zero bytes / 24 zero bits, how long do
you think it would take to find a hash where _all 256 bits_ were zero?
