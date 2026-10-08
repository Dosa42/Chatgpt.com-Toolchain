use std::hint::black_box;
use std::time::Instant;

fn main() {
    let started = Instant::now();
    let mut checksum = 0_u64;
    for value in 1..1_000_000 {
        checksum ^= toolchain_math::gcd(black_box(value), black_box(600_851_475_143));
    }
    println!(
        "iterations=999999 elapsed_ns={} checksum={}",
        started.elapsed().as_nanos(),
        black_box(checksum)
    );
}
