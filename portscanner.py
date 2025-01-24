import socket
import threading
from datetime import datetime

# Define global variables
open_ports = []

# Define a function for the port scanning task
def scan_port(target, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set timeout to 1 second for faster scanning
        result = sock.connect_ex((target, port))

        # If the connection was successful, mark the port as open
        if result == 0:
            print(f"Port {port}: OPEN")
            open_ports.append(port)
        sock.close()
    except socket.error as e:
        # Handle any socket errors (e.g., network issue)
        print(f"Error scanning port {port}: {e}")

# Thread function to scan multiple ports
def scan_ports_thread(target, start_port, end_port):
    print(f"Scanning target: {target}")
    print(f"Scanning ports: {start_port}-{end_port}")
    print("Start time:", datetime.now())

    threads = []
    # Start threads to scan each port in the given range
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"Open ports found: {open_ports}")
    print("End time:", datetime.now())
    print("Scan complete.")

# Input validation
def validate_input():
    target = input("Enter the target (IP or hostname): ")
    if not target:
        print("Target is required!")
        return None, None, None

    try:
        start_port = int(input("Enter the start port: "))
        end_port = int(input("Enter the end port: "))
        if start_port > end_port:
            print("Start port should be less than or equal to end port!")
            return None, None, None
        return target, start_port, end_port
    except ValueError:
        print("Please enter valid port numbers.")
        return None, None, None

# Main function
if __name__ == "__main__":
    target, start_port, end_port = validate_input()
    
    if target and start_port and end_port:
        scan_ports_thread(target, start_port, end_port)
