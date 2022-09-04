# coding:utf-8
import time

import numpy as np
class GobangState(object):
    def __init__(self, width = 9, height = 9, aiFirst = False):
        self.width = width
        self.height = height
        self.myturn = aiFirst
        self.state = np.zeros((height, width), dtype=int)
        self.ai = 1
        self.user = 2
        self.hist = []
        self.last_action = None

    def copy(self):
        s = GobangState(self.width, self.height, self.myturn)
        s.state = self.state.copy()
        s.ai = self.ai
        s.user = self.user
        return s

    def place_ai(self, x, y):
        if self[x, y] != 0:
            return False
        self[x, y] = self.ai
        self.myturn = False
        return True

    def place_user(self, x, y):
        if self[x, y] != 0:
            return False
        self[x, y] = self.user
        self.myturn = True
        return True

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value
        self.last_action = (key, value)

    def up_diag(self, i):
        return [self[i-k, k] for k in range(i+1)]

    def down_diag(self, i):
        return [self[i+k, k] for k in range(self.height - i)]

    def role_symbol(self, role):
        sym = [' ', '●', '○']
        return sym[role]

    def __str__(self):
        rows = ['{:2d}'.format(i) + (' '.join(self.role_symbol(i) for i in x)) + '|' for i,x in enumerate(self.state)]
        line = ' ' + ''.join('{:2d}'.format(i) for i in range(self.width))
        rows.insert(0, line)
        rows.append(line)
        return '\n'.join(rows)

    @property
    def game_over(self):
        """
        check whether game over
        :return: bool
        """
        return StateEval.game_over(self)


class GobangApi(object):
    def next_step(self, state : GobangState):
        raise NotImplementedError()


class StateEval(object):
    @staticmethod
    def eval_row(row, role):
        row = list(row) + [3-role]
        n = len(row)

        cum_cnt = 0
        left_live = False # 左侧是否是活棋，第一个肯定不是的
        value = {}
        max_cum_cnt = 0

        # 连续模板
        for i in range(n):
            if row[i] == role:  # 是自己的子
                cum_cnt += 1
                continue
            elif row[i] == 0: # 没有子
                if cum_cnt > 0:
                    if left_live is True:
                        k = 'live_' + str(cum_cnt)
                        value[k] = value.get(k, 0) + 1
                    else:
                        k = 'right_live_' + str(cum_cnt)
                        value[k] = value.get(k, 0) + 1
                left_live = True
                max_cum_cnt = max(max_cum_cnt, cum_cnt)
                cum_cnt = 0
                continue
            else:   # 是对方的子
                if cum_cnt > 0:
                    if left_live is True:
                        k = 'left_live_' + str(cum_cnt)
                        value[k] = value.get(k, 0) + 1
                    else:
                        k = 'dead_' + str(cum_cnt)
                        value[k] = value.get(k, 0) + 1
                left_live = False
                max_cum_cnt = max(max_cum_cnt, cum_cnt)
                cum_cnt = 0
                continue

        return value, max_cum_cnt

    @staticmethod
    def merge_value(a : dict, b : dict):
        z = a.copy()
        for k, v in b.items():
            z[k] = z.get(k, 0) + v
        return z

    @staticmethod
    def eval(state: GobangState, role=1):
        value = {}
        max_cum_cnt = 0
        for i in range(state.height):
            value_tmp_1, m1 = StateEval.eval_row(state[i, :], role)
            value_tmp_2, m2 = StateEval.eval_row(state[:, i], role)
            value_tmp_3, m3 = StateEval.eval_row(state.up_diag(i), role)
            value_tmp_4, m4 = StateEval.eval_row(state.down_diag(i), role)
            value_tmp = StateEval.merge_value(
                StateEval.merge_value(value_tmp_1, value_tmp_2),
                StateEval.merge_value(value_tmp_3, value_tmp_4)
            )
            value = StateEval.merge_value(value_tmp, value)
            max_cum_cnt = max(max_cum_cnt, m1, m2, m3, m4)

        return value, max_cum_cnt

    @staticmethod
    def _score(state: GobangState, role=1):
        value, max_cnt = StateEval.eval(state, role)
        if max_cnt >= 5:
            return np.inf
        return value.get('live_4', 0) * 1e7 + \
               (value.get('live_3', 0) + value.get('left_live_4', 0) + value.get('right_live_4', 0)) * 1e5 + \
               (value.get('live_2', 0) + value.get('left_live_3', 0) + value.get('right_live_3', 0)) * 1e3 + \
               (value.get('live_1', 0) + value.get('left_live_2', 0) + value.get('right_live_2', 0))

    # 状态评估函数
    @staticmethod
    def score(state: GobangState, role=1):
        return StateEval._score(state, role) - StateEval._score(state, StateEval.change_role(role))

    # 候选动作生成
    @staticmethod
    def next_potential_pos(state: GobangState):
        pos = []
        x, y = state.height // 2, state.width // 2
        if state[x, y] == 0:
            pos.append((x, y))
        for x in range(state.height):
            for y in range(state.width):
                if state[x, y] != 0:
                    ps = [(x, y+1),(x, y-1), (x+1, y), (x+1, y+1),(x+1, y-1), (x-1, y),  (x-1, y-1), (x-1, y+1)]
                    for px, py in ps:
                        if px >= 0 and px < state.height and py >= 0 and py < state.width\
                                and state[px, py] == 0:
                            pos.append((px, py))
        return list(set(pos))

    @staticmethod
    def pos_score(state: GobangState, pos, role):
        if isinstance(pos, list):
            return [StateEval.pos_score(state, p, role) for p in pos]

        s = state.copy()
        s[pos] = role
        return StateEval.score(s, role)

    @staticmethod
    def best_pos(s: GobangState, role):
        pos = StateEval.next_potential_pos(s)
        score = StateEval.pos_score(s, pos, role)
        i = np.argmax(score)
        return pos[i], score[i]

    @staticmethod
    def change_role(role):
        return 3 - role

    @staticmethod
    def min_max_search(s: GobangState, root_role=1, role=1, maxdepth=10, dfs_scale=1.0, depth=0, minmax=1):
        pos = StateEval.next_potential_pos(s)

        if depth >= maxdepth or len(pos) == 0\
                or (depth>=2 and np.random.rand() > np.exp(-1.0 * depth / dfs_scale)):
            return None, StateEval.score(s, root_role)

        bpos, bscore = (), None
        for p in pos:
            s_tmp = s.copy()
            s_tmp[p] = role
            next_role = StateEval.change_role(role)
            _, best_score = StateEval.min_max_search(s_tmp, root_role=root_role,
                                                     role=next_role,
                                                     dfs_scale=dfs_scale,
                                                     depth=depth+1,
                                                     maxdepth=maxdepth,
                                                     minmax=-minmax)
            best_score = best_score * minmax

            if bscore is None or bscore < best_score:
                bpos = p
                bscore = best_score
        return bpos, bscore * minmax


    @staticmethod
    def game_over(state : GobangState):
        value, max_cnt = StateEval.eval(state, 1)
        if max_cnt >= 5:
            return True
        value, max_cnt = StateEval.eval(state, 2)
        if max_cnt >= 5:
            return True
        if not np.any(state[:, :] == 0):
            return True
        return False

def game_simulate(n = 13, dfs_scale = 1.0):
    s = GobangState(n, n)
    role = 1
    step = 0
    while not s.game_over:
        t0 = time.time()
        pos, score = StateEval.min_max_search(s, root_role=role,
                                              role=role, dfs_scale=dfs_scale)
        if pos is None:
            break
        s[pos] = role
        print('Step:', step, 'Role:', s.role_symbol(role) ,
              'pos:', pos, 'min_max score:', score,
              'time:', int(time.time() - t0))
        print(s)
        role = StateEval.change_role(role) # 换一个人
        step += 1
        # time.sleep(1)

def test_minmaxsearch():
    s = GobangState(9, 9)
    s[3, 1] = 2
    s[3, 2:6] = 1
    print(StateEval.min_max_search(s, 1, 1))


def test():
    s = GobangState(9, 9)
    s[3, 3:5] = 1
    print(s)
    print(s[0, 0])
    print(s[0, :])
    print(s.up_diag(3))
    print(s.down_diag(3))

    print(StateEval.eval(s))
    print(StateEval.score(s, 2))
    pos = StateEval.next_potential_pos(s)
    print('pos:', pos)
    score = StateEval.pos_score(s, pos, 1)
    print(list(zip(pos, score)))

    best_pos = pos[np.argmax(score)]
    print('best_pos', best_pos)
    s[best_pos] = 1
    print(s)

    print(StateEval.best_pos(s, 2))
    print(StateEval.game_over(s))

def test_gen_pos():
    s = GobangState(9, 9)
    s[3, 3] = 1
    s[3, 4] = 2
    pos = StateEval.next_potential_pos(s)
    score = StateEval.pos_score(s, pos, 1)
    print(s)
    for p, sc in zip(pos, score):
        print('pos', p, 'score', sc)
        s_tmp = s.copy()
        s_tmp[p] = 1
        print(s_tmp)


if __name__ == '__main__':
    # test_minmaxsearch()
    # 减少 dfs_scale 可以加快搜索速度，但效果要差一些
    game_simulate(13, dfs_scale=0.00001)
    # test_gen_pos()