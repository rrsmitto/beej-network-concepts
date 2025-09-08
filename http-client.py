import sys
import socket

website = sys.argv[1]
port = sys.argv[2]
s = socket.socket()
s.connect((website, int(port)))
s.sendall("GET /file2.html HTTP/1.1\r\n\r\n".encode("ISO-8859-1"))
d = s.recv(4096).decode("ISO-8859-1")
payload = d
while not d.endswith('\r\n\r\n'):
    d = s.recv(4096).decode("ISO-8859-1")

s.close()
print(payload)
