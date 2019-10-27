import socket
import time 
import random
import argparse
from argparse import RawTextHelpFormatter
import hashlib

def parseArguments():
    parser = argparse.ArgumentParser(description='StopAndWait', formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version='')
    parser.add_argument('-ri', '--receiverip', required=True, help='Define receiver ip')
    parser.add_argument('-rp', '--receiverport', type=int, required=True, help='Define receiver port')

    return parser.parse_args()
    
def gen_hash(msg):
    hash_object = hashlib.md5(msg.encode())
    return hash_object.hexdigest()

# server_socket.settimeout(1)  

def main():
    args = parseArguments()
    dest = (args.receiverip, int(args.receiverport))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server_socket.bind(dest)
        print('Server established!')
        print('Waiting for packages')   
    except:
        print('Error establishing server...')

        exit()
    while (True):
        acknowledged = False
        while True:
            data, adress = server_socket.recvfrom(512)
            data_hash, adress = server_socket.recvfrom(512)
            check_hash = gen_hash(str(data, 'utf-8'))

            number = random.randint(0, 100)
            if(data_hash.decode('utf-8') != check_hash):
                print('Received \'' + str(data, 'utf-8') + '\' with error')
                print('Received hash: ' + data_hash.decode('utf-8'))
                print('Check hash: ' + check_hash)
                print('\n')
            elif(number > 30 and acknowledged == False):
                server_socket.sendto(b'Acknowledged', adress)
                print('Received \'' + str(data, 'utf-8') + '\' with ACK')
                print('\n')
                acknowledged = True
                break
            else:
                # server_socket.sendto(b'AKC', adress)
                print('Received \'' + str(data, 'utf-8') + '\', but could not send ACK')
                print('\n') 

if __name__ == '__main__':
    main()