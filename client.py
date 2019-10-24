import socket

def frames_divider(msg, n):
    
    for i in range(0, len(msg), n):
        yield msg[i:i+n]

dest = ('127.0.0.1', 9091)
while True:
    message = input('Digite sua mensagem:')
    delimiter = int(input('Tamanho do delimitador:'))
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for frame in frames_divider(message, delimiter):
        if len(frame) < delimiter:
            frame = frame.ljust(delimiter, '#')                 
        my_socket.sendto(bytes(frame, 'utf-8'), dest)
    print('\n')

my_socket.close()




