import socket

def port_scanner(ip, start_port, end_port):
    try:
        # Convert hostname to IPv4 address
        target = socket.gethostbyname(ip)
    except socket.gaierror:
        print(f"Unable to resolve {ip}. Please check the name and try again.")
        return
    
    print(f"Scanning ports for {target}...")
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second
        
        try:
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} is open.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            sock.close()

# Get user input
ip_input = input("Enter the target IP or hostname: ")
start_port = int(input("Enter the starting port number: "))
end_port = int(input("Enter the ending port number: "))

port_scanner(ip_input, start_port, end_port)