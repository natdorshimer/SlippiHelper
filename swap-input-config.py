import os
import configparser
import sys


def update_profile(user, profile):
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


def main(args):
    if len(args) == 2:
        user, profile = args
    else:
        user, profile = input(
            'Load controller config. Format: ${user} ${profile}\n').split()
    update_profile(user, profile)


class MyConfigParser(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.optionxform = str

    def verify_has_section(self, section: str) -> bool:
        if not self.has_section(section):
            print(
                f"The section '{section}' does not exist in the config file. Exiting.")
            exit()


def verify_path_exists(path: str) -> bool:
    if not os.path.exists(path):
        print(f"The path '{path}' does not exist. Exiting")
        exit()


if __name__ == "__main__":
    main(sys.argv[1:])
