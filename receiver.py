import socket
import time 
import random 
dest = ('127.0.0.1', 9091)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(dest)
while (True):
    data, adress = server_socket.recvfrom(512)
    if (data):
        # print (data)
        number = random.randint(0,20)
        if(number < 10):
            time.sleep(0.5)
            print("Received \'" + str(data) + "\', but NO send AKC")
        else:
            server_socket.sendto(b'AKC', adress)
            print("Received \'" + str(data) + "\' with AKC")
        data = ''
    else:
        server_socket.close()
        exit()