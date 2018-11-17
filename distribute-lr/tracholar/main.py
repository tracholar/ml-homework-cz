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


    global w, lr, step, reg
    w = np.zeros(n_feature)
    lr = 1
    step = 0
    reg = 1e-3
    def pull():
        global w
        return w.tolist()

    def push(dw):
        global w, step, lr, reg
        w -= lr * np.array(dw) + 0.5 * reg * w
        step += 1
        if step % 1000 == 0:
            logger.info("w: %s" % str(w[:5]))

            if step % 5000 == 0:
                lr /= 2
        return True

    def close():
        sys.exit(0)

    from SimpleXMLRPCServer import SimpleXMLRPCServer
    server = SimpleXMLRPCServer((host, port), logRequests=False)
    server.register_function(pull)
    server.register_function(push)
    server.register_function(close)

    server.serve_forever()

def RunWorker(opt):
    logger.info("run worker at %s:%d" %(socket.gethostbyname(socket.gethostname()) , opt['port']))

    import xmlrpclib
    s = xmlrpclib.ServerProxy('http://' + opt['server'])

    from problem import gen_batch, loss_function

    cum_loss = 0
    loss_decay = 0.9
    for i in range(opt['max_iter']):
        w = np.array(s.pull())
        w_, X, y = gen_batch(128, dim=n_feature)
        loss, g = loss_function(w, X, y)
        cum_loss = cum_loss * loss_decay + (1-loss_decay) * loss
        s.push(g.tolist())

        logger.info("iter:%d\tloss:%.5f\tnorm(g):%.5f\t%s" % (i, cum_loss, np.linalg.norm(g), str(w_[:3])))

    print 'w:', w


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", help="server | worker", required=True)
    parser.add_argument("--server", help="server 机器 ip:port")
    parser.add_argument("--port", help="本机端口号", type=int, required=True)
    parser.add_argument("--max_iter", default=1000, help="迭代轮数", type=int)


    args = parser.parse_args()
    if args.role == 'server':
        RunServer({'port': args.port})
    else:
        RunWorker({'port' : args.port,
                   'server' : args.server,
                   'max_iter' : args.max_iter})
