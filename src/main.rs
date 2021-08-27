#![windows_subsystem = "windows"]

use configparser::ini::Ini;
use std::env;
use std::io;

fn update_profile(user: &String, profile: &String) {
    let mut config = Ini::new_cs();
    let profile_path = &format!("C:/Games/f1-profiles/{}.ini", profile);
    let config_path = &format!("C:/Games/{}/User/Config/GCPadNew.ini", user);

    let profile = config
        .load(profile_path)
        .expect(format!("No config file found at path {}", profile_path).as_str())
        .get("Profile")
        .expect("The section 'Profile' does not exist in the config file. Exiting.")
        .clone();

    config
        .load(config_path)
        .expect(format!("No config file found at path {}", config_path).as_str());

    config.get_mut_map().insert("GCPad1".to_owned(), profile);

    config.write(config_path).expect(
        format!(
            "Error while writing to configuration file with path {}",
            config_path
        )
        .as_str(),
    );
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let error_msg = "Not enough arguments provided. Exiting";
    let user = args.get(1).expect(error_msg);
    let profile = args.get(2).expect(error_msg);
    update_profile(user, profile);
}

pub fn get_line(message: &str) -> String {
    println!("{}", message);
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .map(|_| input.trim_end().to_string())
        .expect("Error parsing input. Exiting.")
}
