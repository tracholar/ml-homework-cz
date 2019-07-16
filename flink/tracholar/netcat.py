#coding:utf-8

from socketserver import ThreadingTCPServer,BaseRequestHandler
import random
import time

def rand_str():
    s = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.sample(s, 5))

class Handler(BaseRequestHandler):
    def handle(self):
        while True:
            time.sleep()
            self.wfile.write(rand_str())

server = ThreadingTCPServer(('localhost', 1026), Handler)
server.serve_forever()





