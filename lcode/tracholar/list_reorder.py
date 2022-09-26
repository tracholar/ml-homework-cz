

class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    @staticmethod
    def build(arr):
        if len(arr) == 0:
            return None;
        T = None
        head = None
        for v in arr:
            n = ListNode(v)
            if T is None:
                T = n
                head = T
            else:
                T.next = n
                T = T.next
        return head

    def __str__(self):
        return str(self.val)

class Solution(object):
    def reorderList(self, head):
        """
        :type head: ListNode
        :rtype: None Do not return anything, modify head in-place instead.
        """
        array = []
        p = head
        while p is not None:
            array.append(p)

        n = len(array)
        cur = None
        for i in range(n):
            if i % 2 == 0:
                p = array[i/2]
            else:
                p = array[n -1 - i/2]

            if cur is None:
                cur = p
            else:
                cur.next = p
                cur = p
        cur.next = None
        return head



head = ListNode.build([1,2,3,4,5,6,7])
T = Solution().reorderList(head)
print(T)