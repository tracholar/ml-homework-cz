# coding:utf-8

class TestCls():
    def __init__(self):
        self.name = 'testCls'

    def print(self):
        print(self.name)

def func(self, some):
    return self.name + some

TestCls.func = func

cls = TestCls()
print(cls.func(' hello'))