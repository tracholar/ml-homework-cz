
class TreeNode(object):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def build(array):
        def buildNode(v):
            if v is None:
                return None
            return TreeNode(v)

        n = 1
        root = TreeNode(array.pop(0))
        queue = [root]
        while len(array) > 0:
            children = []
            for n in queue:
                if n is None:
                    continue
                if len(array) > 0:
                    n.left = buildNode(array.pop(0))
                if len(array) > 0:
                    n.right = buildNode(array.pop(0))

                children.append(n.left)
                children.append(n.right)

