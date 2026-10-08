fn main() {
    let mut hash = 0xcbf29ce484222325_u64;
    for argument in std::env::args().skip(1) {
        for byte in argument.bytes() {
            hash ^= u64::from(byte);
            hash = hash.wrapping_mul(0x100000001b3);
        }
    }
    println!("{hash:016x}");
}
