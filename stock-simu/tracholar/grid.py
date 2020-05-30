#coding:utf-8
"""网格交易法"""
import logging
import numpy as np


def roundn(d, n):
    return round(d * pow(10, n))/pow(10, n)

# 份额，成本，最新价格
class CangweiState(dict):
    def __getattr__(self, item):
        return self[item]
    def __setattr__(self, key, value):
        self[key] = value

    def __init__(self):
        self.fenge = 0
        self.cost = 0
        self.price = 1         # 当前价格
        self.last_price = 1 # 上次交易价格

    def buy(self, amount, price):
        self.update(price)
        if amount <= 0:
            return
        self.last_price = price
        self.fenge += amount / price
        self.cost += amount

    def sell(self, amount, price):
        self.update(price)
        value = self.fenge * price
        amount = min(amount, value)
        self.buy(-amount, price)

    def update(self, price):
        self.price = price


    def get_inc_amount(self):
        return self.price * self.fenge - self.cost

    def __str__(self):
        d = dict(self)
        d['inc_amount'] = roundn(self.get_inc_amount(), 0)
        if self.cost > 0:
            d['inc_ratio'] = roundn(d['inc_amount'] / self.cost, 3)
        d['fenge'] = roundn(self.fenge, 0)
        d['cost'] = roundn(self.cost, 0)
        if self.fenge > 0:
            d['cost_per'] = roundn(self.cost / self.fenge, 4)
        d['price'] = roundn(self.price, 4)
        return str(d)


class StockStrategy(object):
    def on_action(self, price):
        raise NotImplementedError()

    def get_state(self):
        raise NotImplementedError()

    def __init__(self):
        self.inc_ammount = []
        self.cost = []

    def simulate(self, prices):
        for p in prices:
            self.on_action(p)

            self.inc_ammount.append(self.state.get_inc_amount())
            self.cost.append(self.state.cost)
        return self.get_state()

class DingtouStrategy(StockStrategy):

    def __init__(self, amount=1000, init_amount = 10000):
        super(DingtouStrategy, self).__init__()
        # 初始持仓1W
        self.state = CangweiState()
        self.step = 0

        self.amount = amount
        self.init_amount = init_amount

    def get_state(self):
        return self.state


    def on_action(self, price):
        self.step += 1

        if self.step == 1:
            self.state.buy(self.init_amount, price)
            return

        m = self.amount
        self.state.buy(m, price)


        logging.info('买入{}元', m)


class BasicGridStrategy(StockStrategy):
    def __init__(self, amount=1000, init_amount = 10000):
        super(BasicGridStrategy, self).__init__()
        # 初始持仓1W
        self.state = CangweiState()
        self.step = 0
        self.amount = amount
        self.init_amount = init_amount

    def get_state(self):
        return self.state


    def on_action(self, price):
        self.step += 1

        if self.step == 1:
            self.state.buy(self.init_amount, price)
            return


        diff = round((price / self.state.last_price - 1)*100)

        self.state.update(price)
        if diff < 0:
            m = - self.amount * diff
            self.state.buy(m, price)
            logging.info('买入{}元', m)
        elif diff > 0:
            m = self.amount * diff
            self.state.sell(m, price)
            logging.info('卖出{}元', m)




def rnd_price(n = 200):
    p = []
    t = 0.0
    for _ in range(n):
        t += np.random.rand() - 0.5
        p.append(t)
    return np.array(p)

if __name__ == '__main__':
    n = 200

    print '单边上涨'
    prices = np.linspace(1, 2, n)
    print '网格策略', BasicGridStrategy().simulate(prices)
    print '定投策略', DingtouStrategy().simulate(prices)

    print '\n单边下跌'
    prices = 2.5 - np.linspace(1, 2, n)
    print '网格策略', BasicGridStrategy().simulate(prices)
    print '定投策略', DingtouStrategy().simulate(prices)

    print '\n正弦波'
    prices = np.sin(np.linspace(1, 2, n) * 20/2/np.pi)*0.5 + 1
    print '网格策略', BasicGridStrategy().simulate(prices)
    print '定投策略', DingtouStrategy().simulate(prices)

    print '\n随机游走'
    prices = rnd_price(n) * 0.3 + 1
    print '网格策略', BasicGridStrategy().simulate(prices)
    print '定投策略', DingtouStrategy().simulate(prices)

