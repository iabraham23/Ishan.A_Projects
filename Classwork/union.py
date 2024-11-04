#gets logarithmic time for find, connected, and union


class WeightedQuickUnion():
    def __init__(self, n):
        self.count = n
        self.parent = list(range(n))
        self.size = [1] * n

    """

    def find(self, p): #finds the root/identity
        while p != self.parent[p]:
            p = self.parent[p]
        return p
    """
    def find(self, p):  # finds the root/identity, and compresses (makes every node point to identity)

        if p == self.parent[p]:
            return p

        self.parent[p] = self.find(self.parent[p])
        return self.parent[p]




    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q:
            return
        if self.size[root_p] < self.size[root_q]:
            self.parent[root_p] = root_q #root p's parent is root q
            self.size[root_q] += self.size[root_p] #root q gets larger by amount of p
        else:
            self.parent[root_q] = root_p #root q's parents is root p
            self.size[root_p] += self.size[root_q]
        self.count -= 1