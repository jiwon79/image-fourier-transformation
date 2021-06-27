def mst_dfs(mst, pointList):
    graph, color, pred = {}, {}, {}
    path = [0]

    N = len(pointList)
    for i in range(N):
        graph[i] = []

    for e in mst:
        graph[e[0]].append(e[1])
        graph[e[1]].append(e[0])

    def DFSvisit(node):
        color[node] = 1
        for adj in graph[node]:
            if color[adj] == 0:
                path.append(adj)
                pred[adj] = node
                DFSvisit(adj)
                path.append(pred[adj])
        color[node] = 2

    for node in graph.keys():
        color[node] = 0
        pred[node] = -1
    for node in graph.keys():
        if(color[node] == 0):
            DFSvisit(node)
    return path

def TSP_approx(path):
    result = []
    for p in path:
        if not p in result:
            result.append(p)
    return result