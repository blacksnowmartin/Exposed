import argparse
import os
import sys

from cryptography.fernet import Fernet, InvalidToken


def load_key(args):
    if args.key:
        return args.key.encode()

    if args.key_file:
        with open(args.key_file, "rb") as handle:
            return handle.read().strip()

    raise ValueError("Provide either --key or --key-file.")


def decrypt_directory(directory, cipher, skip_files):
    decrypted = []
    failed = []

    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        if os.path.abspath(path) in skip_files:
            continue

        with open(path, "rb") as handle:
            encrypted_data = handle.read()

        try:
            plain_data = cipher.decrypt(encrypted_data)
        except InvalidToken:
            failed.append(name)
            continue

        with open(path, "wb") as handle:
            handle.write(plain_data)
        decrypted.append(name)

    return decrypted, failed


def main():
    parser = argparse.ArgumentParser(
        description="Reverse the Fernet file encryption used by malware.py."
    )
    parser.add_argument(
        "--key",
        help="The original Fernet key as a base64 string.",
    )
    parser.add_argument(
        "--key-file",
        help="Path to a file containing the original Fernet key.",
    )
    parser.add_argument(
        "--dir",
        default=os.getcwd(),
        help="Directory containing the encrypted files. Defaults to the current directory.",
    )
    args = parser.parse_args()

    try:
        key = load_key(args)
        cipher = Fernet(key)
    except Exception as exc:
        print(f"Unable to initialize decryption: {exc}", file=sys.stderr)
        sys.exit(1)

    skip_files = {os.path.abspath(__file__)}
    if args.key_file:
        skip_files.add(os.path.abspath(args.key_file))

    decrypted, failed = decrypt_directory(args.dir, cipher, skip_files)

    print(f"Decrypted {len(decrypted)} file(s).")
    if decrypted:
        print("Recovered:", ", ".join(decrypted))

    if failed:
        print(
            "Skipped files that do not match this key or are not Fernet-encrypted:",
            ", ".join(failed),
        )


if __name__ == "__main__":
    main()
