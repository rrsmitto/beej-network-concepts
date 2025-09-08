import socket
import time

def system_time_since_1990():
    seconds_delta = 2208988800
    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch

for i in range(4):
    print("Requesting in:", 4-i)
    time.sleep(1)

with socket.socket() as nist_socket:
    nist_socket.connect(('time.nist.gov', 37))
    nist_time = int.from_bytes(nist_socket.recv(4))
    nist_socket.close()
    print('Nist time:', nist_time)
    system_time = system_time_since_1990()
    print('System time:', system_time)
    print('Delta:', system_time - nist_time)
