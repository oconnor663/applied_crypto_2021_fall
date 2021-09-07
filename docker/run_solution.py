#! /usr/bin/env python3

import os
from os import path
import subprocess
import sys


def eprint(*args):
    print(*args, file=sys.stderr)


if len(sys.argv) != 2:
    eprint("Usage: run_solution.py <dir>")
    sys.exit(1)

solution_dir = sys.argv[1]
if not path.exists(solution_dir):
    eprint(f"{solution_dir} doesn't exist")
    sys.exit(1)


def solution_exists(filename):
    return path.exists(path.join(solution_dir, filename))


def run_solution(cmd):
    # Allow both stdout and stderr to inherit. Ignore the exit status of the
    # solution.
    subprocess.run(cmd, cwd=solution_dir)


# Look for solution files in this order:
#   - solution.sh
#   - solution.py
#   - Cargo.toml (Rust project)
#   - go.mod (Go project)
#   - settings.gradle (Java project)
# If more than one is found, only execute the first one found.
if solution_exists("solution.sh"):
    run_solution(["bash", "solution.sh"])
elif solution_exists("solution.py"):
    run_solution([sys.executable, "solution.py"])
elif solution_exists("Cargo.toml"):
    os.environ["RUST_BACKTRACE"] = "1"
    run_solution(["cargo", "run"])
elif solution_exists("go.mod"):
    run_solution(["go", "run", "."])
elif solution_exists("settings.gradle"):
    run_solution(["gradle", "run", "--quiet"])
else:
    eprint("No executable solution found. Solution may be one of:")
    eprint("  - solution.sh")
    eprint("  - solution.py")
    eprint("  - Cargo.toml (Rust project)")
    eprint("  - go.mod (Go project)")
    eprint("  - settings.gradle (Java project)")
    sys.exit(1)
