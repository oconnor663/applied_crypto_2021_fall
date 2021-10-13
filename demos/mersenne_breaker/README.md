The output of Python's `random.randbytes` function is predictable. Here's a
demo of that.

1. Save the output of `mersenne.py`.
2. Delete the last 10 elements of that output.
3. Feed that truncated output to `mersenne_breaker` (`cargo run`).
4. The output of `mersenne_breaker` is the same as the 10 elements you deleted.

Tested on Python 3.9.
