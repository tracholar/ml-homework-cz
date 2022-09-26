class Solution(object):
    def minimumRefill(self, plants, capacityA, capacityB):
        """
        :type plants: List[int]
        :type capacityA: int
        :type capacityB: int
        :rtype: int
        """
        alice = 0
        bob = 0

        cAlice = capacityA
        cBob = capacityB

        pa = 0
        pb = len(plants)-1

        while pb >= pa:
            isAlice = pa != pb or (pa == pb and cAlice >= cBob)
            isBob = pa != pb or (pa == pb and cBob > cAlice)
            if isAlice:
                if cAlice < plants[pa]:

                    nAlice = plants[pa] // capacityA
                    alice += nAlice
                    left = plants[pa] % capacityA
                    if left > 0:
                        alice += 1
                        cAlice = capacityA - left
                    else:
                        cAlice = 0
                else:
                    cAlice = cAlice - plants[pa]



            if isBob:

                if cBob < plants[pb]:
                    nBob = plants[pb] // capacityB
                    bob += nBob
                    left = plants[pb] % capacityB

                    if left > 0:
                        bob += 1
                        cBob = capacityB - left
                    else:
                        cBob = 0
                else:
                    cBob = cBob - plants[pb]

            pa += 1
            pb -= 1
        return alice + bob

plants = [2,2,5,2,2]
A = 5
B = 5
print(Solution().minimumRefill(plants, A, B))