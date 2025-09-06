# Master NMap effortlessly

No.
Category

Description
1
auth

Determination of authentication credentials.

2
broadcast

Scripts, which are used for host discovery by broadcasting and the discovered hosts, can be automatically added to the remaining scans.

3
brute

Executes scripts that try to log in to the respective service by brute-forcing with credentials.

4
default

Default scripts executed by using the -sC option.

5
discovery

Evaluation of accessible services.

6
dos

These scripts are used to check services for denial of service vulnerabilities and are used less as it harms the services.

7
exploit

This category of scripts tries to exploit known vulnerabilities for the scanned port.

8
external

Scripts that use external services for further processing.

9
fuzzer

This uses scripts to identify vulnerabilities and unexpected packet handling by sending different fields, which can take much time.

10
intrusive

Intrusive scripts that could negatively affect the target system.

11
malware

Checks if some malware infects the target system.

13
safe

Defensive scripts that do not perform intrusive and destructive access.

14
version

Extension for service detection.

15
vuln

Identification of specific vulnerabilities.

Some useful NSE examples that you may use in your scans include:

## Nmap command

### Description

nmap -Pn -script=http-sitemap-generator scanme.nmap.org

http site map generator.

nmap -Pn -script=dns-brute domain.com

Brute forces DNS hostnames guessing subdomains.

nmap -script whois* domain.com

Whois query.

nmap -p80 -script http-unsafe-output-escaping scanme.nmap.org

Detect cross site scripting vulnerabilities.

nmap -p80 -script http-sql-injection scanme.nmap.org

Detect cross site scripting vulnerabilities.

Reviewed and edited by:

### Martin Kitonga 
