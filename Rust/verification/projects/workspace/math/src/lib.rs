/// Compute the greatest common divisor using Euclid's algorithm.
pub fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let remainder = a % b;
        a = b;
        b = remainder;
    }
    a
}

/// Sum signed values, returning None if the result overflows.
pub fn checked_sum(values: &[i64]) -> Option<i64> {
    values.iter().try_fold(0_i64, |sum, &value| sum.checked_add(value))
}

/// Calculate a dot product with length and overflow checking.
pub fn checked_dot(a: &[i64], b: &[i64]) -> Option<i64> {
    if a.len() != b.len() {
        return None;
    }
    a.iter().zip(b).try_fold(0_i64, |sum, (&x, &y)| {
        sum.checked_add(x.checked_mul(y)?)
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn arithmetic_and_overflow() {
        assert_eq!(checked_sum(&[12, -4, 9]), Some(17));
        assert_eq!(checked_sum(&[]), Some(0));
        assert_eq!(checked_sum(&[i64::MAX, 1]), None);
        assert_eq!(checked_dot(&[1, 2, 3], &[4, 5, 6]), Some(32));
        assert_eq!(checked_dot(&[1], &[]), None);
        assert_eq!(checked_dot(&[i64::MAX], &[2]), None);
    }

    #[test]
    fn gcd_boundaries_and_divisibility() {
        assert_eq!(gcd(0, 0), 0);
        assert_eq!(gcd(u64::MAX, 0), u64::MAX);
        assert_eq!(gcd(48, 18), 6);
        for a in 1..100 {
            for b in 1..100 {
                let divisor = gcd(a, b);
                assert_eq!(a % divisor, 0);
                assert_eq!(b % divisor, 0);
                assert_eq!(divisor, gcd(b, a));
            }
        }
    }
}
