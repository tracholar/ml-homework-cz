# coding:utf-8

import sys
sys.path.append('./')

import CjfService
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # 参考链接
    # http://blog.sina.com.cn/s/blog_46dcac190101gn9h.html

    # socket
    port = TSocket.TSocket('localhost', 9001)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(port)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = CjfService.Client(protocol)

    # Connect!
    transport.open()

    path = "/Users/chengjiafeng/Desktop/test/test2.txt"
    filePath = "/Users/chengjiafeng/Desktop/test/"

    print(client.cat(path))

    transport.close()


if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)
