import sys
input = sys.stdin.readline

BITS = 20

class TrieNode:
    __slots__ = ("child", "count", "ids")
    def __init__(self):
        self.child = [None, None]
        self.count = 0
        self.ids = set()

class XORTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, code, id):
        node = self.root
        for b in range(BITS-1, -1, -1):
            bit = (code >> b) & 1
            if node.child[bit] is None:
                node.child[bit] = TrieNode()
            node = node.child[bit]
            node.count += 1
        node.ids.add(id)

    def remove(self, code, id):
        node = self.root
        for b in range(BITS-1, -1, -1):
            bit = (code >> b) & 1
            node = node.child[bit]
            node.count -= 1
        node.ids.remove(id)

    def query(self, code):
        node = self.root
        xorVal = 0
        for b in range(BITS-1, -1, -1):
            bit = (code >> b) & 1
            desired = bit ^ 1
            if node.child[desired] and node.child[desired].count > 0:
                xorVal |= (1 << b)
                node = node.child[desired]
            else:
                node = node.child[bit]
        witness = min(node.ids)
        return xorVal, witness

def main():
    M = int(input())
    trie = XORTrie()
    active = {}
    for _ in range(M):
        parts = input().split()
        if parts[0] == "ON":
            id, code = int(parts[1]), int(parts[2])
            active[id] = code
            trie.insert(code, id)
        elif parts[0] == "OFF":
            id = int(parts[1])
            code = active[id]
            trie.remove(code, id)
            del active[id]
        else:  # CHECK
            code = int(parts[1])
            val, witness = trie.query(code)
            print(val, witness)

if __name__ == "__main__":
    main()
