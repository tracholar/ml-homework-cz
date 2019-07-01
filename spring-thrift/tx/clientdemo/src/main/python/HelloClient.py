from Hello import HelloWorld,constants,ttypes
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    transport = TSocket.TSocket('localhost', 9122)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    transport.open()

    client=HelloWorld.Client(protocol)

    print(client.cat("/Users/xuetang/Downloads/test.txt",ttypes.ModeStatus.TEXT))


    client.upload("/Users/xuetang/Downloads/test2.txt","hhh")

    transport.close()

if __name__=='__main__':
    main()




    
