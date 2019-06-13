#coding:utf-8
""" 实现FP Tree算法
1. 代码参考: https://github.com/enaeseth/python-fp-growth/blob/master/fp_growth.py
2. FP Tree 算法原理: Mining frequent patterns without candidate generation, 将论文中的例子动手演练一遍,就知道FP Tree构建的步骤了
"""
from movielens_dataset import MovieLens
import pandas as pd
from numba import jit
from collections import namedtuple

class TreeNode:
    def __init__(self, name, n_occur, parent):
        self.name = name
        self.n_occur = n_occur
        self.parent = parent

        self.node_link = None
        self.children = {}

    def add(self, child):
        if child.name not in self.children:
            self.children[child.name] = child

    def search(self, name):
        try:
            return self.children[name]
        except KeyError:
            return None

    def __contains__(self, name):
        return name in self.children

    def __repr__(self):
        return '{}:{}'.format(self.name, self.n_occur)

    def inc(self):
        self.n_occur += 1

    @property
    def is_root(self):
        return self.name is None

    @property
    def is_leaf(self):
        return len(self.children) == 0

class FPTree:
    Route = namedtuple('Route', ['head', 'tail']) # 一个简单的二元组构造类

    def __init__(self):
        self.root = TreeNode(None, None, None)
        self.head_table = {}

    def _update_head_table(self, point):
        """更新FP树的路由表,论文中叫 Head Table, key是item,即TreeNode.name, value是一个二元组,
        分别代表这个item关联的所有节点构成的链表的头尾指针, 每个节点内部由node_link指针关联了下一个
        节点,从而实现从head table出发的一条链表"""
        try:
            # 如果能在head table中找到当前节点对应的item,那么就将对应的链表延长
            route = self.head_table[point.name]
            route.tail.node_link = point
            self.head_table[point.name] = self.Route(route.head, point)
        except KeyError:
            # 如果找不到, 那么就在head table创建一个新的链表, 新链表的头尾指针都是point
            self.head_table[point.name] = self.Route(point, point)


    def add(self, transaction):
        """增加一条记录,更新每个节点的统计信息"""
        point = self.root
        for item in transaction:
            next_point = point.search(item)
            if next_point is not None: #found
                next_point.inc() # 将找到的这个节点次数+1
            else: # not found
                next_point = TreeNode(item, 1, point)
                point.add(next_point)
                self._update_head_table(next_point)
            point = next_point

    def items(self):
        """生成所有以item开头的节点链表 (item, [node1, node2, ...])"""
        for name in self.head_table:
            yield (name, self.nodes(name))

    def nodes(self, name):
        """生成以name为item的所有节点"""
        try:
            node = self.head_table[name].head
        except KeyError:
            return

        while node is not None:
            yield node
            node = node.node_link

    def prefix_paths(self, name):
        """生成以name结尾的前缀路径"""
        def collect_path(node):
            path = []
            while node is not None and not node.is_root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(name))

def conditional_tree_from_paths(paths):
    """从给定的前缀路径创建树"""
    tree = FPTree()
    condition_item = None
    items = set()

    for path in paths:
        if condition_item is None:
            condition_item = path[-1].name
        point = tree.root
        for node in path:
            next_point = point.search(node.name)
            if next_point is None:
                items.add(node.name)
                count = node.n_occur if node.name == condition_item else 0 # 除了最后的item,其他的都为0
                next_point = TreeNode(node.name, count, point)
                point.add(next_point)
                tree._update_head_table(next_point)
            point = next_point

    for path in tree.prefix_paths(condition_item):
        count = path[-1].n_occur  # condition item 的频率
        for node in path[:-1]:
            node.n_occur += count # 每条路径前缀节点的频率调整为condition item的频率,
                                  # 如果有多条路径,则加总

    return tree

def find_frequent_itemsets(transactions, min_support):
    cnt = count_item(transactions)
    cnt = {k:v for k,v in cnt.items() if v >= min_support}

    master_tree = FPTree()
    for trans in transactions:
        trans = sorted([t for t in trans if t in cnt and cnt[t] >= min_support], \
                       key=lambda t: cnt[t], reverse=True)
        master_tree.add(trans)

    def find_with_suffix(tree, suffix):
        for name, nodes in tree.items():
            support = sum(n.n_occur for n in nodes)

            if support >= min_support and name not in suffix: # 说明该item + suffix 是一个频繁模式
                found_set = [name] + suffix
                yield (found_set, support)

                # 构造条件树, 搜索频繁前缀, 搜索更长模式
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(name))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s

    for itemset in find_with_suffix(master_tree, []):
        yield itemset





@jit
def count_item(data):
    cnt = {}
    for row in data:
        for i in row:
            cnt[i] = cnt.get(i, 0) + 1
    return cnt

dataset = MovieLens()
df = dataset.get_user_like_list()
min_support = 10000

for items, support in find_frequent_itemsets(df.tolist(), min_support):
    if len(items) >= 2:
        print dataset.get_movie_list(items), support