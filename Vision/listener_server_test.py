import socket
from listener_server import HOST, PORT 

# Run Listener Server Locally and calls vision script
# Only Tests Massive failure of script, not integration
def check_tcp_port(host,port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)  # Set a 5-second timeout
        result = s.connect_ex((host, port))

        cmd = "run_vision"
        s.sendall(cmd.encode("utf-8"))

        if result == 0:
            print(f"Port {port} on {host} is OPEN")
        else:
            print(f"Port {port} on {host} is CLOSED or filtered (Error code: {result})")


if __name__ == "__main__":
    check_tcp_port(HOST, PORT)
