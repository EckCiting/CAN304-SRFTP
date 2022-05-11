import hashlib
from hashlib import pbkdf2_hmac
from ftplib import FTP
from os import path
from socket import *

from AESUtil import AESUtil
from config import *

bind_ip = '0.0.0.0'
bind_port = PORT


def user_exists(username, password):
    ftp = FTP('127.0.0.1')
    try:
        ftp.login(user=username, passwd=password)
        # Login successful
        return True
    except:
        # Login failed
        return False


def encrypt_file(username, password, filename):
    # read file
    print('reading file')
    f = open('file_folder/' + username + '/' + filename)
    lines = f.read()

    # generate key
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), filename.encode('utf-8'), 1000)

    try:
        # encrypt file
        print('encrypting file')
        enc_lines = AESUtil(key).encrypt(lines)
        f.close()

        # store to public folder
        print('storing file')
        f2 = open('file_folder/public/enc_' + filename, 'wb')
        f2.write(enc_lines)

        # note: this is the md5 value of original file
        md5_val = get_md5_value(lines.encode('utf-8'))
        f2.close()
        return md5_val

    except:
        return ''


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str)
    return my_md5.hexdigest()


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print('Received {}'.format(request))
    username, password, filename = AESUtil(PRE_DEFINED_KEY).decrypt(request).split('$')
    print('username: {}, password: {}, filename: {}'.format(username, password, filename))
    # check whether user have this file
    if user_exists(username, password):

        if path.exists('file_folder/' + username + '/' + filename):

            # encrypt the file and move to public area
            md5_val = encrypt_file(username, password, filename)
            if len(md5_val) != 0:
                client_socket.send(md5_val.encode('utf-8'))
            else:
                client_socket.send(b'encrypt failed')
        else:
            client_socket.send(b'file not found')

    # do not own this file
    else:
        client_socket.send(b'reject')

    client_socket.close()


def listening():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)  # max backlog of connections
    while True:
        print('Listening on {}:{}'.format(bind_ip, bind_port))
        client_sock, address = server.accept()
        print('Accepted connection from {}:{}'.format(address[0], address[1]))
        handle_client_connection(client_sock)
        # client_handler = threading.Thread(
        #     target=handle_client_connection,
        #     args=(client_sock,)
        # )
        # client_handler.start()
