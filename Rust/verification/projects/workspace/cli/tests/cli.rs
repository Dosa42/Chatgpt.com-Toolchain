use std::process::Command;

#[test]
fn computes_a_real_sum() {
    let output = Command::new(env!("CARGO_BIN_EXE_toolchain-cli"))
        .args(["12", "-4", "9"])
        .output()
        .unwrap();
    assert!(output.status.success());
    assert_eq!(String::from_utf8(output.stdout).unwrap().trim(), "17");
}

#[test]
fn rejects_invalid_input_and_overflow() {
    for arguments in [vec!["invalid"], vec!["9223372036854775807", "1"]] {
        let output = Command::new(env!("CARGO_BIN_EXE_toolchain-cli"))
            .args(arguments)
            .output()
            .unwrap();
        assert_eq!(output.status.code(), Some(2));
        assert!(!output.stderr.is_empty());
    }
}
