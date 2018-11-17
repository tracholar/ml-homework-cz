#coding:utf-8

import argparse
import logging
import socket
import numpy as np
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("distribute-lr")

n_feature = 1024
def RunServer(opt):
    host = socket.gethostbyname(socket.gethostname())
    port = opt['port']
    logger.info("run server at %s:%d" %( host,port ))

    def pull():
        #TODO return weight
        """
        注意返回 np.ndarray 时,需要转换为 Python list, 否则无法序列化
        :return: weight
        """
        raise NotImplementedError()

    def push(dw):
        raise NotImplementedError()


    from SimpleXMLRPCServer import SimpleXMLRPCServer
    server = SimpleXMLRPCServer((host, port), logRequests=False)
    server.register_function(pull)
    server.register_function(push)

    server.serve_forever()

def RunWorker(opt):
    logger.info("run worker at %s:%d" %(socket.gethostbyname(socket.gethostname()) , opt['port']))

    import xmlrpclib
    s = xmlrpclib.ServerProxy('http://' + opt['server'])

    from problem import gen_batch, loss_function

    for i in range(opt['max_iter']):
        # TODO 分布式随机梯度下降, 先从 server pull权重,计算梯度,然后 push 到server
        raise NotImplementedError()


"""
先启动server
python main.py  --role server --port 10000

然后启动多个worker
python main.py  --role worker --server <server-ip>:10000
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", help="server | worker", required=True)
    parser.add_argument("--server", help="server 机器 ip:port")
    parser.add_argument("--port", help="本机端口号", type=int)
    parser.add_argument("--max_iter", default=1000, help="迭代轮数", type=int)


    args = parser.parse_args()
    if args.role == 'server':
        RunServer({'port': args.port})
    else:
        RunWorker({'port' : args.port,
                   'server' : args.server,
                   'max_iter' : args.max_iter})