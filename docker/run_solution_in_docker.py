#! /usr/bin/env python3

import os
from os import path
import subprocess
import sys


def eprint(s):
    print(s, file=sys.stderr)
    sys.exit(1)


HERE = path.dirname(path.realpath(__file__))

if len(sys.argv) != 3:
    eprint("Usage: run_solution_in_docker.py <pset_dir> <solution_dir>")

pset_dir = sys.argv[1]
if not path.exists(pset_dir):
    eprint(f"{pset_dir} doesn't exist")
    sys.exit(1)

solution_dir = sys.argv[2]
if not path.exists(solution_dir):
    eprint(f"{solution_dir} doesn't exist")
    sys.exit(1)

# Build the Docker image quietly, if it hasn't been built before, redirecting
# any output to stderr.
build_script = path.join(HERE, "build_grading_image.py")
subprocess.run(
    [sys.executable, build_script, pset_dir, "--quiet"], stdout=sys.stderr, check=True
)

# Run the grader inside the grading image. This is similar to the instructions
# at https://gradescope-autograders.readthedocs.io/en/latest/manual_docker/.
# Mount the solution as read-only and then copy it to the submission directory,
# to avoid modifying the caller's solution dir in any way. (Docker setups like
# this one have an annoying tendency to write root-owned files to mounted
# directories.)
image_name = "applied_crypto_grading"
inner_script = """
set -e -u -o pipefail
cp -r /solution_ro /autograder/submission
/autograder/run_autograder
"""
output = subprocess.run(
    [
        "docker",
        "run",
        "--rm",
        "--interactive",
        "-v",
        f"{path.realpath(solution_dir)}:/solution_ro:ro",
        image_name,
        "bash",
        "-c",
        inner_script,
    ],
)
sys.exit(output.returncode)
