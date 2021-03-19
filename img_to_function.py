from classes import *

l = [Point(10,10), Point(100,50), Point(40,100), Point(80,90)]
def draw_by_list(canvas, l):
    for i in range(len(l)-1):
        canvas.create_line(l[i].x, l[i].y, l[i+1].x, l[i+1].y, fill="#476042", width=5)

def segment_function(p1, p2, t): # 0 <= t <= 1
    return p1 + (p2-p1)*t

def img_function(t): # 0<= t <= 1
    l = [Point(10,10), Point(100,50), Point(40,100), Point(80,90)]

    idx = int(t*len(l)-1)
    para = t*len(l)-idx
    return segment_function(l[idx], l[idx+1], para)

print(img_function(0.2).x)
print(img_function(0.4).y)
print(img_function(0.8))