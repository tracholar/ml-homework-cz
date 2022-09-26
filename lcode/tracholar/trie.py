
class Node(object):
    def __init__(self, value = False, children = None):
        """
        :param value: whether stands for a word, default False
        :param children: children list
        """
        self.value = value

        if children is None:
            self.children = {}
        elif isinstance(children, dict):
            self.children = children
        else:
            raise Exception('')

    def add_child(self, key, node):
        self.children[key] = node

    def has_child(self, c):
        return self.children is not None and len(self.children) > 0 and c in self.children

class Trie(object):

    def __init__(self):
        self.root = Node()

    def insert(self, word):
        """
        :type word: str
        :rtype: None
        """
        p = self.root
        for c in word:
            if not p.has_child(c):
                p.add_child(c, Node())

            p = p.children[c]
        p.value = True # 设置为ture


    def search(self, word):
        """
        :type word: str
        :rtype: bool
        """
        p = self.root
        for c in word:
            if not p.has_child(c):
                return False
            p = p.children[c]
        return p.value


    def startsWith(self, prefix):
        """
        :type prefix: str
        :rtype: bool
        """
        p = self.root
        for c in prefix:
            if not p.has_child(c):
                return False
            p = p.children[c]
        return True



trie =  Trie()
trie.insert("apple")
print(trie.search("apple"))
print(trie.search("app"))
print(trie.startsWith("app"))
print(trie.insert("app"))
print(trie.search("app"))
