from pyamaze import maze,agent,textLabel
from queue import PriorityQueue
import math
from djitellopy import Tello

def angle_calc(lst, n):
    sum = 0;
    for i in range(len(lst) - 1):
        angle = math.atan2(lst[i][1] - lst[i+1][1], lst[i][0] - lst[i+1][0]) * 180 / 3.14
        all_angles.append(angle)


def h(cell1,cell2):
    x1,y1 = cell1
    x2,y2 = cell2

    return abs(x1-x2) + abs(y1-y2)

def aStar(m):
    start=(m.rows,m.cols)
    g_score= {cell:float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start,(1,1))

    open=PriorityQueue()
    open.put((h(start,(1,1)),h(start,(1,1)),start))
    aPath={}
    while not open.empty():
        currCell=open.get()[2]
        if currCell == (1,1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score = g_score[currCell]+1
                temp_f_score = temp_g_score+h(childCell,(1,1))

                if temp_f_score<f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score,h(childCell,(1,1)),childCell))
                    aPath[childCell] = currCell
    fwdPath = {}
    cell = (1,1)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath
hs = int(input("Enter the size of maze: "))
m =maze(hs,hs)
m.CreateMaze()
path = aStar(m)
x = list(path.values())
y=(hs,hs)
x.append(y)
print(x)
a=agent(m,footprints=True)
m.tracePath({a:path})
l=textLabel(m,'A Star Path Length',len(path)+1)

all_angles=[]
angle_calc(x,len(x))
print(all_angles)

m.run()

tello = Tello()
tello.connect()

print(f"Battery percentage: {tello.get_battery()}")
tello.takeoff()
for i in range(len(all_angles)):
    # w = B[i][0]
    # s = B[i][1]
    fwd = 20
    ang1 = all_angles[i]
    if(int(ang1) == 180):
        tello.move_right(fwd)
    if (int(ang1) == -90):
        tello.move_forward(fwd)
    if (int(ang1) == 0):
        tello.move_left(fwd)
    if (int(ang1) == 90):
        tello.move_back(fwd)


tello.land()


#the rotations should be counter clock wise
#we dont need the distance as it is unit distance and path is already found

