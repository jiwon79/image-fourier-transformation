from classes import *
from time import *
import math

# search every node O(n^2)
def nearest_point_n2(pointList, outline, p):
    dis = 800
    for point in pointList:
        if outline[point.y][point.x] == 0 and dis > p.getDistance(point):
            near = point
            dis = p.getDistance(point)
    outline[near.y][near.x] = 1
    return near

# search by bfs
def nearest_point_bfs(outline, p):
    n = 1
    adj = []
    while True:
        for i in range(n):
            direction = [(n-i, i), (-i, n-i), (-n+i, -i), (i, -n+i)]
            for dir in direction:
                x, y = p.x + dir[0], p.y + dir[1]
                if 0 <= x < 400 and 0 <= y < 400:
                    if outline[y][x] == 0:
                        adj.append(Point(x, y))

        if (len(adj) != 0):
            outline[adj[0].y][adj[0].x] = 1
            return adj[0]
        n += 1

# search by bfs & 탐색한 점 근처로 잡음
def nearest_point(outline, p):
    n = 1
    adj = []
    while True:
        for i in range(n):
            direction = [(n-i, i), (-i, n-i), (-n+i, -i), (i, -n+i)]
            for dir in direction:
                x, y = p.x + dir[0], p.y + dir[1]
                if 0 <= x < 400 and 0 <= y < 400:
                    if outline[y][x] == 0:
                        adj.append(Point(x, y))

        if (len(adj) != 0):
            max = -1
            for point in adj:
                direction = [(0,1), (1,0), (0,-1), (-1,0)]
                count = 0
                for dir in direction:
                    x, y = point.x+dir[1], point.y+dir[0]
                    if 0 <= x < 400 and 0 <= y < 400:
                        if outline[y][x] == 1:
                            count += 1
                if max < count:
                    max = count
                    near = point
            outline[near.y][near.x] = 1
            return near
        n += 1

# search circles
def circle(n):
    direction = []
    for i in range(n+1):
        if i==n:    a = 0
        else :
            a = ((n-0.5)**2-i**2)**0.5
        b = ((n+0.5)**2-i**2)**0.5
        for j in range(int(a)+1, int(b)+1):
            direction += [(i,j), (j,-i), (-i,-j), (-j,i)]
    return direction

def diamond(n):
    direction = []
    for i in range(n):
        direction += [(n-i, i), (-i, n-i), (-n+i, -i), (i, -n+i)]
    return direction

# search by bfs & make cluster
def nearest_point_cluster(outline, p, cluster):
    n = 1
    adj = []

    while True:
        direction = circle(n)
        # direction = diamond(n)
        # print(n)
        for dir in direction:
            x, y = p.x + dir[0], p.y + dir[1]
            if 0 <= x < 400 and 0 <= y < 400:
                if outline[y][x] == 0:
                    adj.append(Point(x, y))  
       
        if (len(adj) != 0):
            max = -1
            for point in adj:
                direction = [(0,1), (1,0), (0,-1), (-1,0)]
                count = 0
                for dir in direction:
                    x, y = point.x+dir[1], point.y+dir[0]
                    if 0 <= x < 400 and 0 <= y < 400:
                        if outline[y][x] == 1:
                            count += 1
                if max <= count:
                    max = count
                    near = point

            outline[near.y][near.x] = 1
            if n > 5:
                cluster[-1].append(near)
                cluster.append([near])
            else:
                cluster[-1].append(near)
            return near, cluster
        n += 1

# kruskal algorithm
def pointToGraph(pointList):
    N = len(pointList)
    print("N : ", N)
    graph = []
    print("kurskal graph start")
    t1 = time()
    
    for i in range(N):
        for j in range(i+1, N):
            graph.append((i, j, pointList[i].getDistance(pointList[j])))
    graph.sort(key = lambda x:x[2])
    t2 = time()
    print("krusal graph end", t2 - t1)
    return graph

def kruskal(graph, N):
    def find(u):
        if u != p[u]:
            p[u] = find(p[u])
        return p[u]
    
    def union(u, v):
        root1 = find(u)
        root2 = find(v)
        p[root2] = root1

    mst = []
    t2 = time()

    p = [i for i in range(N+1)]
    
    tree_edges = 0
    mst_cost = 0

    while True:
        if tree_edges == N-1:
            break
        u, v, wt = graph.pop(0)
        if find(u) != find(v):
            if (tree_edges/N > 0.98):
                print(tree_edges, end=" ")
            union(u, v)
            mst.append((u, v))
            mst_cost += wt
            tree_edges += 1

    # print("MST : ", mst)
    print("MST COST : ", mst_cost)
    print("MST end", time() - t2)
    return mst

def pointFind(p, pointList):
    for i in range(len(pointList)):
        if pointList[i] == p:
            return i
    return -1

def cluster_kruskal(cluster):
    mst_apro = []
    clusterGraph = []
    pairDict = {}
    for c in cluster:
        for i in range(len(c)-2):
            mst_apro.append((c[i], c[i+1]))
    
    for i in range(len(cluster)):
        for j in range(i+1, len(cluster)):
            d, pair = clusterDis3(cluster[i], cluster[j])
            clusterGraph.append((i, j, d))
            pairDict[(i, j)] = pair
            # print("pair : ", pair)
    clusterGraph.sort(key = lambda x:x[2])

    # print("cluster Graph : ", clusterGraph)
    print(len(cluster))
    clusterMST = kruskal(clusterGraph, len(cluster))
    print("Cluster MST : ", clusterMST)
    for e in clusterMST:
        mst_apro.append(pairDict[e])
    return mst_apro

# 모든 점들 사이 거리를 확인
def clusterDis(c1, c2):
    min = math.inf
    for i in range(len(c1)-1):
        for j in range(len(c2)-1):
            x, y = c1[i], c2[j]
            d = x.getDistance(y)
            if d <= min:
                min = d
                pair = (x,y)
    return min, pair

# 10번째 점들끼리만 확인
def clusterDis2(c1, c2):
    min = math.inf
    n, m = 10, 10
    for i in range((len(c1)-1)//n):
        for j in range((len(c2)-1)//m):
            x, y = c1[i*m], c2[j*m]
            d = x.getDistance(y)
            if d <= min:
                min = d
                pair = (x,y)
    return min, pair

# 10번째 점들끼리 보고 최소pair에서 근처 점을 탐색
def clusterDis3(c1, c2):
    min = math.inf
    n, m = 10, 10
    for i in range((len(c1)-1)//n):
        for j in range((len(c2)-1)//m):
            x, y = c1[i*m], c2[j*m]
            d = x.getDistance(y)
            if d <= min:
                min = d
                pair = (x,y)
                pairIdx = (i, j)

    for i in range((pairIdx[0]-1)*n, (pairIdx[0]+1)*m):
        for j in range((pairIdx[1]-1)*n, (pairIdx[1]+1)*m):
            if 0 <= i < len(c1)-1 and 0 <= j < len(c2)-1:
                x, y = c1[i], c2[j]
                d = x.getDistance(y)
                if d <= min:
                    min = d
                    pair = (x,y)
    
    return min, pair


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
    # print("pred : ", pred)
    return path
    return [pointList[i] for i in path]


if __name__ == "__main__":
    # pointList = [Point(0,0), Point(0,1), Point(0,2), Point(2,1), Point(3,1)]
    # cluster = [[Point(0,0), Point(0,1), Point(0,2), Point(2,1)], [Point(2,1), Point(3,1), Point(0,0)]]
    # pointGraph = pointToGraph(pointList)
    # mst = kruskal(pointGraph, len(pointList))
    # dfs = mst_dfs(mst, pointList)
    # print("MST : ", mst)
    # print("dfs path : ", dfs)

    pointGraph = [(0,1,3), (0,2,11), (0,3,12), (1,2,10), (1,3,11), (2,3,1)]
    pointGraph.sort(key = lambda x:x[2])
    mst = kruskal(pointGraph, 4)
    print(mst)
    # mst_apro = cluster_kruskal(cluster, pointList)
    # print(mst_apro)
    # mst_aproIdx = [(pointFind(mst_apro[i][0], pointList), pointFind(mst_apro[i][1], pointList)) for i in range(len(mst_apro))]
    # print(mst_aproIdx)
    # mst_path = mst_dfs(mst_aproIdx, pointList)
    # print(mst_path)
    # connectList = [pointList[i] for i in  mst_path]