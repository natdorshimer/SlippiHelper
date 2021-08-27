fn main() {
    windows::build! {
        Windows::Win32::UI::WindowsAndMessaging::{
                BringWindowToTop,
                EnumWindows,
                GetWindowTextW
        },
        Windows::Win32::Foundation::*
    };
}
