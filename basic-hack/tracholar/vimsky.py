from multiprocessing import Pool
from socket import socket, AF_INET, SOCK_STREAM
import sys

def fetch(port):
    ip = '47.93.116.66'
    addr = (ip, port)

    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(1)
    try:
        if s.connect_ex(addr) == 0:
            print("[*] {}:{} open".format(*addr))
        else:
            pass
            # print("[ ] {}:{} closed".format(*addr), file=sys.stderr, flush=True)
    except:
        print("{}:{} close".format(*addr))
        pass
    finally:
        s.close()

if __name__ == '__main__':
    ports = [80, 443, 8000, 8080] + list(range(1025, 10000))
    p = Pool(30)
    p.map(fetch, ports)

    fetch(80)

