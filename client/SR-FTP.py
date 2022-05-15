import ftplib
import hashlib
import sys
from hashlib import pbkdf2_hmac
from socket import *
from AESUtil import AESUtil
from config import *
import argparse


def send_tcp_request(message):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((remote_host, PORT))
    client.send(message)
    response = client.recv(4096)
    return response


def init():
    parser = argparse.ArgumentParser()
    if len(sys.argv) < 8 and len(sys.argv)!= 2:
        print('Missing Parameters')
        parser.print_usage()
        sys.exit(1)
    parser.add_argument('-u', '--username', help='FTP username')
    parser.add_argument('-p', '--password', help='FTP user password')
    parser.add_argument('-f', '--filename', help='Request file')
    parser.add_argument('-s', '--server', help='FTP server address')
    args = parser.parse_args()
    return args


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str)
    return my_md5.hexdigest()


if __name__ == '__main__':
    args = init()
    username = args.username
    password = args.password
    filename = args.filename
    remote_host = args.server

    req = '{}${}${}'.format(username, password, filename)
    print('packed request parameters\n' + req + '\n')
    enc_req = AESUtil(PRE_DEFINED_KEY).encrypt(req)
    print('use pre-defined key to encrypt the request\n' + enc_req.decode('utf-8') + '\n')

    response = send_tcp_request(enc_req)
    print('send to SR-FTP server...' + '\n')

    if response != b'file not found' and response != b'reject':
        print('received confirmation from the SR-FTP server' + '\n')
        remote_file_md5 = response.decode('utf-8')
        print('md5 value:\n' + remote_file_md5 + '\n')
        ftp = ftplib.FTP(remote_host)
        ftp.login('anonymous', '')

        # Grab file
        ftp.retrbinary("RETR enc_" + filename, open(filename, 'wb').write)
        ftp.close()

        # generate key
        key = pbkdf2_hmac('sha256', password.encode('utf-8'), filename.encode('utf-8'), 1000)
        print('generate the AES-key from the password\n' + key.hex() + '\n')

        # decrypt
        f = open(filename, 'rb')
        lines = f.read()
        print('grabbed encrypted successfully from the FTP server\n' + lines.decode('utf-8') + '\n')
        f.close()
        dec_lines = AESUtil(key).decrypt(lines)

        # verify
        dec_md5 = get_md5_value(dec_lines.encode('utf-8'))
        print('md5 value of the grabbed file\n' + dec_md5)
        if dec_md5 == remote_file_md5:
            print('The md5 value is the same, file integrity verification passed\n')

            # store to file
            f2 = open(filename, 'w')
            f2.write(dec_lines)
            f2.close()
            print('decrypt and store the file')
        else:
            print('The md5 value is not the same, origin:{}\ndecrypt:{}\n file integrity verification failed\n'.format(remote_file_md5,dec_md5))
            print('please try again')

    elif response == b'reject':
        print('login failed, please check your ftp username and password')
    elif response == b'file not found':
        print('file not found')
