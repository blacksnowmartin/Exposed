from __future__ import annotations

import argparse
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Decrypt .encrypted files in a chosen directory using a local Fernet key."
    )
    parser.add_argument("target", help="Directory that contains the encrypted files.")
    parser.add_argument(
        "--key-file",
        default="file.key",
        help="Path to the local key file to use. Default: file.key",
    )
    return parser


def iter_encrypted_files(target_dir: Path, key_path: Path, script_path: Path):
    for path in target_dir.rglob("*.encrypted"):
        if not path.is_file():
            continue
        if path == key_path or path == script_path:
            continue
        yield path


def decrypt_file(path: Path, cipher: Fernet) -> None:
    original_path = path.with_suffix("")
    decrypted_data = cipher.decrypt(path.read_bytes())
    original_path.write_bytes(decrypted_data)
    path.unlink()


def main() -> None:
    args = build_parser().parse_args()
    target_dir = Path(args.target).expanduser().resolve()
    key_path = Path(args.key_file).expanduser().resolve()
    script_path = Path(__file__).resolve()

    if not target_dir.is_dir():
        raise SystemExit(f"Target directory not found: {target_dir}")
    if not key_path.is_file():
        raise SystemExit(f"Key file not found: {key_path}")

    cipher = Fernet(key_path.read_bytes())

    decrypted_count = 0
    for file_path in iter_encrypted_files(target_dir, key_path, script_path):
        try:
            decrypt_file(file_path, cipher)
            decrypted_count += 1
        except InvalidToken as exc:
            raise SystemExit(
                "The key file does not match the encrypted files."
            ) from exc

    print(f"Decrypted {decrypted_count} file(s).")


if __name__ == "__main__":
    main()
