


class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def print(self):
        p = self
        while p is not None and p.val is not None:
            print(p.val, '-> ', end='')
            p = p.next
        print('nil')

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
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        pre = None
        cur = head

        n = 1
        newHead = None
        lastTail = None
        while cur is not None:
            if n % 2 == 0:
                # 翻转
                tmp = cur.next
                cur.next = pre
                pre.next = tmp

                if newHead is None:
                    newHead = cur

                if lastTail is not None:
                    lastTail.next = cur

                lastTail = pre

                cur = tmp
            else:
                pre = cur
                cur = cur.next

            n += 1
        return newHead


T = ListNode.build([1,2,3,4])
head = Solution().swapPairs(T)
head.print()