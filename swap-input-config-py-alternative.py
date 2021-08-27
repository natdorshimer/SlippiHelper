import os
import configparser
import sys
import win32gui
import re


def update_profile(user: str, profile: str):
    # Set to personal directories for ease of use

    profile_path = f"C:/Games/f1-profiles/{profile}.ini"
    config_path = f"C:/Games/{user}/User/Config/GCPadNew.ini"
    verify_path_exists(profile_path)
    verify_path_exists(config_path)

    new_profile_config = MyConfigParser()
    new_profile_config.read(profile_path)
    new_profile_config.verify_has_section('Profile')
    new_profile = new_profile_config['Profile']

    to_replace = MyConfigParser()
    to_replace.read(config_path)
    to_replace.verify_has_section('GCPad1')
    to_replace['GCPad1'] = new_profile

    with open(config_path, 'w') as configfile:
        to_replace.write(configfile)


def verify(predicate: bool, error_message: str):
    if not predicate:
        print(error_message)
        exit()


def main(args):
    if len(args) == 2:
        user, profile = args
    else:
        user_input = input(
            'Load controller config. Format: ${user} ${profile}\n').split()
        verify(len(user_input) >= 2, 'Both user and profile are required')
        user, profile = user_input[:2]

    update_profile(user, profile)
    set_window_active(".*| Wrote memory card.*")


class MyConfigParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.optionxform = str

    def verify_has_section(self, section: str):
        verify(
            self.has_section(section),
            f"The section '{section}' does not exist in the config file. Exiting."
        )


def verify_path_exists(path: str):
    verify(
        os.path.exists(path),
        f"The path '{path}' does not exist. Exiting"
    )


def find_window_wildcard(wildcard: str):
    handle = None

    """Callback that sets handle to the first window that matches the wildcard"""
    def find_matching_window(hwnd, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            nonlocal handle
            handle = hwnd

    win32gui.EnumWindows(find_matching_window, wildcard: str)
    return handle


def set_window_active(window_name: str):
    handle = find_window_wildcard(window_name)
    win32gui.BringWindowToTop(handle)


if __name__ == "__main__":
    main(sys.argv[1:])
