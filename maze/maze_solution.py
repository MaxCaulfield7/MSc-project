# coding:utf-8


import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.cm as cm

# M[i,j] = [LEFT, UP, RIGHT, DOWN, CHECK_IF_VISITED]


def wall_follower(M,left_hand_rule=False):

    #  current cell（0，-1）
    previousX = 0
    previousY = -1
    currentX = 0
    currentY = 0
    shape = M.shape
    endX, endY = shape[0]-1,shape[1]-1
    path = []
    path.append((0,0))

    #  set a visited dict to store visited cell
    visited = dict()

    #  if not end point：
    while currentX!=endX or currentY!=endY:
        deltaX = currentX - previousX
        deltaY = currentY - previousY
        if deltaY==1:
            direction = 'east'
        elif deltaY==-1:
            direction = 'west'
        elif deltaX==1:
            direction = 'south'
        elif deltaX==-1:
            direction = 'north'
        arr = [None]*4
        if direction=='north':
            arr[0] = 'east'
            arr[1] = 'north'
            arr[2] = 'west'
            arr[3] = 'south'
        elif direction=='south':
            arr[0] = 'west'
            arr[1] = 'south'
            arr[2] = 'east'
            arr[3] = 'north'
        elif direction == 'east':
            arr[0] = 'south'
            arr[1] = 'east'
            arr[2] = 'north'
            arr[3] = 'west'
        elif direction == 'west':
            arr[0] = 'north'
            arr[1] = 'west'
            arr[2] = 'south'
            arr[3] = 'east'

        if left_hand_rule==True:
            tmp = arr[0]
            arr[0] = arr[2]
            arr[2] = tmp

        # if reach end point
        flag = False
        # iterate four direction
        for item in arr:
            if item=='east':
                if 'east' not in visited.get((currentX, currentY),[]) and M[currentX, currentY,2] == 1:
                    flag = True
                    newX = currentX
                    newY = currentY + 1
                    visited.setdefault((currentX,currentY),[])
                    visited[(currentX, currentY)].append("east")
                    break


            elif item=='west':
                if 'west' not in visited.get((currentX, currentY),[]) and M[currentX, currentY,0] == 1:
                    flag = True
                    newX = currentX
                    newY = currentY -1
                    visited.setdefault((currentX, currentY), [])
                    visited[(currentX, currentY)].append("west")
                    break

            elif item=='south':
                if 'south' not in visited.get((currentX, currentY),[]) and M[currentX, currentY,3] == 1:
                    flag = True
                    newX = currentX  + 1
                    newY = currentY
                    visited.setdefault((currentX, currentY), [])
                    visited[(currentX, currentY)].append("south")
                    break

            elif item=='north':
                if 'north' not in visited.get((currentX, currentY),[]) and M[currentX, currentY,1] == 1:
                    flag = True
                    newX = currentX - 1
                    newY = currentY
                    visited.setdefault((currentX, currentY), [])
                    visited[(currentX, currentY)].append("north")
                    break

        # cannor solve
        if flag==False:
            print('error')
            return []
        else:
            path.append((newX,newY))

        previousX = currentX
        previousY = currentY
        currentX = newX
        currentY = newY
    # path.append((endX,endY))
    return path

def A_star(maze):

    # get size
    size1 = maze.shape[0]
    size2 = maze.shape[1]

    # set start point and end point
    start = (0,0)
    end = (size1-1,size2-1)

    # save G and F
    F_dict = dict()
    G_dict = dict()

    # save open list and close list
    open_list = dict()
    close_list = list()

    # save path
    path = []
    current = start
    # save parent cell
    parent_dict = dict()

    r = (0,1)
    d = (1,0)

    if maze[0,0,2]==1:
        F_dict[r] = (end[0]-0+end[1]-1)
        G_dict[r] = 10
        open_list[r] = start
        parent_dict[r] = start

    if maze[0,0,3]==1:
        F_dict[d] = (end[0]-1+end[1]-0)
        G_dict[d] = 10
        open_list[d] = start
        parent_dict[d] = start

    close_list.append(start)

    while end not in close_list:
        # find min F + G
        min_node = None
        min_value = 20000

        # find corresponding cell
        for node in open_list.keys():
            if G_dict[node]+F_dict[node]<min_value:
                min_node = node

        i,j = min_node[0],min_node[1]
        open_list.pop(min_node)
        close_list.append(min_node)

        # if this cell can move in one of four direction
        if i>0 and maze[i,j,1]==1:
            tmp = (i-1,j)
            if tmp not in close_list:
                if tmp not in open_list:
                    F_dict[tmp] = (end[0] - (i-1) + end[1] - j)
                    G_dict[tmp] = G_dict[min_node]+10
                    open_list[tmp] = min_node
                    parent_dict[tmp] = min_node
                else:
                    if G_dict[min_node] + 10<G_dict[tmp]:
                        G_dict[tmp] = G_dict[min_node] + 10
                        open_list[tmp] = min_node
        if i<size1-1 and maze[i,j,3]==1: # down
            tmp = (i+1,j)
            if tmp not in close_list:
                if tmp not in open_list:
                    F_dict[tmp] = (end[0] - (i+1) + end[1] - j)
                    G_dict[tmp] = G_dict[min_node]+10
                    open_list[tmp] = min_node
                    parent_dict[tmp] = min_node

                else:
                    if G_dict[min_node] + 10<G_dict[tmp]:
                        G_dict[tmp] = G_dict[min_node] + 10
                        open_list[tmp] = min_node

        if j > 0 and maze[i, j, 0] == 1:  # left
            tmp = (i, j - 1)
            if tmp not in close_list:
                if tmp not in open_list:
                    F_dict[tmp] = (end[0] - (i) + end[1] - (j-1))
                    G_dict[tmp] = G_dict[min_node] + 10
                    open_list[tmp] = min_node
                    parent_dict[tmp] = min_node

                else:
                    if G_dict[min_node] + 10 < G_dict[tmp]:
                        G_dict[tmp] = G_dict[min_node] + 10
                        open_list[tmp] = min_node

        if j < size2- 1 and maze[i, j, 2] == 1:  # right
            tmp = (i, j+1)
            if tmp not in close_list:
                if tmp not in open_list:
                    F_dict[tmp] = (end[0] - (i) + end[1] - (j+1))
                    G_dict[tmp] = G_dict[min_node] + 10
                    open_list[tmp] = min_node
                    parent_dict[tmp] = min_node

                else:
                    if G_dict[min_node] + 10 < G_dict[tmp]:
                        G_dict[tmp] = G_dict[min_node] + 10
                        open_list[tmp] = min_node

    current = end
    while current!=start:
        path.append(current)
        current = parent_dict[current]
    path.append(start)
    path.reverse()
    return path


def mark_maze(maze,i,j):
    maze[i,j,4] = 2 # mark as visited


def recursive(maze,start,end,path):

    size1 = maze.shape[0]
    size2 = maze.shape[1]

    mark_maze(maze,start[0],start[1])

    if start[0]==end[0] and start[1]==end[1]:
        path.append(start)
        return True

    i,j = start[0],start[1]
    # loop four direction
    direction = ['up','down','left','right']
    random.shuffle(direction)
    # choose direction
    for dir in direction:
        if dir=='up':
            if i>0:
                #next = (i-1,j)
                if maze[i-1][j][4]!=2 and maze[i][j][1]==1:
                    if recursive(maze,(i-1,j),end,path)==True:
                        path.append(start)
                        return True
            else:
                continue

        elif dir=='down':
            if i<size1-1:
                if maze[i+1][j][4]!=2 and maze[i][j][3] == 1:
                    if recursive(maze, (i + 1, j),end,path)== True:
                        path.append(start)
                        return True

        elif dir=='left':

            if j>0:
                if maze[i][j-1][4]!=2 and maze[i][j][0] == 1:
                    if recursive(maze, (i, j-1),end,path) == True:
                        path.append(start)
                        return True

        elif dir=='right':

            if j<size2-1:
                if maze[i][j+1][4]!=2 and maze[i][j][2] == 1:
                    if recursive(maze, (i , j+1),end,path) == True:
                        path.append(start)
                        return True
    return False

