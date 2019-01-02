import socket

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.bind(('::', 1234))
data, addr = sock.recvfrom(1024)
print(data, addr)
