import socket
import argparse
from argparse import RawTextHelpFormatter

def parseArguments():
    parser = argparse.ArgumentParser(description='StopAndWait', formatter_class=RawTextHelpFormatter)
    parser.add_argument("-v", "--version", action='version', version='')
    parser.add_argument("-ri", "--receiveripl", required=True, help="Define receiver ip")
    parser.add_argument("-rp", "--receiverport", type=int, required=True, help="Define receiver port")

    return parser.parse_args()

def frames_divider(msg, n):
    
    for i in range(0, len(msg), n):
        yield msg[i:i+n]

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
            my_socket.sendto(bytes(frame, 'utf-8'), dest)
            while True:
                try:
                    ACK = my_socket.recvfrom(1024)
                    acknowledged = True
                    print(str(ACK, 'utf-8'))
                    break
                except socket.timeout:
                    print("TIME OUT! Resending frame: " + str(frame))  
                    my_socket.sendto(bytes(frame, 'utf-8'), dest)
                    acknowledged = False
                acknowledged = False
        print('\n')

    my_socket.close()



if __name__ == "__main__":
    main()