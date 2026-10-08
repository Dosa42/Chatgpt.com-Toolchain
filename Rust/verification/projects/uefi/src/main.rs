#![no_std]
#![no_main]

#[repr(C)]
pub struct TableHeader {
    signature: u64,
    revision: u32,
    header_size: u32,
    crc32: u32,
    reserved: u32,
}

/// Validate the firmware system-table header before accepting the environment.
///
/// # Safety
/// Firmware must supply a valid pointer to its system table when non-null.
#[no_mangle]
pub unsafe extern "efiapi" fn efi_main(_image: usize, system_table: *const TableHeader) -> usize {
    let error_bit = 1_usize << (usize::BITS - 1);
    if system_table.is_null() {
        return error_bit | 2;
    }
    let header = unsafe { &*system_table };
    if header.signature != 0x5453_5953_2049_4249
        || header.header_size < core::mem::size_of::<TableHeader>() as u32
    {
        return error_bit | 2;
    }
    0
}

#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    loop {
        core::hint::spin_loop();
    }
}
