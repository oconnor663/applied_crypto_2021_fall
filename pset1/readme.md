# How coding problem sets work

All the coding problem sets in this course will work like this:

- Your solution will be a standalone program that reads from standard input and
  writes to standard output. **You'll submit your solution to Gradescope**, and
  it'll be graded automatically. There's no limit to the number of times you
  can submit.
- The name of your program is important. The grading program will look for
  `solution.py`, `solution.sh`, or a short list of other known project files.
  For the exact details, look at what the
  [`run_solution.py`](../docker/run_solution.py) script does.
- In the grading environment, **your program's stdin will be a JSON object**
  containing all the inputs for all the problems in the problem set. The input
  for Problem 1 will be the `"problem1"` field of that object, the input for
  Problem 2 will be the `"problem2"` field, and so on.
- **Your program's stdout should be a JSON object of the same form,**
  containing all the outputs for all the problems in the problem set. Your
  answer for Problem 1 should be the `"problem1"` field of that object, your
  answer for Problem 2 should be the `"problem2"` field, and so on.
- Your program's standard error will be ignored. It's fine to leave debug
  printouts in place, as long as they write to stderr and not stdout, but note
  that writing anything other than one JSON object to stdout will break the
  grading program.
- The grading program will parse your JSON output and then check your answers
  for (in most cases) exact equality with the expected answer. Because this is
  done after parsing, differences in JSON whitespace formatting don't matter,
  and you don't need to worry about indentation or trailing newlines. Each
  correct problem is worth a point. There is no partial credit for close
  answers or nearly correct code. Output that isn't valid JSON won't get any
  points.
- Gradescope is the source of truth for due dates. We'll usually publish
  solutions for each problem set immediately after the submission deadline
  expires. Partly for that reason, **Gradescope will not accept any late
  submissions.** If we need to make accommodations for illness or other life
  circumstances, we can reach out to the Office of Student Affairs together.

To help everyone get up to speed on the first problem set, complete example
solutions in several languages are provided [in this folder](./). As noted
below, our copying policy is relaxed for this first problem set, and it's ok to
copy code from these examples. I've also made a screen recording of myself
writing a solution and submitting it. I recommend everyone watch this
recording:

<a href="http://www.youtube.com/watch?v=b0gGlcHvfY0">
  <img src="http://img.youtube.com/vi/b0gGlcHvfY0/maxresdefault.jpg" alt="walkthrough video" width="400">
</a>

## Programming languages

Your solutions can be written in any language you like, as long as you can call
libsodium functions (see Problem 4 below) and run your code in the grading
environment, an Ubuntu-20.04-based Docker container. The grading environment
has pre-installed support for Python 3, Go, Rust, Java, and C/C++, and if you
like you can install extra dependencies yourself by including a `setup.sh`
script in your solution. Lectures and example code will focus on Python, so
**doing your problem sets in Python will be the lowest-friction choice with the
most help available**. Please make sure you use Python 3 and not Python 2.
Adventurous students looking for something new are encouraged to try Go or
Rust. Java is mildly discouraged, because it will be higher-friction than
Python, and because there will be less help available. If you're leaning
towards Java because you haven't used Python in a while, please seriously
consider brushing up on Python. But if you love Java, and you're already
familiar with command line build tools like Gradle, then have at it. Problem
sets will be independent of each other, so doing different problem sets in
different languages is fine.

## Cheating policy

**All the code you submit must be written by you.** Submitting code written by
anyone else is cheating in the official sense. Please don't do that.

It's ok (and encouraged!) for students to work together by discussing problems
without sharing code. It's also ok to have someone look at your code to help
you debug a specific issue. But it's not ok to look at someone else's code to
copy it or to have anyone write code for you. Please don't explore the gray
area between these things.

For common operations like "open a file", "parse a JSON string", or "call a
library function", it's ok to copy two or three lines of code from
documentation, Stack Overflow, etc. But copying more than two or three lines of
code is probably not ok. If you do, you must clearly cite your source in an
inline comment that begins with `COPIED`. Citing your source doesn't
automatically make copying ok, but failing to cite your source turns one
violation into two violations. Please don't explore the gray area of what
counts as a "line of code".

The sole exception to this policy is here in Problem Set 1, where we've
provided the screen recording above and example solutions in several languages,
to help everyone get their tools set up and get used to the problem set
structure. For this problem set, and only this problem set, it's ok if you copy
our code.

# Coding Problem Set 1

Example input:

```json
{
  "problem1": [1, 9, 7, 5, 8],
  "problem2": "616172647661726b206f63746f70757320686970706f706f74616d75732070696720696775616e61",
  "problem3": "unicorn sheep rhinoceros yak manatee",
  "problem4": "badb9827d58a815975420a9213da7cfb9069d71e427ddcb2cf223fe58418e56c5dc1c50205adbf8b12b70bf082d98b",
  "problem5": [
    "4e3c2989dde712b0112322f439602d8eb04b8c25a2e8f2302411be39e64cac278a2320213d8b773e69a1d9cee556315234b4",
    "457ae67254cd53a370492c46c7d2e23ff57040b158f901e3a154cbfd3246223efd2ecf12fc1fc2fd8f2525d3674fe7106e1f",
    "9bcadaa18f14307ddef060096b846d6ef807ae445c0b8e719b01e119cf443f4894fe1af631592391cdc1d5e1e0b5e502fc00",
    "76752ae61b3f22e0b05c564b647bb16d2028f6059fcb618b377105719017141ebd3d262d5762cd07377842c7c4b4afd8b838",
    "2102d51548ffdc82dd5c5269f15ecbf75a62cf6c5e36dce6cac5736434980e2e504e3a2fdfc479e843736506b55cc52375eb",
    "6647af5d9152b83c4953e5d15bf49647370f7e181848ee298c288117a14cd3c50000d14a7fa44ff66bb296b34ebe996740e4",
    "d5eb8fcda6d0a5a7e4d422f94f32feec74ddcac4b00090df4a21179beec1670033f324778e1264fe6c2b4c065b6deb6eff79",
    "871145d8c2f0fb218ae11bd4c943ec6e060557ae4d85118a0f39b07d9916a182ce1a1ec80d4ce5853577d6cf40784a8ec24e",
    "dd8cda730487aa0903741bcf3e81520e9a07618943d357c77cf246f1f9d64be4a529d0faabd347543a8639218bfd86e614b6",
    "7611ff79f203c3ae335a94b325bc2d5f9a3267c61a21c4bd3a9e118022e31bfd2cd379184bb677bd09cea933e9d348bd393c"
  ]
}
```

Example output:

```json
{
  "problem1": {
    "sum": 30,
    "product": 2520
  },
  "problem2": "aardvark octopus hippopotamus pig iguana",
  "problem3": "756e69636f726e207368656570207268696e6f6365726f732079616b206d616e61746565",
  "problem4": "quail cat giraffe turkey wombat",
  "problem5": "unicorn jaguar butterfly dog llama"
}
```

If you're not sure how to work with these inputs and outputs, and you haven't
yet watched the walkthrough video above, **please watch the video**.

## Problem 1

Let's start with a small arithmetic problem, to get used to reading JSON input
and producing JSON output. The input (the `"problem1"` field in the input JSON
object) is a list of integers, and the output (the `"problem1"` field in your
output JSON object) is an object with two fields: "sum" containing the sum of
the integers, and "product" containing the product of the integers.

**Input:** a list of integers, e.g. `[2, 3, 4]`

**Output:** an object with two fields, "sum" and "product", e.g. `{ "sum": 9,
"product": 24 }`

## Problem 2

Now that we've got JSON working, let's get hex encoding and decoding working.

**Input:** a hexadecimal string, which encodes some ASCII bytes, e.g. `"68656c6c6f20776f726c64"`

**Output:** the decoded ASCII string, e.g. `"hello world"`

## Problem 3

This is the inverse of Problem 2 above, to make sure we can go both directions.

**Input:** an ASCII string, e.g. `"hello world"`

**Output:** a hexadecimal string, which encodes the ASCII bytes of the input
string, e.g. `"68656c6c6f20776f726c64"`

## Problem 4

Finally, let's play with some crypto! Before you can do these last two
problems, you'll need to get set up with libsodium. The recommended way to do
that in Python is to install the
[PyNaCl](https://pynacl.readthedocs.io/en/latest/) library. You can take a look
at their [installation
instructions](https://pynacl.readthedocs.io/en/latest/install/#), but in short
you're going to run:

```
pip install pynacl
```

Pip is the standard Python tool for downloading and installing new
modules/libraries. In many cases that command will Just Work. Unfortunately, it
might work a little differently depending on what operating system you're using
(Windows/macOS/Linux) and how you installed Python (from the official website,
or with Chocolatey/Homebrew/apt-get/etc). In some cases, particularly on macOS
and Ubuntu, `python` and `pip` may be called `python3` and `pip3`. If `pip
install pynacl` doesn't seem to work, or if it prints scary deprecation
warnings about Python 2, you might need to try `pip3 install pynacl`. You'll
know you've got it when you can run the Python 3 interpreter and `import nacl`
without any errors, like this:

```
$ python
Python 3.9.6 (default, Jun 30 2021, 10:22:16)
[GCC 11.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import nacl
>>>
```

I apologize in advance for the suffering that some students will go through to
get Python and Pip working. I hope it's some consolation that, once you've
figured it out, you'll have opened up [an entire universe of Python
packages](https://pypi.org/) that you can use for [all
sorts](https://seaborn.pydata.org/examples/index.html) of [fun
stuff](https://towardsdatascience.com/animations-with-matplotlib-d96375c5442c).
For students working with Go, Rust, or Java, take a look at how the example
solutions for this problem set are set up. For students working in other
languages, good luck and Godspeed.

Anyway, back to Problem 4: Your input will be an encrypted message in the
NaCl/Sodium secretbox format. Your output should be the decrypted plaintext, an
ASCII string. You need to decrypt it using
[`nacl.secret.SecretBox.decrypt`](https://pynacl.readthedocs.io/en/latest/secret/#nacl.secret.SecretBox.decrypt)
(in Python) or any other equivalent of the libsodium
[`crypto_secretbox_open_easy`](https://doc.libsodium.org/secret-key_cryptography/secretbox)
function. Using `SecretBox.decrypt` looks something like this:

```python
from nacl.secret import SecretBox

plaintext = SecretBox(key).decrypt(ciphertext, nonce)
```

The key for this message is thirty-two `A` (0x41) bytes, and the nonce is
twenty-four `B` (0x42) bytes. What exactly is a "nonce"? We'll talk more about
that in the next class and in the next problem set, but if you'd like to read
ahead, take a look at [the `SecretBox`
docs](https://pynacl.readthedocs.io/en/latest/secret/#nonce). (It's always a
good idea to read the docs of any library you rely on, especially for
security.)

**Input:** an encrypted ciphertext, encoded as a hexadecimal string

**Output:** the decrypted plaintext, an ASCII string

## Problem 5

Ok, now we know how to open a secretbox. You can try encrypting your own
messages if you like, but for the final problem in this set, we're going to
stick with decryption and look and an important fact that you might already
have noticed: Decryption can fail.

It turns out that secretbox is doing more than meets the eye. We'll wait to
dive into the nitty gritty details until we get to "authenticated encryption"
(chapter 8 in Serious Cryptography). But in the meantime, just notice that if
you try to decrypt some random garbage bytes, you don't get a random garbage
answer. Instead, you get an error. Take a few minutes to play with this. You
can try decrypting the ciphertext from Problem 4 above using the wrong key or
the wrong nonce too.

Your input for this problem is a list of candidate ciphertexts, each encoded as
a hexadecimal string. Only one of these ciphertexts is valid. The others are
random garbage bytes that will fail to decrypt. Using a key of thirty-two `C`
(0x43) bytes and a nonce of twenty-four `D` (0x44) bytes, find the valid
ciphertext and output the plaintext that it decrypts to.

This problem requires error handling, because you don't want decryption
failures to crash your whole program. In Python, that means catching
`nacl.exceptions.CryptoError` exceptions with `try`/`except`. Other languages
will need to do something similar.

**Input:** a list of candidate ciphertexts, each encoded as a hexadecimal string

**Output:** the decrypted plaintext of the single valid ciphertext, an ASCII string
