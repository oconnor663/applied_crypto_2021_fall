use std::io::prelude::*;

// COPIED from https://github.com/dcrewi/rust-mersenne-twister
const F: u32 = 1812433253;
const W: u32 = 32;
const N: usize = 624;
const M: usize = 397;
const R: u32 = 31;
const A: u32 = 0x9908B0DF;
const U: u32 = 11;
const D: u32 = 0xFFFFFFFF;
const S: u32 = 7;
const B: u32 = 0x9D2C5680;
const T: u32 = 15;
const C: u32 = 0xEFC60000;
const L: u32 = 18;
const LOWER_MASK: u32 = (1 << R) - 1; // That is, the binary number of r 1's
const UPPER_MASK: u32 = !LOWER_MASK; // lowest w bits of (not lower_mask)

pub struct MT {
    array: [u32; N],
    index: usize,
}

impl MT {
    pub fn seed(seed: u32) -> Self {
        let mut array = [0; N];
        array[0] = seed;
        for i in 1..N {
            array[i] = F
                .wrapping_mul(array[i - 1] ^ (array[i - 1] >> (W - 2)))
                .wrapping_add(i as u32);
        }
        Self { array, index: N }
    }

    pub fn extract_number(&mut self) -> u32 {
        if self.index >= N {
            if self.index > N {
                panic!();
            }
            self.twist();
        }

        let mut y = self.array[self.index];
        y ^= (y >> U) & D;
        y ^= (y << S) & B;
        y ^= (y << T) & C;
        y ^= y >> L;

        self.index += 1;
        y
    }

    fn twist(&mut self) {
        for i in 0..N - 1 {
            let x = (self.array[i] & UPPER_MASK) + (self.array[(i + 1) % N] & LOWER_MASK);
            let mut x_a = x >> 1;
            if (x % 2) != 0 {
                // lowest bit of x is 1
                x_a = x_a ^ A;
            }
            self.array[i] = self.array[(i + M) % N] ^ x_a;
        }
        self.index = 0;
    }
}

fn undo_right_shift_xor_mask(mut y: u32, shift: u32, mask: u32) -> u32 {
    // One bit at a time.
    for bit_index in 0..32 {
        if bit_index + shift < 32 {
            let bit_mask = 1 << (31 - bit_index);
            y ^= ((y & bit_mask) >> shift) & mask;
        }
    }
    y
}

fn undo_left_shift_xor_mask(mut y: u32, shift: u32, mask: u32) -> u32 {
    // One bit at a time.
    for bit_index in (0..32).rev() {
        if bit_index >= shift {
            let bit_mask = 1 << (31 - bit_index);
            y ^= ((y & bit_mask) << shift) & mask;
        }
    }
    y
}

fn untemper(mut y: u32) -> u32 {
    // Here's what we have to undo:
    // let mut y = self.array[self.index];
    // y ^= (y >> U) & D;
    // y ^= (y << S) & B;
    // y ^= (y << T) & C;
    // y ^= y >> L;

    y = undo_right_shift_xor_mask(y, L, !0);
    y = undo_left_shift_xor_mask(y, T, C);
    y = undo_left_shift_xor_mask(y, S, B);
    y = undo_right_shift_xor_mask(y, U, D);
    y
}

fn main() {
    let mut input_ints: Vec<u32> = Vec::new();
    for line in std::io::stdin().lock().lines() {
        input_ints.push(line.expect("io error").trim().parse().expect("invalid int"));
    }
    if input_ints.len() < N {
        eprintln!("needs {} ints", N);
        std::process::exit(1);
    }
    let mut untempered = [0; N];
    for i in 0..N {
        untempered[i] = untemper(input_ints[i]);
    }
    let mut rng_clone = MT {
        array: untempered,
        index: N,
    };

    // rng_clone is now correctly initialized, and N input ints have been "consumed". Run the RNG
    // forward to the end of the input stream.
    for i in N..input_ints.len() {
        assert_eq!(rng_clone.extract_number(), input_ints[i]);
    }

    // Finally, print the next few elements after the end of the input stream.
    for _ in 0..10 {
        println!("{}", rng_clone.extract_number());
    }
}
