# coding:utf-8
# 改进版的五子棋API
import numpy as np


class Board(object):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    @staticmethod
    def change_role(role):
        if role not in (Board.BLACK, Board.WHITE):
            raise Exception("error role value " + str(role))
        return 3 - role

    def __init__(self, size = 9):
        self._size = size
        self._s = np.zeros((size, size), dtype=int)
        self._hist = []

    def place(self, pos, role):
        if self._s[pos] != Board.EMPTY:
            raise Exception("not empty pos " + str(pos))
        self._s[pos] = role
        self._hist.append((pos, role))

    # 悔棋
    def undo(self):
        if len(self._hist) == 0:
            return
        pos, role = self._hist.pop(-1)
        self._s[pos] = Board.EMPTY

    def __getitem__(self, item):
        return self._s[item]

    def __setitem__(self, key, value):
        self._s[key] = value

    def up_diag(self, i):
        return [self[i-k, k] for k in range(i+1)]

    def down_diag(self, i):
        return [self[i+k, k] for k in range(self._size - i)]

    def __str__(self):
        sym = [' ', '●', '○']
        rows = ['{:2d}'.format(i) + (' '.join(sym[i] for i in x)) + '|' for i,x in enumerate(self._s)]
        line = ' ' + ''.join('{:2d}'.format(i) for i in range(self._size))
        rows.insert(0, line)
        rows.append(line)
        return '\n'.join(rows)


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
    def eval(state: Board, role=1):
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
    def _score(state: Board, role=1):
        value, max_cnt = StateEval.eval(state, role)
        if max_cnt >= 5:
            return np.inf
        return value.get('live_4', 0) * 1e7 + \
               (value.get('live_3', 0) + value.get('left_live_4', 0) + value.get('right_live_4', 0)) * 1e5 + \
               (value.get('live_2', 0) + value.get('left_live_3', 0) + value.get('right_live_3', 0)) * 1e3 + \
               (value.get('live_1', 0) + value.get('left_live_2', 0) + value.get('right_live_2', 0))

    @staticmethod
    def score(state: Board, role=1):
        return StateEval._score(state, role) - StateEval._score(state, StateEval.change_role(role))

    @staticmethod
    def next_potential_pos(state: Board):
        pos = []
        x, y = state.height // 2, state.width // 2
        if state[x, y] == 0:
            pos.append((x, y))
        for x in range(state.height):
            for y in range(state.width):
                if state[x, y] != 0:
                    ps = [(x, y+1),(x, y-1), (x+1, y), (x+1, y+1),(x+1, y-1), (x-1, y),  (x-1, y-1),  (x-1, y+1)]
                    for px, py in ps:
                        if px >= 0 and px < state.height and py >= 0 and py < state.width \
                                and state[px, py] == 0:
                            pos.append((px, py))
        return pos

    @staticmethod
    def pos_score(state: Board, pos, role):
        if isinstance(pos, list):
            return [StateEval.pos_score(state, p, role) for p in pos]

        s = state.copy()
        s[pos] = role
        return StateEval.score(s, role)

    @staticmethod
    def best_pos(s: Board, role):
        pos = StateEval.next_potential_pos(s)
        score = StateEval.pos_score(s, pos, role)
        i = np.argmax(score)
        return pos[i], score[i]

    @staticmethod
    def change_role(role):
        return 3 - role

    @staticmethod
    def min_max_search(s: Board, role=1, depth=2):
        pos = StateEval.next_potential_pos(s)

        if len(pos) == 0:
            return None, 0

        if depth == 1:
            score = StateEval.pos_score(s, pos, role)
            i = np.argmax(score)
            return pos[i], score[i]

        bpos, bscore = (), None
        for p in pos:
            s_tmp = s.copy()
            s_tmp[p] = role
            next_role = StateEval.change_role(role)
            _, best_score = StateEval.min_max_search(s_tmp, next_role, depth-1)
            best_score = -best_score

            if bscore is None or bscore < best_score:
                bpos = p
                bscore = best_score
        return bpos, bscore




    @staticmethod
    def game_over(state : Board):
        value, max_cnt = StateEval.eval(state, 1)
        if max_cnt >= 5:
            return True
        value, max_cnt = StateEval.eval(state, 2)
        if max_cnt >= 5:
            return True
        if not np.any(state[:, :] == 0):
            return True
        return False


class AIPlayer(object):
    def __init__(self, depth = 2):
        self._depth = depth

    def next_pos(self, s : Board):
        return ()

