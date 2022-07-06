import socket


addr = socket.getaddrinfo('127.0.0.1', 65432)[0][-1]
print('address', addr)
s = socket.socket()
s.bind(addr)
s.listen(1)


print('trying to connect')
conn, addr = s.accept()
print('it made it')
print('client connected from', addr)
print('connection: ', conn)
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)

conn.close()