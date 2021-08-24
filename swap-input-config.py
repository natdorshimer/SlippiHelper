import os
import configparser
import sys


def verify_path_exists(path):
    if not os.path.exists(path):
        print(f"The path '{path}' does not exist. Exiting")
        exit()


def update_profile(user, profile):
    # Set to personal directories for ease of use

    profile_path = f"C:/Games/f1-profiles/{profile}.ini"
    config_path = f"C:/Games/{user}/User/Config/GCPadNew.ini"
    verify_path_exists(profile_path)
    verify_path_exists(config_path)

    new_profile_config = configparser.ConfigParser()
    new_profile_config.optionxform = str
    new_profile_config.read(profile_path)
    new_profile = new_profile_config['Profile']

    to_replace = configparser.ConfigParser()
    to_replace.optionxform = str
    to_replace.read(config_path)
    to_replace['GCPad1'] = new_profile

    with open(config_path, 'w') as configfile:
        to_replace.write(configfile)


def main(args):
    if(len(args) >= 2):
        user, profile = args
    else:
        user, profile = input(
            'Load controller config. Format: ${user} ${profile}\n').split()
    update_profile(user, profile)


if __name__ == "__main__":
    main(sys.argv[1:])
