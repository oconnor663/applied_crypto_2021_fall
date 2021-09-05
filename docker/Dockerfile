FROM gradescope/auto-builds:ubuntu-20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    default-jdk \
    git \
    libsodium-dev \
    python3 \
    python3-nacl \
    unzip

# Go
RUN curl https://dl.google.com/go/go1.17.linux-amd64.tar.gz | tar -C /usr/local -xz
ENV PATH="${PATH}:/usr/local/go/bin"

# Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --profile minimal -y
ENV PATH="${PATH}:/root/.cargo/bin"
# Update the crates.io index.
RUN /root/.cargo/bin/cargo search --limit 0
# Tell sodiumoxide to use the system copy of libsodium. This avoids wasting
# time building a static copy.
ENV SODIUM_LIB_DIR="/usr/lib/x86_64-linux-gnu/"
ENV SODIUM_SHARED="1"

# Gradle (Java). Note that the version of Gradle available through `apt-get` is
# too old and will not run the example Java solution.
RUN curl https://downloads.gradle-dn.com/distributions/gradle-7.2-bin.zip > /tmp/gradle.zip && unzip -d /usr/local/ /tmp/gradle.zip && rm /tmp/gradle.zip
ENV PATH="${PATH}:/usr/local/gradle-7.2/bin"

# Making this directory here makes it easier to run this container locally.
RUN mkdir -p /autograder/results

COPY run_solution.py /autograder/run_solution.py
COPY run_autograder /autograder/run_autograder
COPY grade.py /autograder/grade.py
COPY grading_input.json /autograder/grading_input.json
COPY grading_output.json /autograder/grading_output.json
