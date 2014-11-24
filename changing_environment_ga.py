import ConfigParser
import argparse
from main import set_global_variables, generate_data
import sys
from string import ascii_uppercase

def parse_everything():
    # Parse any conf_file specification
    conf_parser = argparse.ArgumentParser(
        description='The changing environments program.')
    conf_parser.add_argument("-c", "--config_file", nargs=1)
    conf_parser.add_argument("-o", '--output_folder', nargs=1)
    args = conf_parser.parse_args()

    config = ConfigParser.SafeConfigParser()
    config.read([args.config_file[0]])
    config.set("DEFAULT", "output_folder", args.output_folder[0])
    return config

def main():
    config = parse_everything()
    set_global_variables(config)
    generate_data()

if __name__ == "__main__":
    main()
