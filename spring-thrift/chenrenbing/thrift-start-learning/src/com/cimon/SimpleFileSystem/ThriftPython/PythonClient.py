#coding:utf-8

import sys
import glob
sys.path.append('./')

import FileSystem
from  FileSystem import *
from FileSystem.ttypes import Mode,ThriftFile

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = FileSystem.Client(protocol)

    # Connect!
    transport.open()

    path="/Users/bing/Desktop/IDEAP/thrift-start-learning/Src/com/cimon/SimpleFileSystem"
    filePath = "/Users/bing/Desktop/IDEAP/thrift-start-learning/Src/com/cimon/SimpleFileSystem/StorageFile"

    print(client.cat(path+"/FileSystem.thrift",Mode.TXT))

    transport.close()


if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print('%s' % tx.message)