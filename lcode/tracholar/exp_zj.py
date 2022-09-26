
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def buildTree(arr):
        if len(arr) == 0:
            return None
        nodes = []
        for x in arr:
            if x is not None:
                nodes.append(TreeNode(x))
            else:
                nodes.append(None)

        n = len(nodes)
        for i, node in enumerate(nodes):
            if node is None:
                continue
            left = 2*i+1
            right = 2*i+2
            if left < n:
                node.left = nodes[left]
            if right < n:
                node.right = nodes[right]
        return nodes[0]

root = TreeNode.buildTree([0,1,2,3,4,None,6,7,8,9,10])

def dfs(root, arr):
    if root is None:
        return
    dfs(root.left, arr)
    dfs(root.right, arr)
    arr.append(root)

def bfs(root):
    arr = []
    arr.append(root)

    values = []
    while len(arr) != 0:
        p = arr.pop(0)
        values.append(p.value)

        if p.left:
            arr.append(p.left)
        if p.right:
            arr.append(p.right)
    return arr

def layer_bfs(root):
    arr = [root]
    values = []
    while len(arr) > 0:
        values.append([n.value for n in arr])
        nodes = []
        for n in arr:
            if n.left:
                nodes.append(n.left)
            if n.right:
                nodes.append(n.right)
        arr = nodes


def max_width(root):
    arr = [(root, 1)]

    width = 1
    while len(arr):
        tmp = []
        for node, i in arr:
            if node.left:
                tmp.append((node.left, i*2))
            if node.right:
                tmp.append((node.right, i*2+1))
        if len(tmp) > 0:
            width = max(width, tmp[-1][1] - tmp[0][1] + 1)
        arr = tmp
    return width


def max_width2(root):
    depth2idx = {}
    width = {}

    def _dfs(p, depth, i):
        if p is None:
            return 0
        if depth not in depth2idx:
            depth2idx[depth] = i
        return max(_dfs(p.left, depth+1, i*2),
                _dfs(p.right, depth+1, i*2+1),
                i - depth2idx[depth] + 1)
    _dfs(root, 1, 1)
    return max(width.values())

arr = []
dfs(root, arr)
print(arr)
print(bfs(root))
print(max_width(root))


