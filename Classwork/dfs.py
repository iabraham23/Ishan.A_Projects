class DepthFirstSearch:

#stack for depth

    def __init__(self, graph, start):
        self.marked = [False for _ in graph.adj]
        self.dfs(graph, start)

    def dfs(self, graph, v):
        self.marked[v] = True
        for w in graph.adj[v]:
            if not self.marked[w]:
                self.dfs(graph, w)
#takes 0(v + e), linear time: v is vertex e is edge.