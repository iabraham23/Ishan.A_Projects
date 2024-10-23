from collections import deque


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def __str__(self):
        return f'[{self.left} {self.key} {self.right}]'
    def __repr__(self):
        return str(self)


t = Node('C', Node('F', Node('D')), Node('B', Node('A', Node('G'), Node('E'))))

#preorder: root, then left subtree recursive, then right subtree recursive
#inorder: left subtree recursive, root, right subtree recursive
#postorder: left, right, root
#level order: read across levels -- breadth first (wide), other 3 are depth first (deep)

def level_order(t):
    result = []
    if t:
        d = deque()
        d.append(t)
        while len(d):
            n = d.popleft()
            result.append(n.key)
            if n.left:
                d.append(n.left)
            if n.right:
                d.append(n.right)
    return result
def preorder(t):
    result = []

    def f(n):
        if n:
            result.append(n.key)
            f(n.left)
            f(n.right)
    f(t)
    return result
def inorder(t): #results in an in order traversal of binary search tree
    result = []

    def f(n):
        if n:
            f(n.left)
            result.append(n.key)
            f(n.right)
    f(t)
    return result
def postorder(t):
    result = []

    def f(n):
        if n:
            f(n.left)
            f(n.right)
            result.append(n.key)
    f(t)
    return result





