
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def __repr__(self):
        return '{}'.format(self.val)

    @staticmethod
    def buildTree(array):
        if array is None or len(array) == 0:
            return None

        v = array.pop(0)
        if v is None:
            return None

        T = TreeNode(v)
        T.left = TreeNode.buildTree(array)
        T.right = TreeNode.buildTree(array)
        return T



class Solution(object):
    def s2(self, root):
        if root is None:
            return []
        array = self.s2(root.left)
        array = array + self.s2(root.right)
        array = array + [root.val]
        return array

    def postorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        result = []
        p = root

        stack = []

        while len(stack)>0 or p is not None:
            if p is not None:
                result.insert(0, p.val)
                stack.append(p)
                p = p.left
            else:
                p = stack.pop(-1)
                p = p.right


        return result

T = TreeNode.buildTree([1,None,2,3])

s = Solution()
print(s.s2(T))