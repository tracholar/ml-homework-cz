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

    def copy(self):
        s = GobangState(self.width, self.height, self.myturn)
        s.state = self.state.copy()
        s.ai = self.ai
        s.user = self.user
        return s

    def place_ai(self, x, y):
        if self.state[x][y] != 0:
            return False
        self.state[x][y] = self.ai
        self.myturn = False
        return True

    def place_user(self, x, y):
        if self.state[x][y] != 0:
            return False
        self.state[x][y] = self.user
        self.myturn = True
        return True

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

    def up_diag(self, i):
        return [self[i-k, k] for k in range(i+1)]

    def down_diag(self, i):
        return [self[i+k, k] for k in range(self.height - i)]

    def __str__(self):
        sym = [' ', '●', '○']
        rows = [' '.join(sym[i] for i in x) for x in self.state]
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
    def score(state: GobangState, role=1):
        value, max_cnt = StateEval.eval(state, role)
        if max_cnt >= 5:
            return 1e9
        return value.get('live_4', 0) * 1e7 + \
               (value.get('live_3', 0) + value.get('left_live_4', 0) + value.get('right_live_4', 0)) * 1e5 + \
               (value.get('live_2', 0) + value.get('left_live_3', 0) + value.get('right_live_3', 0)) * 1e3 + \
               (value.get('live_1', 0) + value.get('left_live_2', 0) + value.get('right_live_2', 0))

    @staticmethod
    def next_potential_pos(state: GobangState):
        pos = []
        x, y = state.height // 2, state.width // 2
        if state[x, y] == 0:
            pos.append((x, y))
        for x in range(state.height):
            for y in range(state.width):
                if state[x, y] != 0:
                    ps = [(x, y+1), (x+1, y), (x+1, y+1), (x-1, y), (x, y-1), (x-1, y-1), (x+1, y-1), (x-1, y-1)]
                    for px, py in ps:
                        if px >= 0 and px < state.height and py >= 0 and py < state.width\
                                and state[px, py] == 0:
                            pos.append((px, py))
        return pos

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
    def min_max_search(s: GobangState, role=1, depth=2, min_max=-1):
        pos = StateEval.next_potential_pos(s)

        if len(pos) == 0:
            return None, 0

        if depth == 1:
            score = StateEval.pos_score(s, pos, role)
            score = [s * min_max for s in score]
            i = np.argmax(score)
            return pos[i], score[i]

        bpos, bscore = (), None
        for p in pos:
            s_tmp = s.copy()
            s_tmp[p] = role
            next_role = StateEval.change_role(role)
            _, best_score = StateEval.min_max_search(s_tmp, next_role, depth-1, -min_max)
            best_score = best_score * min_max

            myscore, _ = StateEval.eval(s_tmp, role)
            best_score = best_score + myscore
            if bscore is None or bscore < best_score:
                bpos = p
                bscore = best_score
        return bpos, bscore




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





def game_simulate(n = 13, search_depth = 2):
    s = GobangState(n, n)
    role = 1
    step = 0
    while not s.game_over:
        pos, score = StateEval.min_max_search(s, role, search_depth)
        if pos is None:
            break
        s[pos] = role
        print('Step:', step, 'pos:', pos, 'min_max score:', score)
        print(s)
        role = StateEval.change_role(role) # 换一个人
        step += 1
        # time.sleep(1)

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

if __name__ == '__main__':
    game_simulate(19, 2)