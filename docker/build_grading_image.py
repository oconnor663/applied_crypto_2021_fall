#! /usr/bin/env python3

import os
from os import path
import shutil
import subprocess
import sys
import tempfile

HERE = path.dirname(path.realpath(__file__))

if len(sys.argv) < 2:
    print("Usage: build_grading_image.py <pset_dir> [DOCKER OPTIONS]")
    sys.exit(1)
pset_dir = sys.argv[1]

with tempfile.TemporaryDirectory() as tempdir:
    # Copy all the files under docker/ to the tempdir.
    shutil.copytree(HERE, tempdir, dirs_exist_ok=True)

    # Copy the grading script from the problem set directory.
    shutil.copy(path.join(pset_dir, "grade.py"), path.join(tempdir, "grade.py"))

    # If grading_input.json and grading_output.json don't exist in the problem
    # set directory, use the example input and output files in their place. The
    # idea here is that the grading input and output files will not be visible
    # to students.
    example_input_src = path.join(pset_dir, "example_input.json")
    example_output_src = path.join(pset_dir, "example_output.json")
    grading_input_src = path.join(pset_dir, "grading_input.json")
    grading_output_src = path.join(pset_dir, "grading_output.json")
    grading_input_dest = path.join(tempdir, "grading_input.json")
    grading_output_dest = path.join(tempdir, "grading_output.json")
    if not path.exists(grading_input_src):
        assert not path.exists(grading_output_src)
        shutil.copy(example_input_src, grading_input_dest)
        shutil.copy(example_output_src, grading_output_dest)
    else:
        shutil.copy(grading_input_src, grading_input_dest)
        shutil.copy(grading_output_src, grading_output_dest)

    # Build the Docker image.
    image_name = "applied_crypto_grading"
    command = ["docker", "build", "-t", image_name, "."] + sys.argv[2:]
    subprocess.run(command, cwd=tempdir, check=True)
