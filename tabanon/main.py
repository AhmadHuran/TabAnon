from tabanon.lib import encrypt, decrypt
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="tabanon: Table anonymization. "
                    "Supports csv and xlsx tables.")

    # Mandatory data input file (positional argument)
    parser.add_argument(
            "data_input_file",
            type=str,
            help="Path to the data input file")

    # Mandatory info file (using --info flag)
    parser.add_argument(
            "--info",
            type=str,
            required=True,
            help="Path to the info file")

    # Optional mode argument (default is 'encrypt')
    help_msg = ("Mode of operation: encrypt or decrypt. In decrypt mode, "
                "the key is read from info file.")
    parser.add_argument(
            "--mode",
            type=str,
            choices=["encrypt", "decrypt"],
            default="encrypt",
            help=help_msg)

    # Optional key argument (default is None)
    parser.add_argument(
            "--key",
            type=str,
            default=None,
            help="Encryption key (default is None)")

    # Optional output file (using -o flag)
    parser.add_argument(
            "-o",
            "--output",
            type=str,
            default=None,
            help="Output file name (default None)")

    return parser.parse_args()
def main():
    args = parse_arguments()
    file = args.data_input_file
    action = args.mode
    key = args.key
    info = args.info
    output = args.output

    if not key is None:
        key = key.encode()

    if action == "encrypt":
        encrypt(file, info, key, output)
    else:
        decrypt(file, info, output)


if __name__ == "__main__":
    main()


