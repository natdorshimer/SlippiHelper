use bindings::Windows::Win32::{
    Foundation::{BOOL, HWND, LPARAM, PWSTR},
    UI::WindowsAndMessaging::{BringWindowToTop, EnumWindows, GetWindowTextW},
};
use regex::Regex;

pub fn set_window_active(window_matching_re: Regex) {
    unsafe {
        let handle = find_window_wildcard(window_matching_re);
        BringWindowToTop(handle);
    }
}

unsafe fn get_window_text(handle: HWND) -> String {
    let mut text: [u16; 512] = [0; 512];
    let len = GetWindowTextW(handle, PWSTR(text.as_mut_ptr()), text.len() as i32);
    String::from_utf16_lossy(&text[..len as usize])
}

unsafe fn find_window_wildcard(re: Regex) -> Option<HWND> {
    struct Message {
        handle: Option<HWND>,
        re: Regex,
    }

    //Windows API in rust is pretty rough since closures aren't supported for EnumWindows
    let mut message = Message { handle: None, re };
    let lparam_message_ptr = LPARAM(std::ptr::addr_of_mut!(message) as isize);

    //Find window that matches message.re and store it into message.handle
    pub unsafe extern "system" fn find_matching_window(hwnd: HWND, lparam: LPARAM) -> BOOL {
        let message_ptr = lparam.0 as *mut Message;
        let mut message = &mut *message_ptr;
        let is_match = message.re.is_match(get_window_text(hwnd).as_str());
        message.handle = if is_match { Some(hwnd) } else { None };
        BOOL::from(is_match)
    }

    EnumWindows(Some(find_matching_window), lparam_message_ptr);
    message.handle.to_owned()
}
