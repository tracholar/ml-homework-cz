
class MinStack(object):

    def __init__(self):
        self.data = []
        self.min = None

    def _update_min(self):
        if len(self.data) > 0:
            self.min = min(self.data)
        else:
            self.min = None

    def push(self, val):
        """
        :type val: int
        :rtype: None
        """
        self.data.append(val)
        self._update_min()


    def pop(self):
        """
        :rtype: None
        """
        value = self.data.pop()
        self._update_min()


    def top(self):
        """
        :rtype: int
        """
        if len(self.data) > 0:
            return self.data[-1]
        return None


    def getMin(self):
        """
        :rtype: int
        """
        return self.min
