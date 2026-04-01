Usage Examples

Basic usage against a local test server:

bash
 Copy
python3 dir_bruteforcer.py http://localhost:8000 --wordlist common_paths.txt

Against an actual target site, using a smaller wordlist:

bash
 Copy
curl -s https://example-site.com | grep -o '/[a-z0-9_-]+/' > my_wordlist.txt 
python3 dir_bruteforcer.py https://example-site.com --wordlist my_wordlist.txt
Ethical Considerations

Be respectful of server load: use the default max_workers=10 which balances speed and politeness.

Avoid testing sensitive areas that might trigger alerts (like /admin).

For production scanning, add rate limiting or exponential backoff.

Improvement Ideas

Add output to CSV/XML for parsing

Implement user-agent rotation

Add support for cookie/session handling

Use proper error handling instead of try/except blocks

Ethical Hacking Approach
This script requires permission before use against any live website. Unauthorized access attempts may violate computer crime laws.
Testing Against Test Servers
To test this script:
text
 Copy
mkdir -p /var/www/html/common_paths_test
echo "<!DOCTYPE html><html><body>Hello from test!</body></html>" > /var/www/html/common_paths_test/admin.html
Then run:
bash
 Copy
python3 dir_bruteforcer.py http://localhost:8000 --wordlist common_paths.txt
Ethical Practice Notes

Start with smaller wordlists first (like the common_paths.txt)

For large sites, use binary search on known paths when available

For sensitive sites, limit concurrent requests to avoid detection as bot traffic