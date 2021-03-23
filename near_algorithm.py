from classes import *

# search every node O(n^2)
def nearest_point_n2(pointList, outline, p):
    dis = 800
    for point in pointList:
        if outline[point.y][point.x] == 255 and dis > p.getDistance(point):
            near = point
            dis = p.getDistance(point)
    outline[near.y][near.x] = 254
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
                    if outline[y][x] == 255:
                        adj.append(Point(x, y))

        if (len(adj) != 0):
            outline[adj[0].y][adj[0].x] = 254
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
                    if outline[y][x] == 255:
                        adj.append(Point(x, y))

        if (len(adj) != 0):
            max = -1
            for point in adj:
                direction = [(0,1), (1,0), (0,-1), (-1,0)]
                count = 0
                for dir in direction:
                    x, y = point.x+dir[1], point.y+dir[0]
                    if 0 <= x < 400 and 0 <= y < 400:
                        if outline[y][x] == 254:
                            count += 1
                if max < count:
                    max = count
                    near = point
            outline[near.y][near.x] = 254
            return near
        n += 1