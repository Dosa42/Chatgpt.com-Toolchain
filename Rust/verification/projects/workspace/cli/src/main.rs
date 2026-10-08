fn main() {
    let values: Result<Vec<i64>, _> = std::env::args().skip(1).map(|value| value.parse()).collect();
    match values {
        Ok(values) => match toolchain_math::checked_sum(&values) {
            Some(total) => println!("{total}"),
            None => {
                eprintln!("Sum overflowed i64");
                std::process::exit(2);
            }
        },
        Err(error) => {
            eprintln!("Invalid integer: {error}");
            std::process::exit(2);
        }
    }
}
