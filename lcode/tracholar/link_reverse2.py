

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

# 每隔N个翻转一次
def reverseList(head, N):

    pre = None
    cur = head

    newHead = None
    curTail = head
    lastTail = None
    i = 0
    while cur is not None:
        i += 1
        pnext = cur.next
        cur.next = pre

        if i == N:
            if newHead is None:
                newHead = cur

            curTail.next = pnext
            if lastTail is not None:
                lastTail.next = cur

            cur = pnext

            i = 0
            if cur is not None:
                lastTail = curTail
                curTail = cur
                pre = cur
                cur = cur.next

                i = 1
        else:
            pre = cur
            cur = pnext

    if newHead is None:
        newHead = pre
    return newHead


head = ListNode.build([1,2])
T = reverseList(head, 3)
T.print()
