import ConfigParser
import argparse
from main import set_global_variables, generate_data
import sys
from string import ascii_uppercase

def add_arguements(parser):
    parser.add_argument('--number_of_generations', type=int, help='number of generations')

    parser.add_argument('--number_of_organisms', type=int, help='number of organisms')

    parser.add_argument('--mutation_rate', type=float, help='mutation rate')

    parser.add_argument('--target_string', type=str, help='target string')

    parser.add_argument('--letters', type=str, help='letters')

    parser.add_argument('--output_file', help='output_file')
    parser.add_argument("-v", "--verbose", action="store_true")
def parse_everything():
    # Parse any conf_file specification
    # We make this parser with add_help=False so that
    # it doesn't parse -h and print help.
    conf_parser = argparse.ArgumentParser(
        description='The changing environments program.', # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # Turn off help, so we print all options in response to -h
        add_help=False
        )
    conf_parser.add_argument("-c", "--conf_file",
                        help="Specify config file", metavar="FILE")

    args, remaining_argv = conf_parser.parse_known_args()

    if args.conf_file:
        config = ConfigParser.SafeConfigParser()
        config.read([args.conf_file])
        defaults = dict(config.items("DEFAULT"))
    else:
        defaults = {}

    # Parse rest of arguments
    # Don't suppress add_help here so it will handle -h
    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser]
        )
    parser.set_defaults(**defaults)
    add_arguements(parser)
    args = parser.parse_args(remaining_argv)
    return args

def main():
    args = parse_everything()
    set_global_variables(args)
    generate_data()

if __name__ == "__main__":
    main()
