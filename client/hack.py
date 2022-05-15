import ftplib
from socket import *


def send_tcp_request(message):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('192.168.0.188', 1030))
    client.send(message)
    response = client.recv(4096)
    return response


# if __name__ == '__main__':
#     # simulate a client-to-server replay attack
#     enc_req = b'nM56IKoBGGhaY5wHUFP+ej+8u3P9EgwIsA2d/9Vw48I='
#     response = send_tcp_request(enc_req)
#     print('send to SR-FTP server...' + '\n')
#     print(response)  # b'5eb63bbbe01eeed093cb22bb8f5acdc3'

if __name__ == '__main__':
    ftp = ftplib.FTP('192.168.0.188')
    ftp.login('anonymous', '')

    # Grab file
    ftp.retrbinary("RETR enc_" + 'hello.txt',
                   open('hello.txt', 'wb').write)
    ftp.close()

    f = open('hello.txt')
    lines = f.read()
    print(lines)