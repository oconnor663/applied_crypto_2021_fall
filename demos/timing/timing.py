#! /usr/bin/env python3

import hmac
import secrets
import sys
import time

# The slow_leaky_check() function will use this key, but the
# discover_mac_without_key() function will not look at it.
SECRET_KEY = secrets.token_bytes(32)


def slow_leaky_check(message, mac):
    expected_mac = hmac.digest(key=SECRET_KEY, msg=message, digest="sha256")
    assert len(expected_mac) == len(mac)
    for i in range(len(mac)):
        if expected_mac[i] != mac[i]:
            return False
        # Simulate a really slow equality check by sleeping for 0.1 milliseconds.
        time.sleep(1 / 10_000)
    return True


def discover_mac_without_key(message):
    # Note that this function does not look at SECRET_KEY!
    mac = bytearray([0] * 32)
    # Discover each index of the correct MAC, one by one.
    for i in range(len(mac)):
        # For the current index i, try all possible values of the byte.
        slowest_time = None
        slowest_value = None
        for value in range(256):
            # We want to find the *slowest* value for the current byte, because
            # that indicates that more digits are correct. But a check might
            # also be slow because of random CPU noise (other applications
            # doing stuff and taking up CPU time). To reduce this noise, check
            # each value several times, and use the *fastest* time we get for
            # each value.
            fastest_time = None
            for tries in range(5):
                mac[i] = value
                start_time = time.time()
                # We ignore the return value here. It's almost always going to
                # be false, and we only care about how long the check takes.
                slow_leaky_check(message, mac)
                duration = time.time() - start_time
                if fastest_time is None or duration < fastest_time:
                    fastest_time = duration
            # Now if the *fastest* time for this value was slower than the
            # *slowest* time we've seen so far at this index, save this value.
            if slowest_time is None or fastest_time > slowest_time:
                slowest_time = fastest_time
                slowest_value = value
        # Keep whichever value was the slowest at the current index, and move
        # on to the next index.
        mac[i] = slowest_value
        # Print these values to the terminal so that we can watch the progress.
        print(slowest_value, end=", ")
        sys.stdout.flush()
    print()
    # Confirm that the end result is correct.
    assert slow_leaky_check(message, mac)
    print("SUCCESS!")


def main():
    message = b"hello world"
    print("The correct MAC:")
    print(list(hmac.digest(key=SECRET_KEY, msg=message, digest="sha256")))
    print("The discovered MAC:")
    print("[", end="")
    discover_mac_without_key(message)


if __name__ == "__main__":
    main()
