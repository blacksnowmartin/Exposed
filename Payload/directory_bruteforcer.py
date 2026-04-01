#!/usr/bin/env python3
# dir_bruteforcer.py - A simple web directory brute force tool

import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_dir(base_url, wordlist_file):
    """Check if a URL exists."""
    
    try:
        with open(wordlist_file) as f:
            words = [line.strip() for line in f if line.strip()]
            
        results = []
        
        def test_path(path):
            full_url = f"{base_url}/{path}"
            response = requests.get(full_url, allow_redirects=False)
            
            # Check status code range (200=normal file, 3xx=redirect, others=error)
            if 200 <= response.status_code < 400:
                return f"FOUND: {full_url} ({response.status_code})"
            else:
                return None
                
        with ThreadPoolExecutor(max_workers=min(len(words), 10)) as executor:
            futures = [executor.submit(test_path, word) for word in words]
            
            # Process completed tasks
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
                
        return sorted(results)
        
    except FileNotFoundError:
        print(f"Error: Wordlist file '{wordlist_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Directory Bruteforcer")
    parser.add_argument("target", help="Base URL (e.g., http://example.com)")
    parser.add_argument("--wordlist", required=True, help="File with paths to try")
    
    args = parser.parse_args()
    
    print(f"Starting scan on {args.target} using {args.wordlist}")
    
    # Add trailing slash if needed
    base_url = args.target.rstrip('/') + '/'
    
    results = check_dir(base_url, args.wordlist)
    
    if results:
        for result in results:
            print(result)
    else:
        print("No obvious directories found.")