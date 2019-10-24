import socket
port=9091
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', port))
while (True):
    data, adress = server_socket.recvfrom(512)
    if (data):
        print (str(data,'utf-8'))
        data = ''
    else:
        server_socket.close()
        exit()