# How problem sets work

The problem sets in this course will work like this:

- Your solution will be a standalone program that reads from standard input and
  writes to standard output. You'll submit your solution to Gradescope, and it
  will be graded automatically.
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
- Each problem set will provide an [`example_input.json`](./example_input.json)
  and an [`example_output.json`](./example_output.json) file for your
  reference. The [`generate_input.py`](./generate_input.py) and
  [`grade.py`](./grade.py) scripts will also be available for each problem set,
  and you might find it useful to test your solutions against these scripts
  locally. The [`run_solution.py`](../docker/run_solution.py) script can help
  you make sure your solution is named and organized correctly. If you set up
  Docker, you can even use the
  [`build_grading_image.py`](../docker/build_grading_image.py) and
  [`run_solution_in_docker.py`](../docker/run_solution_in_docker.py) scripts to
  reproduce the exact grading environment and run your code in it. The only
  thing hidden from you will be the specific input created by
  `generated_input.py` that's used for grading on Gradescope.

Rather than writing out all these steps in exhaustive detail, I've made a
screen recording of myself working through the first problem set. As noted
below, our copying policy is relaxed for this first problem set, so that you
can take full advantage of the recording. Please watch it:

[![problem set 1 walkthrough video](http://img.youtube.com/vi/W0SVEHqy9h4/0.jpg)](http://www.youtube.com/watch?v=W0SVEHqy9h4 "Applied Crypto problem set 1 walkthrough")

Your solutions can be written in any language you like, as long as you can call
libsodium functions and run your code in the grading environment, an
Ubuntu-20.04-based Docker container. The grading environment has pre-installed
support for Python 3, Go, Rust, Java, and C/C++, and if you like you can
install extra dependencies yourself by including a `setup.sh` script in your
solution. Lectures and example code will focus on Python, so **doing your
problem sets in Python will be the lowest-friction choice with the most help
available**. Adventurous students are encouraged to try Go or Rust. Java is
mildly discouraged, because it will be higher-friction than Python, and because
there will be less help available. If you're leaning towards Java because you
haven't used Python in a while, please seriously consider brushing up on
Python. But if you love Java, and you're already familiar with command line
build tools like Gradle, then have at it. Problem sets will be independent of
each other, so doing different problem sets in different languages is fine.

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

The sole exception to this policy is here in Problem Set 1, where I'll provide
a screen recording and example solutions in several languages, to help everyone
get their tools set up and get used to the problem set structure. For this
problem set, and only this problem set, it's ok if you copy my code.

# Problem Set 1

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

Finally, let's play with some crypto! Your input will be an encrypted message
in the NaCl/Sodium secretbox format. You need to decrypt it, using
[`nacl.secret.SecretBox.decrypt`](https://pynacl.readthedocs.io/en/latest/secret/#nacl.secret.SecretBox.decrypt)
(in Python) or any other equivalent of the libsodium
[`crypto_secretbox_open_easy`](https://doc.libsodium.org/secret-key_cryptography/secretbox)
function. The key for this message is thirty-two `A` (0x41) bytes, and the
nonce is twenty-four `B` (0x42) bytes.

**Input:** an encrypted ciphertext, encoded as a hexadecimal string

**Output:** the decrypted plaintext, an ASCII string

## Problem 5

Ok, now we know how to open a secretbox. You can try encrypting your own
messages if you like, but for the final problem in this set, we're going to
stick with decryption and look and an important fact that you might've already
noticed: Decryption can fail.

It turns out that secretbox is doing more than meets the eye. We'll wait to
dive into the nitty gritty details until we get to "authenticated encryption"
(chapter 8 in Serious Cryptography). But in the meantime, just notice that if
you try to decrypt some random garbage bytes, you don't get a random garbage
answer. Instead, you get an error. Take a few minutes to play with this. Try
decrypting a legitimate ciphertext using the wrong key or the wrong nonce too.

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
