#coding:utf-8
import sys

class Node():
    def __init__(self, fa, lch, rch):
        self.fa = fa
        self.lch = lch
        self.rch = rch


class Tree():
    def __init__(self, n, root):
        self.n = n
        self.root = root
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.fa] = node

    def _deep(self, nid):
        if nid == 0:
            return 0

        node = self.nodes[nid]

        return 1 + max(self._deep(node.lch), self._deep(node.rch))

    def max_dist(self):
        root_node = self.nodes[self.root]
        ldeep = self._deep(root_node.lch)
        rdeep = self._deep(root_node.rch)

        return ldeep + 1 + rdeep


def get_tree_args():
    kv = raw_input().split(' ')
    return int(kv[0]), int(kv[1])

def get_node():
    kv = raw_input().split(' ')
    return Node(int(kv[0]), int(kv[1]), int(kv[2]))

n, root = get_tree_args()
tree = Tree(n, root)
for _ in range(n):
    node = get_node()
    tree.add_node(node)


print tree.max_dist()