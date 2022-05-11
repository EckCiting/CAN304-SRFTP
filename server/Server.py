from multiprocessing import Process
import tcp_server
import ftp_server
import threading

if __name__ == '__main__':

    tcp_server_p = Process(target=tcp_server.listening,args=())
    tcp_server_p.start()

    ftp_server_p = Process(target=ftp_server.start_ftp_server,args=())
    ftp_server_p.start()
