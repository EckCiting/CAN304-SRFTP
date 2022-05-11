from pathlib import Path

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from config import *


def start_ftp_server():
    authorizer = DummyAuthorizer()

    for user in USERS:
        if not Path.exists(Path('file_folder/'+user[0])):
            Path.mkdir(Path('file_folder/'+user[0]))
        authorizer.add_user(user[0], user[1], 'file_folder/'+user[0], perm='elradfmwM')

    if not Path.exists(Path('file_folder/public')):
        Path.mkdir(Path('file_folder/public'))
    authorizer.add_anonymous('file_folder/public')

    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(('0.0.0.0', 21), handler)
    server.serve_forever()


# def start_ftp_server():
#     server.serve_forever()

