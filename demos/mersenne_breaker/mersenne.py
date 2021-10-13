#! /usr/bin/env python3

import random

for _ in range(1000):
    # Note that random.randrange(2**32) is not equivalent. It skips bytes in
    # the RNG output stream.
    print(int.from_bytes(random.randbytes(4), "little"))
