#![no_std]

/// Calculate an unsigned sum without the standard library.
pub fn checked_sum(values: &[u32]) -> Option<u32> {
    values.iter().try_fold(0_u32, |sum, &value| sum.checked_add(value))
}
