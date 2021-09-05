use serde::{Deserialize, Serialize};
use sodiumoxide::crypto::secretbox::{self, Key, Nonce};

#[derive(Deserialize)]
struct Input {
    problem1: Vec<i64>,
    problem2: String,
    problem3: String,
    problem4: String,
    problem5: Vec<String>,
}

#[derive(Default, Serialize)]
struct Output {
    problem1: Problem1Output,
    problem2: String,
    problem3: String,
    problem4: String,
    problem5: String,
}

#[derive(Default, Serialize)]
struct Problem1Output {
    sum: i64,
    product: i64,
}

fn main() {
    let input: Input = serde_json::from_reader(std::io::stdin()).expect("parsing JSON failed");
    let mut output = Output::default();

    // Problem 1
    output.problem1.sum = input.problem1.iter().sum();
    output.problem1.product = input.problem1.iter().product();

    // Problem 2
    let output_bytes = hex::decode(&input.problem2).expect("invalid hex");
    output.problem2 = String::from_utf8_lossy(&output_bytes).into();

    // Problem 3
    output.problem3 = hex::encode(&input.problem3);

    // Problem 4
    let ciphertext_bytes = hex::decode(input.problem4).expect("invalid hex");
    let key = Key(['A' as u8; 32]);
    let nonce = Nonce(['B' as u8; 24]);
    let plaintext_bytes =
        secretbox::open(&ciphertext_bytes, &nonce, &key).expect("decryption failed");
    output.problem4 = String::from_utf8_lossy(&plaintext_bytes).into();

    // Problem 5
    let key = Key(['C' as u8; 32]);
    let nonce = Nonce(['D' as u8; 24]);
    for ciphertext_hex in &input.problem5 {
        let ciphertext_bytes = hex::decode(ciphertext_hex).expect("invalid hex");
        if let Ok(plaintext_bytes) = secretbox::open(&ciphertext_bytes, &nonce, &key) {
            output.problem5 = String::from_utf8_lossy(&plaintext_bytes).into();
            break;
        }
    }

    // Output
    serde_json::to_writer_pretty(std::io::stdout(), &output).expect("output failed");
    println!()
}
