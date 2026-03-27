#!/usr/bin/env python3
"""
decrypt_downloads.py – Educational demo to decrypt files that were
previously encrypted with a simple Fernet key.

Prerequisites:
    pip install cryptography

How it works:
    1.  Load the encryption key from `key.key` (44‑byte Fernet key).
    2.  Scan the user’s ~/Downloads folder for files ending in `.locked`.
    3.  For each file, decrypt the data in `<file>.locked` and write the
        result to `<file>`.
    4.  Remove the temporary `.locked` file.

The script now correctly handles filenames that already end with
`.locked` (no double‑extension is attempted).
"""

import os
import sys
from pathlib import Path
from cryptography.fernet import Fernet

# --------------------------------------------------------------------------- #
# Decryption helper
# --------------------------------------------------------------------------- #
def decrypt(file_path: Path, key: bytes) -> None:
    """
    Decrypt a single file that was encrypted to <file_path>.locked.

    Parameters
    ----------
    file_path : Path
        Path to the *original* file (without the .locked suffix).
    key : bytes
        44‑byte Fernet key used for decryption.

    Raises
    ------
    Exception
        Any error during decryption is caught and printed by the caller.
    """
    # Ensure the file name is without a trailing .locked
    if file_path.suffix == ".locked":
        file_path = file_path.with_suffix("")

    cipher = Fernet(key)

    encrypted_file = str(file_path) + ".locked"
    if not os.path.exists(encrypted_file):
        # Defensive: the file might have been removed meanwhile
        raise FileNotFoundError(f"{encrypted_file} does not exist")

    # Decrypt
    with open(encrypted_file, "rb") as f_in, open(file_path, "wb") as f_out:
        encrypted_data = f_in.read()
        decrypted_data = cipher.decrypt(encrypted_data)
        f_out.write(decrypted_data)

    # Clean up the temporary encrypted copy
    os.remove(encrypted_file)


# --------------------------------------------------------------------------- #
# Batch decryption for the Downloads folder
# --------------------------------------------------------------------------- #
def batch_decrypt(key: bytes, folder: str = "Downloads") -> int:
    """
    Scan the specified folder for *.locked files and decrypt each one.

    Parameters
    ----------
    key : bytes
        Fernet key for decryption.
    folder : str, optional
        Subfolder under the user’s home directory (default: 'Downloads').

    Returns
    -------
    int
        Number of files successfully decrypted.
    """
    download_path = Path.home() / folder
    if not download_path.exists():
        print("[!] Downloads folder not found!")
        sys.exit(1)

    total = 0
    # Look only at files that end with .locked once
    for file in download_path.glob("*.locked"):
        if file.is_file():
            try:
                decrypt(file.with_suffix(""), key)
                total += 1
            except Exception as e:
                print(f"Error decrypting {file}: {e}")

    return total


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    # Load the encryption key
    try:
        key_file = Path("key.key")
        with open(key_file, "rb") as f:
            key = f.read()
        print(f"[+] Decryption key loaded: {len(key)} bytes")
    except FileNotFoundError:
        print("[!] Encryption key not found – create a key with `keygen.py`")
        sys.exit(1)
    except Exception as e:
        print("[!] Unexpected error while loading the key:", e)
        sys.exit(1)

    # Run the batch decryption
    total_decrypted = batch_decrypt(key)

    if total_decrypted > 0:
        print(f"[+] Successfully decrypted {total_decrypted} files.")
    else:
        print("[-] No encrypted files found.")


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()