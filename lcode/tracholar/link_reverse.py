
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

class Solution(object):

    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head is None:
            return head

        p1 = head
        if head.next is None:
            return head
        p2 = head.next

        while p2 is not None:
            p3 = p2.next

            p2.next = p1
            p1 = p2
            p2 = p3
        head.next = None
        return p1

head = ListNode.build([1,2,3,4,5])
T = Solution().reverseList(head)
print(head)