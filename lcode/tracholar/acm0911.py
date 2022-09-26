List = list

class Solution:
    def intervalInteract(self, a, b: List[int]):
        x, y = b
        xa, ya = a
        return (x>=xa and x<=ya) or (y>=xa and y<=ya ) or (xa >= x and xa <= y) or (ya>=x and ya<=y)

    def interact(self, a:List[int], arr:List[List[int]]):
        if len(arr) == 0:
            return False

        for x in arr:
            if self.intervalInteract(a, x):
                return True
        return False

    def minGroups(self, intervals: List[List[int]]) -> int:
        splitList = [[]]

        for interval in intervals:
            hasInteract = True
            target = None
            for arr in splitList:
                if not self.interact(interval, arr):
                    hasInteract = False
                    target = arr
                    break
            if hasInteract:
                splitList.append([interval])
            else:
                target.append(interval)

        return len(splitList)




s = Solution()
r = s.minGroups([[441459,446342],[801308,840640],[871890,963447],[228525,336985],[807945,946787],[479815,507766],[693292,944029],[751962,821744]])

print(r)