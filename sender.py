import socket
import argparse
from argparse import RawTextHelpFormatter
import base64
import bitarray
import random
import string
import hashlib


def parseArguments():
    parser = argparse.ArgumentParser(description='StopAndWait', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='')
    parser.add_argument('-ri', '--receiverip', required=True, help='Define receiver ip')
    parser.add_argument('-rp', '--receiverport', type=int, required=True, help='Define receiver port')

    return parser.parse_args()

def frames_divider(msg, n):
    for i in range(0, len(msg), n):
        yield msg[i:i+n]

def change_bit(msg):
    return msg.replace(msg[0], random.choice(string.ascii_letters))


def gen_hash(msg):
    hash_object = hashlib.md5(msg.encode())
    return hash_object.hexdigest()

def main():
    args = parseArguments()
    dest = (args.receiverip, int(args.receiverport))
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.settimeout(1)
    
    while True:
        message = input('Digite sua mensagem:')
        delimiter = int(input('Tamanho do delimitador:'))    
        acknowledged = False

        for frame in frames_divider(message, delimiter):
            if len(frame) < delimiter:
                frame = frame.ljust(delimiter, '#')                 
            number = random.randint(0, 100)
            if(number < 30):
                aux_frame = change_bit(frame)
                hash_frame = gen_hash(str(frame))
                my_socket.sendto(bytes(aux_frame, 'utf-8'), dest)
                my_socket.sendto(bytes(hash_frame, 'utf-8'), dest)

            else:
                hash_frame = gen_hash(str(frame))
                my_socket.sendto(bytes(frame, 'utf-8'), dest)
                my_socket.sendto(bytes(hash_frame, 'utf-8'), dest)
                # my_socket.sendto(bytes(gen_hash(frame), 'utf-8'), dest)

            while True:
                try:
                    ACK, adress = my_socket.recvfrom(1024)
                    if (ACK.decode('utf-8') == 'ack'):  
                        acknowledged = True
                        print('Sucessful! Ack was received!')
                        print('#########')
                        break
                    else:
                        print('Transmission error! Resending frame: ' + str(frame))
                        print('#########')
                except socket.timeout:
                    hash_frame = gen_hash(str(frame))
                    print('Timeout! Resending frame: ' + str(frame))
                    print('#########')
                    # print('\n')
                    my_socket.sendto(bytes(frame, 'utf-8'), dest)
                    my_socket.sendto(bytes(hash_frame, 'utf-8'), dest)
                    acknowledged = False
                acknowledged = False
        print('New Message!')
        
    my_socket.close()



if __name__ == '__main__':
    main()