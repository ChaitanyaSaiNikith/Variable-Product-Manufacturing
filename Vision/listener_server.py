import socket
import vision

HOST = "10.241.34.37"
PORT = 30002

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Server started. Waiting for UR5 on {HOST}:{PORT}...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024).decode('utf-8')
                if data == "run_vision":
                    vision.main()
                conn.sendall(b"UR Command Recieved")  # Send acknowledgment back to robot

if __name__ == "__main__":
    start()
