import os

TCP_PTCL_NUMBER = b'\x06'

def validate_checksum(ip_file, tcp_file):
    source_ip, dest_ip = read_address_file(ip_file)
    source_ip_bytes = ip_to_bytes(source_ip)
    dest_ip_bytes = ip_to_bytes(dest_ip)

    checksum, tcp_data_zero_checksum = read_tcp_file(tcp_file)
    tcp_length = get_tcp_length(tcp_file)
    
    pseudo_header = pseudo_ip_header(source_ip_bytes, dest_ip_bytes, TCP_PTCL_NUMBER, tcp_length)

    computed_checksum = compute_checksum(pseudo_header, tcp_data_zero_checksum)

    checksums_match = False
    if computed_checksum == checksum:
        checksums_match = True

    return checksums_match

def compute_checksum(pseudo_header, zero_checksum_tcp_data):
    tcp_data = pseudo_header + zero_checksum_tcp_data

    if len(tcp_data) % 2 == 1:
        tcp_data += b'\x00'

    offset = 0
    total = 0
    while offset < len(tcp_data):
        word = int.from_bytes(tcp_data[offset:offset+2])

        total += word
        total = (total & 0xffff) + (total >> 16)
        
        offset += 2

    return (~total) & 0xffff
    
def read_tcp_file(filename):
    tcp_bytes = b''
    with open(filename, 'rb') as f:
        for byte in f:
            tcp_bytes += byte

    tcp_checksum = int.from_bytes(tcp_bytes[16:18])
    tcp_data = tcp_bytes[:16] + b'\x00\x00' + tcp_bytes[18:]

    return tcp_checksum, tcp_data
    
def read_address_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            ips = line.split()

    return ips[0], ips[1]

def ip_to_bytes(ip):
    ip_octets = ip.split('.')
    ip_bytes = b''
    for ip in ip_octets:
        ip_bytes += int(ip).to_bytes()

    return ip_bytes

def get_tcp_length(filename):
    length = os.path.getsize(filename)
    return length.to_bytes(2)

def get_ptcl():
    ptcl = 6
    return int.to_bytes(ptcl)

def pseudo_ip_header(source, dest, pctl, tcp_length):
    return source + dest + (0).to_bytes() + pctl + tcp_length

source_ip, dest_ip = read_address_file('/home/rsmith/beej/network-concepts/tcp_data/tcp_addrs_1.txt')
source_ip_bytes = ip_to_bytes(source_ip)
dest_ip_bytes = ip_to_bytes(dest_ip)
ptcl = get_ptcl()
tcp_length = get_tcp_length('/home/rsmith/beej/network-concepts/tcp_data/tcp_data_1.dat')
pseudo_header = pseudo_ip_header(source_ip_bytes, dest_ip_bytes, ptcl, tcp_length)

for i in range(10):
    print(validate_checksum('/home/rsmith/beej/network-concepts/tcp_data/tcp_addrs_' + str(i) + '.txt', '/home/rsmith/beej/network-concepts/tcp_data/tcp_data_' + str(i) +'.dat'))

