use once_cell::sync::Lazy;
use ring::hmac;
use std::convert::TryInto;
use std::io::prelude::*;

type Mac = [u8; 32];

static SECRET_KEY: Lazy<hmac::Key> = once_cell::sync::Lazy::new(|| {
    let rng = ring::rand::SystemRandom::new();
    hmac::Key::generate(hmac::HMAC_SHA256, &rng).unwrap()
});

fn slow_leaky_check(message: &[u8], mac: &Mac) -> bool {
    let expected_mac: Mac = hmac::sign(&SECRET_KEY, message)
        .as_ref()
        .try_into()
        .unwrap();
    assert_eq!(mac.len(), expected_mac.len());
    for i in 0..mac.len() {
        if mac[i] != expected_mac[i] {
            return false;
        }
        // Simulate a really slow equality check by sleeping for 0.1 milliseconds.
        std::thread::sleep(std::time::Duration::from_micros(100));
    }
    true
}

fn discover_mac_without_key(message: &[u8]) {
    // Note that this function does not look at SECRET_KEY!
    let mut mac = [0; 32];
    // Discover each index of the correct MAC, one by one.
    for i in 0..mac.len() {
        // For the current index i, try all possible values of the byte.
        let mut slowest_time = None;
        let mut slowest_value = None;
        for value in 0..=255 {
            // We want to find the *slowest* value for the current byte, because that indicates
            // that more digits are correct. But a check might also be slow because of random CPU
            // noise (other applications doing stuff and taking up CPU time). To reduce this noise,
            // check each value several times, and use the *fastest* time we get for each value.
            let mut fastest_time = None;
            for _tries in 0..5 {
                mac[i] = value;
                let start_time = std::time::Instant::now();
                // We ignore the return value here. It's almost always going to be false, and we
                // only care about how long the check takes.
                slow_leaky_check(message, &mac);
                let duration = std::time::Instant::now() - start_time;
                if fastest_time.is_none() || duration < fastest_time.unwrap() {
                    fastest_time = Some(duration);
                }
            }
            // Now if the *fastest* time for this value was slower than the *slowest* time we've
            // seen so far at this index, save this value.
            if slowest_time.is_none() || fastest_time.unwrap() > slowest_time.unwrap() {
                slowest_time = fastest_time;
                slowest_value = Some(value);
            }
        }
        // Keep whichever value was the slowest at the current index, and move on to the next
        // index.
        mac[i] = slowest_value.unwrap();
        // Print these values to the terminal so that we can watch the progress.
        print!("{}, ", slowest_value.unwrap());
        std::io::stdout().flush().unwrap();
    }
    println!();
    // Confirm that the end result is correct.
    assert!(slow_leaky_check(message, &mac));
    println!("SUCCESS!");
}

fn main() {
    let message = b"hello world";
    let expected_mac: Mac = hmac::sign(&SECRET_KEY, message)
        .as_ref()
        .try_into()
        .unwrap();
    println!("{:?}", expected_mac.as_ref());
    print!("[");
    discover_mac_without_key(b"hello world");
}
