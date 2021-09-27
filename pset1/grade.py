#! /usr/bin/env python3

import json
import sys


def eprint(s, end="\n"):
    print(s, file=sys.stderr, end=end)


if len(sys.argv) != 4:
    eprint("Usage: grade.py <inputs> <expected> <submitted>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    inputs_obj = json.load(f)

with open(sys.argv[2]) as f:
    expected_obj = json.load(f)

with open(sys.argv[3]) as f:
    submitted_obj = json.load(f)

assert type(inputs_obj) == dict, "expected_obj is not a list"
assert type(expected_obj) == dict, "expected_obj is not a list"
assert type(submitted_obj) == dict, "submitted_obj is not a list"

problem_objects = []
for problem in expected_obj:
    problem_object = {"name": problem, "max_score": 1, "score": 0}
    eprint(f"{problem}: ", end="")
    if problem not in submitted_obj:
        eprint("missing")
    elif expected_obj[problem] != submitted_obj[problem]:
        eprint("incorrect")
        eprint(f"  expected:  {repr(expected_obj[problem])}")
        eprint(f"  submitted: {repr(submitted_obj[problem])}")
    else:
        problem_object["score"] = 1
        eprint("ok")
    problem_objects.append(problem_object)

output = {
    "stdout_visibility": "visible",
    "tests": problem_objects,
}
json.dump(output, sys.stdout, indent="  ")
print()
