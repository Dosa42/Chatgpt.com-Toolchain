/// Greatest common divisor exposed through the C ABI.
#[no_mangle]
pub extern "C" fn toolchain_gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let remainder = a % b;
        a = b;
        b = remainder;
    }
    a
}
