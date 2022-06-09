# coding:utf-8

class TestCtx:
    def __init__(self):
        pass

    def __enter__(self):
        print('enter...')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit...')

from contextlib import contextmanager

@contextmanager
def test():
    print('enter...')
    yield
    print('exit...')


with TestCtx():
    print('inside')

with test():
    print('inside')