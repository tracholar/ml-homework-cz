# -*- coding:utf-8 -*-
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.val)

class Solution:
    def findRoot(self, pRoot1, node):
        roots = []
        if pRoot1 is None:
            return roots

        if pRoot1.val == node.val:
            roots.append(pRoot1)

        roots.extend(self.findRoot(pRoot1.left, node))
        roots.extend(self.findRoot(pRoot1.right, node))

        return roots

    def match(self, p1, p2):
        if p2 is None:
            return True

        if p1 is None:
            return False

        return self.match(p1.left, p2.left) and self.match(p1.right, p2.right)

    def HasSubtree(self, pRoot1, pRoot2):
        # write code here

        if pRoot1 is None or pRoot2 is None:
            return False

        roots = self.findRoot(pRoot1, pRoot2)

        if len(roots) == 0:
            return False

        return any([self.match(r, pRoot2) for r in roots])


if __name__ == '__main__':
    s = Solution()
    t1 = TreeNode(1)
    t1.left = TreeNode(2)
    t1.left.left = TreeNode(3)
    t1.left.right = TreeNode(4)

    t2 = TreeNode(2)
    t2.left = TreeNode(3)


    print s.HasSubtree(t1, t2)